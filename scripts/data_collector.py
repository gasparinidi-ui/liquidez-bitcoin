"""
LIQUIDEZ BTC · GDI — data_collector.py

Busca os 30 indicadores de liquidez global/cripto em fontes 100% gratuitas
e grava data_live.json na raiz do repositório. Pensado para rodar via
GitHub Actions (ver .github/workflows/update-data.yml), mas roda igual
localmente:

    pip install -r scripts/requirements.txt
    export FRED_API_KEY=xxxxxxxx
    python scripts/data_collector.py

Filosofia: cada indicador é buscado de forma independente e isolada — se
uma fonte falhar (rate limit, mudança de schema, indisponibilidade), o
script segue em frente e apenas mantém o último valor conhecido (ou grava
None), sem derrubar a atualização dos demais 29 indicadores.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_live.json")

HEADERS = {"User-Agent": "liquidez-btc-gdi/1.0 (+https://github.com/)"}


def safe_call(fn, *args, **kwargs):
    """Executa fn isolando falhas — nunca deixa uma fonte quebrar as outras."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        print(f"[WARN] {fn.__name__}({args}, {kwargs}) falhou: {exc}", file=sys.stderr)
        return None


# ── FRED ──────────────────────────────────────────────────────────────
def fetch_fred_series(series_id, units=None):
    """Retorna (valor_mais_recente, valor_anterior, data) de uma série do FRED."""
    if not FRED_API_KEY:
        print(f"[SKIP] FRED_API_KEY ausente — pulando {series_id}", file=sys.stderr)
        return None
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 2,
    }
    if units:
        params["units"] = units
    r = requests.get(FRED_BASE, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    obs = [o for o in r.json().get("observations", []) if o.get("value") not in (None, ".")]
    if not obs:
        return None
    latest = float(obs[0]["value"])
    prev = float(obs[1]["value"]) if len(obs) > 1 else None
    change_pct = round((latest - prev) / prev * 100, 3) if prev else None
    return {"value": latest, "change_pct": change_pct, "as_of": obs[0]["date"]}


# ── Yahoo Finance (via yfinance) ────────────────────────────────────────
def fetch_yfinance(ticker):
    import yfinance as yf

    hist = yf.Ticker(ticker).history(period="5d")
    if hist.empty:
        return None
    closes = hist["Close"].dropna()
    latest = float(closes.iloc[-1])
    prev = float(closes.iloc[-2]) if len(closes) > 1 else None
    change_pct = round((latest - prev) / prev * 100, 3) if prev else None
    as_of = closes.index[-1].strftime("%Y-%m-%d")
    return {"value": latest, "change_pct": change_pct, "as_of": as_of}


# ── DefiLlama (stablecoins) ─────────────────────────────────────────────
def fetch_stablecoin_supply():
    r = requests.get("https://stablecoins.llama.fi/stablecoins?includePrices=false", headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json().get("peggedAssets", [])
    total_usd = sum(
        (a.get("circulating", {}) or {}).get("peggedUSD", 0) or 0
        for a in data
    )
    total_bi = round(total_usd / 1e9, 2)
    return {"value": total_bi, "change_pct": None, "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d")}


# ── Alternative.me (Fear & Greed) ───────────────────────────────────────
def fetch_fear_greed():
    r = requests.get("https://api.alternative.me/fng/?limit=2", headers=HEADERS, timeout=20)
    r.raise_for_status()
    entries = r.json().get("data", [])
    if not entries:
        return None
    latest = int(entries[0]["value"])
    prev = int(entries[1]["value"]) if len(entries) > 1 else None
    change_pct = round((latest - prev) / prev * 100, 2) if prev else None
    as_of = datetime.fromtimestamp(int(entries[0]["timestamp"]), tz=timezone.utc).strftime("%Y-%m-%d")
    return {"value": latest, "change_pct": change_pct, "as_of": as_of}


# ── OKX (funding rate + open interest, sem bloqueio geográfico) ────────
def fetch_okx_funding_rate():
    r = requests.get(
        "https://www.okx.com/api/v5/public/funding-rate",
        params={"instId": "BTC-USDT-SWAP"},
        headers=HEADERS, timeout=20,
    )
    r.raise_for_status()
    rows = r.json().get("data", [])
    if not rows:
        return None
    latest = float(rows[0]["fundingRate"]) * 100
    as_of = datetime.fromtimestamp(int(rows[0]["fundingTime"]) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    return {"value": round(latest, 4), "change_pct": None, "as_of": as_of}


def fetch_okx_open_interest():
    r = requests.get(
        "https://www.okx.com/api/v5/public/open-interest",
        params={"instId": "BTC-USDT-SWAP"},
        headers=HEADERS, timeout=20,
    )
    r.raise_for_status()
    rows = r.json().get("data", [])
    if not rows:
        return None
    oi_ccy = float(rows[0]["oiCcy"])  # em BTC
    tick = requests.get(
        "https://www.okx.com/api/v5/market/ticker",
        params={"instId": "BTC-USDT-SWAP"},
        headers=HEADERS, timeout=20,
    ).json()
    price = float(tick["data"][0]["last"])
    value_bi = round(oi_ccy * price / 1e9, 3)
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    return {"value": value_bi, "change_pct": None, "as_of": as_of}


# ── Farside Investors (fluxo diário de ETFs spot BTC) ────────────────────
FARSIDE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://farside.co.uk/",
}


def fetch_btc_etf_netflow():
    import pandas as pd
    import io

    r = requests.get("https://farside.co.uk/btc/", headers=FARSIDE_HEADERS, timeout=20)
    r.raise_for_status()
    tables = pd.read_html(io.StringIO(r.text), header=0)
    df = next((t for t in tables if "Total" in t.columns), None)
    if df is None or df.empty:
        return None
    last_row = df.iloc[-2] if str(df.iloc[-1, 0]).lower().startswith("total") else df.iloc[-1]
    value = float(str(last_row["Total"]).replace(",", "").replace("(", "-").replace(")", ""))
    as_of = str(last_row.get(df.columns[0], ""))
    return {"value": value, "change_pct": None, "as_of": as_of}


# ── Montagem final ────────────────────────────────────────────────────
def build_metrics():
    metrics = {}

    # A. Bancos Centrais
    metrics["fed_balance_sheet"] = safe_call(fetch_fred_series, "WALCL")  # milhões USD
    if metrics["fed_balance_sheet"]:
        metrics["fed_balance_sheet"]["value"] = round(metrics["fed_balance_sheet"]["value"] / 1e6, 3)  # -> US$ tri
    metrics["reverse_repo"] = safe_call(fetch_fred_series, "RRPONTSYD")
    metrics["tga_balance"] = safe_call(fetch_fred_series, "WTREGEN")
    metrics["ecb_balance_sheet"] = safe_call(fetch_fred_series, "ECBASSETSW")
    metrics["boj_balance_sheet"] = safe_call(fetch_fred_series, "JPNASSETS")
    metrics["pboc_balance_sheet"] = None  # sem fonte gratuita confiável em API — atualização manual

    if metrics.get("fed_balance_sheet") and metrics.get("tga_balance") and metrics.get("reverse_repo"):
        net = metrics["fed_balance_sheet"]["value"] * 1000 - metrics["tga_balance"]["value"] - metrics["reverse_repo"]["value"] / 1000
        metrics["fed_net_liquidity"] = {"value": round(net / 1000, 3), "change_pct": None, "as_of": metrics["fed_balance_sheet"]["as_of"]}
    else:
        metrics["fed_net_liquidity"] = None

    # B. Agregados Globais — calculados a partir de séries já buscadas quando possível
    metrics["gli_index"] = None  # requer BoE + PBoC — completar manualmente ou expandir fetch_fred_series
    metrics["m2_global_g4"] = None
    metrics["bis_credit_impulse"] = None  # BIS não tem API JSON simples — download CSV manual (ver fontes.html)

    # C. Oferta de Moeda
    metrics["us_m2"] = safe_call(fetch_fred_series, "M2SL")
    if metrics["us_m2"]:
        metrics["us_m2"]["value"] = round(metrics["us_m2"]["value"] / 1000, 3)  # bi -> tri
    metrics["eurozone_m3"] = None  # ECB SDW requer parsing SDMX — ver fontes.html
    metrics["china_m2"] = None
    metrics["japan_m2"] = safe_call(fetch_fred_series, "MYAGM2JPM189S")

    # D. Juros & Crédito
    metrics["fed_funds_rate"] = safe_call(fetch_fred_series, "FEDFUNDS")
    metrics["sofr_rate"] = safe_call(fetch_fred_series, "SOFR")
    metrics["ust10y"] = safe_call(fetch_fred_series, "DGS10")
    metrics["yield_curve_2s10s"] = safe_call(fetch_fred_series, "T10Y2Y")
    metrics["hy_credit_spread"] = safe_call(fetch_fred_series, "BAMLH0A0HYM2")
    metrics["real_yield_10y"] = safe_call(fetch_fred_series, "DFII10")

    # E. Dólar & Risco
    metrics["dxy_index"] = safe_call(fetch_yfinance, "DX-Y.NYB")
    metrics["fed_swap_lines"] = safe_call(fetch_fred_series, "SWPT")
    metrics["vix_index"] = safe_call(fetch_yfinance, "^VIX")
    metrics["move_index"] = safe_call(fetch_yfinance, "^MOVE")
    metrics["gold_price"] = safe_call(fetch_yfinance, "GC=F")

    # F. Liquidez Cripto
    metrics["stablecoin_supply"] = safe_call(fetch_stablecoin_supply)
    metrics["btc_etf_netflow"] = safe_call(fetch_btc_etf_netflow)
    metrics["btc_funding_rate"] = safe_call(fetch_okx_funding_rate)
    metrics["btc_open_interest"] = safe_call(fetch_okx_open_interest)
    metrics["fear_greed_index"] = safe_call(fetch_fear_greed)

    return metrics


def main():
    metrics = build_metrics()
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "metrics": {k: v for k, v in metrics.items() if v is not None},
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    ok = len(payload["metrics"])
    total = len(metrics)
    print(f"[OK] data_live.json gravado — {ok}/{total} indicadores obtidos com sucesso.")


if __name__ == "__main__":
    main()
