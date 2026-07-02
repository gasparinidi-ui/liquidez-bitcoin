import os

SIDEBAR_LINKS = [
    ("index.html", "overview", "Visão Geral"),
    ("bancos-centrais.html", "bancos-centrais", "🏛️ Bancos Centrais"),
    ("agregados-globais.html", "agregados-globais", "🌐 Agregados Globais"),
    ("oferta-moeda.html", "oferta-moeda", "💵 Oferta de Moeda"),
    ("juros-credito.html", "juros-credito", "📈 Juros &amp; Crédito"),
    ("dolar-risco.html", "dolar-risco", "⚖️ Dólar &amp; Risco"),
    ("liquidez-cripto.html", "liquidez-cripto", "₿ Liquidez Cripto"),
    ("fontes.html", "fontes", "📚 Fontes &amp; Metodologia"),
]

def nav_html(active):
    lines = []
    for href, key, label in SIDEBAR_LINKS:
        cls = ' class="active"' if key == active else ''
        lines.append(f'        <a href="./{href}" data-nav="{key}"{cls}>{label}</a>')
    return "\n".join(lines)

def card_html(title, metric_id, unit):
    return f'''      <div class="card">
        <h3>{title}</h3>
        <div class="metric" data-metric="{metric_id}" data-unit="{unit}"><span data-field="value">—</span></div>
        <div class="delta neu" data-field="delta">—</div>
      </div>'''

def method_row(name, source, freq):
    return f'              <tr><td>{name}</td><td><span class="source-pill">{source}</span></td><td>{freq}</td></tr>'

def page(active, icon, title, intro, chips, cards, method_rows, notes):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Liquidez BTC · GDI</title>
<link rel="stylesheet" href="./design/gdi.css">
<style>
  .layout{{ min-height:100vh; }}
  .sidebar{{ position:sticky; top:0; height:100vh; }}
</style>
</head>
<body data-page="{active}">

<div class="layout">
  <aside class="sidebar">
    <div class="nav-group">
      <div class="brand">
        <div class="brand-badge">₿</div>
        <div><h1>Liquidez BTC</h1><p>30 indicadores globais · GDI</p></div>
      </div>
    </div>
    <div class="nav-group">
      <div class="nav-title">Painéis</div>
      <nav class="nav">
{nav_html(active)}
      </nav>
    </div>
    <div class="nav-group">
      <div class="nav-title">Status</div>
      <div class="notice">Atualizado: <strong id="last-update">carregando…</strong></div>
    </div>
  </aside>

  <main class="main">
    <div class="page-hero">
      <div>
        <h2>{icon} {title}</h2>
        <p>{intro}</p>
        <div class="meta-row">
{chips}
        </div>
      </div>
    </div>

    <div class="card-grid">
{cards}
    </div>

    <div class="section" style="padding:0;">
      <div class="panel">
        <h4>Metodologia e fontes</h4>
        <p class="small">{notes}</p>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Indicador</th><th>Fonte</th><th>Frequência</th></tr></thead>
            <tbody>
{method_rows}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="footer-inner">Liquidez BTC · GDI</div>
  </main>
</div>

<script src="./assets/indicators.js"></script>
<script src="./assets/data_loader.js"></script>
</body>
</html>
'''

OUT_DIR = "/home/claude/liquidez-bitcoin"

# ── AGREGADOS GLOBAIS ────────────────────────────────────────────
cards = "\n".join([
    card_html("Global Liquidity Index (GLI)", "gli_index", "US$ tri"),
    card_html("M2 Global G4", "m2_global_g4", "US$ tri"),
    card_html("Credit Impulse Global (BIS)", "bis_credit_impulse", "% PIB"),
])
rows = "\n".join([
    method_row("GLI", "Calculado (Fed+BCE+BoJ+PBoC+BoE)", "Semanal"),
    method_row("M2 Global G4", "Calculado (FRED+ECB+BoJ+PBoC)", "Mensal"),
    method_row("Credit Impulse Global", "BIS Data Portal", "Trimestral"),
])
chips = '          <span class="chip">3 indicadores</span>\n          <span class="chip">Índices agregados</span>'
html = page(
    "agregados-globais", "🌐", "Agregados Globais",
    "Índices que somam ou ponderam a liquidez de todos os grandes bancos centrais em uma única série — a visão de topo do ciclo de liquidez mundial, com correlação histórica de 0.8–0.9 com Bitcoin em fases de expansão.",
    chips, cards, rows,
    "O GLI soma os balanços dos cinco maiores bancos centrais convertidos para USD. O M2 Global G4 pondera a oferta de moeda de EUA, China, Zona do Euro e Japão pelo peso do PIB de cada bloco (fonte: IMF WEO). O Credit Impulse mede a variação do crédito novo como % do PIB global."
)
with open(os.path.join(OUT_DIR, "agregados-globais.html"), "w") as f:
    f.write(html)

# ── OFERTA DE MOEDA ──────────────────────────────────────────────
cards = "\n".join([
    card_html("M2 Estados Unidos", "us_m2", "US$ tri"),
    card_html("M3 Zona do Euro", "eurozone_m3", "EUR tri"),
    card_html("M2 China", "china_m2", "CNY tri"),
    card_html("M2 Japão", "japan_m2", "JPY tri"),
])
rows = "\n".join([
    method_row("M2 EUA", "FRED · M2SL", "Mensal"),
    method_row("M3 Zona do Euro", "ECB SDW · BSI.M.U2.Y.V.M30.X.1", "Mensal"),
    method_row("M2 China", "PBoC / FRED (proxy)", "Mensal"),
    method_row("M2 Japão", "FRED · MYAGM2JPM189S", "Mensal"),
])
chips = '          <span class="chip">4 indicadores</span>\n          <span class="chip">Atualização mensal</span>'
html = page(
    "oferta-moeda", "💵", "Oferta de Moeda",
    "Quanto dinheiro efetivamente circula em cada bloco econômico. Historicamente, picos de crescimento do M2 global antecedem em 2-3 meses os principais rallies de Bitcoin.",
    chips, cards, rows,
    "Séries em moeda local, sem conversão cambial (ver página de Dólar &amp; Risco para o câmbio). China e Japão têm defasagem de publicação maior que EUA e Zona do Euro."
)
with open(os.path.join(OUT_DIR, "oferta-moeda.html"), "w") as f:
    f.write(html)

# ── JUROS E CRÉDITO ──────────────────────────────────────────────
cards = "\n".join([
    card_html("Fed Funds Rate", "fed_funds_rate", "%"),
    card_html("SOFR", "sofr_rate", "%"),
    card_html("Treasury 10 anos", "ust10y", "%"),
    card_html("Curva de Juros 2s10s", "yield_curve_2s10s", "p.p."),
    card_html("Spread High Yield", "hy_credit_spread", "p.p."),
    card_html("Yield Real 10 anos (TIPS)", "real_yield_10y", "%"),
])
rows = "\n".join([
    method_row("Fed Funds Rate", "FRED · FEDFUNDS", "Diária"),
    method_row("SOFR", "FRED · SOFR", "Diária"),
    method_row("Treasury 10 anos", "FRED · DGS10", "Diária"),
    method_row("Curva 2s10s", "FRED · T10Y2Y", "Diária"),
    method_row("Spread High Yield", "FRED · BAMLH0A0HYM2", "Diária"),
    method_row("Yield Real 10 anos", "FRED · DFII10", "Diária"),
])
chips = '          <span class="chip">6 indicadores</span>\n          <span class="chip">Atualização diária</span>'
html = page(
    "juros-credito", "📈", "Juros &amp; Crédito",
    "O custo do dinheiro. Juros reais em queda e spreads de crédito comprimindo sinalizam apetite por risco — historicamente favorável para Bitcoin. Curva invertida costuma preceder estresse de liquidez.",
    chips, cards, rows,
    "Todas as séries em pontos percentuais (%) ou pontos-percentuais de spread (p.p.), publicadas diariamente pelo Federal Reserve Economic Data (FRED)."
)
with open(os.path.join(OUT_DIR, "juros-credito.html"), "w") as f:
    f.write(html)

# ── DÓLAR & RISCO ─────────────────────────────────────────────────
cards = "\n".join([
    card_html("Índice DXY (Dólar)", "dxy_index", "pts"),
    card_html("Linhas de Swap USD do Fed", "fed_swap_lines", "US$ bi"),
    card_html("VIX", "vix_index", "pts"),
    card_html("MOVE Index", "move_index", "pts"),
    card_html("Ouro (XAU/USD)", "gold_price", "US$/oz"),
])
rows = "\n".join([
    method_row("DXY", "Yahoo Finance · DX-Y.NYB", "Intradiária"),
    method_row("Swap Lines Fed", "FRED · SWPT", "Semanal"),
    method_row("VIX", "Yahoo Finance · ^VIX", "Intradiária"),
    method_row("MOVE Index", "Yahoo Finance · ^MOVE", "Intradiária"),
    method_row("Ouro", "Yahoo Finance · GC=F", "Intradiária"),
])
chips = '          <span class="chip">5 indicadores</span>\n          <span class="chip">Intradiário</span>'
html = page(
    "dolar-risco", "⚖️", "Dólar &amp; Risco",
    "A força do dólar é o driver mais consistente e persistente de liquidez global — cerca de 64% da dívida mundial é denominada em USD. Um DXY em queda historicamente coincide com apreciação de Bitcoin.",
    chips, cards, rows,
    "VIX e MOVE são termômetros de volatilidade implícita (ações e Treasuries, respectivamente); leituras baixas indicam maior apetite por risco. O ouro serve como referência de fluxo para ativos de reserva de valor."
)
with open(os.path.join(OUT_DIR, "dolar-risco.html"), "w") as f:
    f.write(html)

# ── LIQUIDEZ CRIPTO ──────────────────────────────────────────────
cards = "\n".join([
    card_html("Supply Total de Stablecoins", "stablecoin_supply", "US$ bi"),
    card_html("Fluxo Líquido ETFs Spot BTC", "btc_etf_netflow", "US$ mi/dia"),
    card_html("Funding Rate Médio (Perpétuos)", "btc_funding_rate", "% (8h)"),
    card_html("Open Interest Futuros BTC", "btc_open_interest", "US$ bi"),
    card_html("Índice Fear &amp; Greed Cripto", "fear_greed_index", "0-100"),
])
rows = "\n".join([
    method_row("Supply de Stablecoins", "DefiLlama API", "Diária"),
    method_row("Fluxo ETFs Spot BTC", "Farside Investors", "Diária"),
    method_row("Funding Rate", "Bybit Public API", "A cada 8h"),
    method_row("Open Interest", "Bybit Public API", "Horária"),
    method_row("Fear &amp; Greed", "Alternative.me API", "Diária"),
])
chips = '          <span class="chip">5 indicadores</span>\n          <span class="chip">O canal mais direto</span>'
html = page(
    "liquidez-cripto", "₿", "Liquidez Cripto",
    "A liquidez macro chega ao Bitcoin através destes canais diretos: cunhagem de stablecoins, fluxo de ETFs spot, alavancagem em derivativos e sentimento de mercado. É aqui que a liquidez global vira compra ou venda real de BTC.",
    chips, cards, rows,
    "Funding rate e open interest são médias dos principais pares perpétuos de BTC. O supply de stablecoins agrega USDT, USDC, DAI e demais dólares tokenizados — um proxy direto de \"pólvora seca\" disponível para compra de cripto."
)
with open(os.path.join(OUT_DIR, "liquidez-cripto.html"), "w") as f:
    f.write(html)

print("5 páginas de categoria geradas com sucesso.")
