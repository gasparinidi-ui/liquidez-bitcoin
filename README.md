# Liquidez BTC · GDI

Site estático (custo zero) que reúne os **30 principais indicadores de liquidez
global** com maior influência histórica sobre a cotação do Bitcoin, organizados
em 6 categorias e atualizados automaticamente por um pipeline gratuito.

## Estrutura

```
liquidez-bitcoin/
├── design/gdi.css              ← design system GDI (autocontido)
├── shared/                     ← reservado para navbar.js do portal, se for anexar a um portal maior
├── assets/
│   ├── indicators.js           ← metadado dos 30 indicadores (nomes, unidades, fontes)
│   └── data_loader.js          ← busca data_live.json e injeta valores no DOM
├── scripts/
│   ├── data_collector.py       ← coleta os 30 indicadores nas fontes gratuitas
│   └── requirements.txt
├── .github/workflows/update-data.yml   ← roda o coletor de hora em hora
├── data_live.json              ← gerado automaticamente (placeholder incluso)
├── index.html                  ← visão geral (tabela mestre com os 30 indicadores)
├── bancos-centrais.html        ← 7 indicadores
├── agregados-globais.html      ← 3 indicadores
├── oferta-moeda.html           ← 4 indicadores
├── juros-credito.html          ← 6 indicadores
├── dolar-risco.html            ← 5 indicadores
├── liquidez-cripto.html        ← 5 indicadores
└── fontes.html                 ← fontes e metodologia completas
```

## Os 30 indicadores

| # | Categoria | Indicador | Fonte |
|---|---|---|---|
| 1 | Bancos Centrais | Balanço do Fed (WALCL) | FRED |
| 2 | Bancos Centrais | Liquidez Líquida do Fed | Calculado |
| 3 | Bancos Centrais | Reverse Repo (RRP) | FRED |
| 4 | Bancos Centrais | Treasury General Account | FRED |
| 5 | Bancos Centrais | Balanço do BCE | FRED |
| 6 | Bancos Centrais | Balanço do BoJ | FRED |
| 7 | Bancos Centrais | Balanço do PBoC | Manual |
| 8 | Agregados Globais | Global Liquidity Index (GLI) | Calculado |
| 9 | Agregados Globais | M2 Global G4 | Calculado |
| 10 | Agregados Globais | Credit Impulse Global | BIS |
| 11 | Oferta de Moeda | M2 EUA | FRED |
| 12 | Oferta de Moeda | M3 Zona do Euro | ECB SDW |
| 13 | Oferta de Moeda | M2 China | Manual |
| 14 | Oferta de Moeda | M2 Japão | FRED |
| 15 | Juros & Crédito | Fed Funds Rate | FRED |
| 16 | Juros & Crédito | SOFR | FRED |
| 17 | Juros & Crédito | Treasury 10 anos | FRED |
| 18 | Juros & Crédito | Curva 2s10s | FRED |
| 19 | Juros & Crédito | Spread High Yield | FRED |
| 20 | Juros & Crédito | Yield Real 10 anos | FRED |
| 21 | Dólar & Risco | DXY | Yahoo Finance |
| 22 | Dólar & Risco | Swap Lines USD do Fed | FRED |
| 23 | Dólar & Risco | VIX | Yahoo Finance |
| 24 | Dólar & Risco | MOVE Index | Yahoo Finance |
| 25 | Dólar & Risco | Ouro | Yahoo Finance |
| 26 | Liquidez Cripto | Supply de Stablecoins | DefiLlama |
| 27 | Liquidez Cripto | Fluxo Líquido ETFs Spot BTC | Farside Investors |
| 28 | Liquidez Cripto | Funding Rate Médio | Bybit |
| 29 | Liquidez Cripto | Open Interest Futuros BTC | Bybit |
| 30 | Liquidez Cripto | Fear & Greed Cripto | Alternative.me |

**Nota sobre indicadores marcados "Manual"/"Calculado":** balanço do PBoC, M2
China, GLI, M2 Global G4 e Credit Impulse (BIS) não têm API JSON gratuita
simples e confiável. O script já traz a estrutura pronta — basta completar as
funções correspondentes em `data_collector.py` (ver comentários no código) ou
atualizar manualmente via download CSV do BIS/ECB a cada mês.

## Como publicar (passo a passo)

1. **Crie um repositório público no GitHub** e suba esta pasta inteira.
2. **Obtenha uma chave gratuita do FRED**: https://fredaccount.stlouisfed.org/apikeys
   (aprovação instantânea, sem custo).
3. No repositório: **Settings → Secrets and variables → Actions** → New repository secret
   → nome `FRED_API_KEY`, valor = sua chave.
4. O workflow `.github/workflows/update-data.yml` já está configurado para
   rodar **de hora em hora** (`cron: '5 * * * *'`) e commitar `data_live.json`
   automaticamente. Pode reduzir para `*/15 * * * *` (a cada 15 min) sem custo,
   já que repositórios públicos têm minutos ilimitados no GitHub Actions.
5. **Conecte o repositório à Vercel** (ou Netlify / Cloudflare Pages / GitHub
   Pages) — qualquer plano gratuito serve, já que o site é 100% estático.
   Cada commit do Actions dispara um novo deploy automaticamente.

## Rodar localmente

```bash
cd scripts
pip install -r requirements.txt
export FRED_API_KEY=sua_chave_aqui
python data_collector.py
# gera/atualiza ../data_live.json
```

Depois é só abrir `index.html` num servidor local (ex: `python -m http.server`)
para ver os dados carregados — abrir via `file://` direto bloqueia o `fetch()`
do `data_loader.js` em alguns navegadores.

## Aviso

Conteúdo puramente informativo. Não constitui recomendação de investimento.
