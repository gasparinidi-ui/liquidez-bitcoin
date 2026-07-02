/**
 * LIQUIDEZ BTC · GDI
 * Registro central dos 30 indicadores de liquidez global que mais
 * influenciam o Bitcoin. Cada objeto define o id usado como chave em
 * data_live.json (gerado pelo GitHub Actions), o rótulo, unidade,
 * categoria e a fonte gratuita de dados.
 *
 * Este arquivo é apenas metadado / referência de UI — os valores reais
 * são injetados em runtime pelo assets/data_loader.js a partir de
 * data_live.json.
 */
const INDICATORS = [
  // ── A. LIQUIDEZ DE BANCOS CENTRAIS (7) ──────────────────────────
  { id: 'fed_balance_sheet', name: 'Balanço do Fed (WALCL)', cat: 'bancos-centrais', unit: 'US$ tri', source: 'FRED · WALCL', freq: 'Semanal' },
  { id: 'fed_net_liquidity', name: 'Liquidez Líquida do Fed', desc: 'WALCL − TGA − RRP', cat: 'bancos-centrais', unit: 'US$ tri', source: 'FRED (calculado)', freq: 'Semanal' },
  { id: 'reverse_repo', name: 'Reverse Repo (RRP)', cat: 'bancos-centrais', unit: 'US$ bi', source: 'FRED · RRPONTSYD', freq: 'Diária' },
  { id: 'tga_balance', name: 'Treasury General Account (TGA)', cat: 'bancos-centrais', unit: 'US$ bi', source: 'FRED · WTREGEN', freq: 'Semanal' },
  { id: 'ecb_balance_sheet', name: 'Balanço do BCE', cat: 'bancos-centrais', unit: 'US$ tri', source: 'FRED · ECBASSETSW', freq: 'Semanal' },
  { id: 'boj_balance_sheet', name: 'Balanço do BoJ', cat: 'bancos-centrais', unit: 'US$ tri', source: 'FRED · JPNASSETS', freq: 'Mensal' },
  { id: 'pboc_balance_sheet', name: 'Balanço do PBoC', cat: 'bancos-centrais', unit: 'US$ tri', source: 'PBoC / manual', freq: 'Mensal' },

  // ── B. AGREGADOS GLOBAIS (3) ─────────────────────────────────────
  { id: 'gli_index', name: 'Global Liquidity Index (GLI)', desc: 'Soma dos 5 maiores balanços de BC em USD', cat: 'agregados-globais', unit: 'US$ tri', source: 'Calculado (Fed+BCE+BoJ+PBoC+BoE)', freq: 'Semanal' },
  { id: 'm2_global_g4', name: 'M2 Global G4', desc: 'EUA+China+Zona do Euro+Japão, ponderado por PIB', cat: 'agregados-globais', unit: 'US$ tri', source: 'Calculado (FRED+ECB+BoJ+PBoC)', freq: 'Mensal' },
  { id: 'bis_credit_impulse', name: 'Credit Impulse Global (BIS)', cat: 'agregados-globais', unit: '% PIB', source: 'BIS Data Portal', freq: 'Trimestral' },

  // ── C. OFERTA DE MOEDA POR REGIÃO (4) ────────────────────────────
  { id: 'us_m2', name: 'M2 Estados Unidos', cat: 'oferta-moeda', unit: 'US$ tri', source: 'FRED · M2SL', freq: 'Mensal' },
  { id: 'eurozone_m3', name: 'M3 Zona do Euro', cat: 'oferta-moeda', unit: 'EUR tri', source: 'ECB SDW · BSI.M.U2.Y.V.M30.X.1', freq: 'Mensal' },
  { id: 'china_m2', name: 'M2 China', cat: 'oferta-moeda', unit: 'CNY tri', source: 'PBoC / FRED (proxy)', freq: 'Mensal' },
  { id: 'japan_m2', name: 'M2 Japão', cat: 'oferta-moeda', unit: 'JPY tri', source: 'FRED · MYAGM2JPM189S', freq: 'Mensal' },

  // ── D. JUROS E CONDIÇÕES DE CRÉDITO (6) ──────────────────────────
  { id: 'fed_funds_rate', name: 'Fed Funds Rate', cat: 'juros-credito', unit: '%', source: 'FRED · FEDFUNDS', freq: 'Diária' },
  { id: 'sofr_rate', name: 'SOFR', cat: 'juros-credito', unit: '%', source: 'FRED · SOFR', freq: 'Diária' },
  { id: 'ust10y', name: 'Treasury 10 anos', cat: 'juros-credito', unit: '%', source: 'FRED · DGS10', freq: 'Diária' },
  { id: 'yield_curve_2s10s', name: 'Curva de Juros 2s10s', cat: 'juros-credito', unit: 'p.p.', source: 'FRED · T10Y2Y', freq: 'Diária' },
  { id: 'hy_credit_spread', name: 'Spread de Crédito High Yield', cat: 'juros-credito', unit: 'p.p.', source: 'FRED · BAMLH0A0HYM2', freq: 'Diária' },
  { id: 'real_yield_10y', name: 'Yield Real 10 anos (TIPS)', cat: 'juros-credito', unit: '%', source: 'FRED · DFII10', freq: 'Diária' },

  // ── E. DÓLAR E APETITE POR RISCO (5) ─────────────────────────────
  { id: 'dxy_index', name: 'Índice DXY (Dólar)', cat: 'dolar-risco', unit: 'pts', source: 'Yahoo Finance · DX-Y.NYB', freq: 'Intradiária' },
  { id: 'fed_swap_lines', name: 'Linhas de Swap USD do Fed', cat: 'dolar-risco', unit: 'US$ bi', source: 'FRED · SWPT', freq: 'Semanal' },
  { id: 'vix_index', name: 'VIX (Volatilidade S&P)', cat: 'dolar-risco', unit: 'pts', source: 'Yahoo Finance · ^VIX', freq: 'Intradiária' },
  { id: 'move_index', name: 'MOVE Index (Volatilidade Treasuries)', cat: 'dolar-risco', unit: 'pts', source: 'Yahoo Finance · ^MOVE', freq: 'Intradiária' },
  { id: 'gold_price', name: 'Ouro (XAU/USD)', cat: 'dolar-risco', unit: 'US$/oz', source: 'Yahoo Finance · GC=F', freq: 'Intradiária' },

  // ── F. LIQUIDEZ ESPECÍFICA DE CRIPTO (5) ─────────────────────────
  { id: 'stablecoin_supply', name: 'Supply Total de Stablecoins', cat: 'liquidez-cripto', unit: 'US$ bi', source: 'DefiLlama API', freq: 'Diária' },
  { id: 'btc_etf_netflow', name: 'Fluxo Líquido ETFs Spot BTC', cat: 'liquidez-cripto', unit: 'US$ mi/dia', source: 'Farside Investors', freq: 'Diária' },
  { id: 'btc_funding_rate', name: 'Funding Rate Médio (Perpétuos BTC)', cat: 'liquidez-cripto', unit: '% (8h)', source: 'Bybit Public API', freq: 'A cada 8h' },
  { id: 'btc_open_interest', name: 'Open Interest Futuros BTC', cat: 'liquidez-cripto', unit: 'US$ bi', source: 'Bybit Public API', freq: 'Horária' },
  { id: 'fear_greed_index', name: 'Índice Fear & Greed Cripto', cat: 'liquidez-cripto', unit: '0-100', source: 'Alternative.me API', freq: 'Diária' },
];

const CATEGORIES = [
  { key: 'bancos-centrais', label: 'Bancos Centrais', page: 'bancos-centrais.html', icon: '🏛️' },
  { key: 'agregados-globais', label: 'Agregados Globais', page: 'agregados-globais.html', icon: '🌐' },
  { key: 'oferta-moeda', label: 'Oferta de Moeda', page: 'oferta-moeda.html', icon: '💵' },
  { key: 'juros-credito', label: 'Juros & Crédito', page: 'juros-credito.html', icon: '📈' },
  { key: 'dolar-risco', label: 'Dólar & Risco', page: 'dolar-risco.html', icon: '⚖️' },
  { key: 'liquidez-cripto', label: 'Liquidez Cripto', page: 'liquidez-cripto.html', icon: '₿' },
];
