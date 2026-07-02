/**
 * LIQUIDEZ BTC · GDI — data_loader.js
 * Busca data_live.json (gerado pelo GitHub Actions a cada execução do
 * scripts/data_collector.py) e substitui os placeholders "—" nos
 * elementos com atributo data-metric="<id_do_indicador>".
 *
 * Estrutura esperada de data_live.json:
 * {
 *   "updated_at": "2026-07-02T14:00:00Z",
 *   "metrics": {
 *     "fed_balance_sheet": { "value": 7.21, "unit": "US$ tri", "change_pct": -0.4, "as_of": "2026-06-25" },
 *     ...
 *   }
 * }
 *
 * Caminho relativo: ajuste DATA_URL conforme a profundidade da página.
 * Raiz do site        -> "./data_live.json"
 * Sem subpastas extras -> mesmo arquivo serve todas as páginas
 */
(function () {
  'use strict';

  const DATA_URL = './data_live.json';

  function fmtNumber(v) {
    if (v === null || v === undefined || Number.isNaN(v)) return '—';
    const abs = Math.abs(v);
    if (abs >= 1000) return v.toLocaleString('pt-BR', { maximumFractionDigits: 0 });
    if (abs >= 10) return v.toLocaleString('pt-BR', { maximumFractionDigits: 1 });
    return v.toLocaleString('pt-BR', { maximumFractionDigits: 2 });
  }

  function applyMetric(el, metric) {
    if (!metric) return;
    const valueEl = el.querySelector('[data-field="value"]') || el;
    const deltaEl = el.querySelector('[data-field="delta"]');
    const asOfEl = el.querySelector('[data-field="as_of"]');

    if (valueEl) {
      const unit = el.getAttribute('data-unit') || '';
      valueEl.textContent = `${fmtNumber(metric.value)}${unit ? ' ' + unit : ''}`;
    }
    if (deltaEl && typeof metric.change_pct === 'number') {
      const sign = metric.change_pct > 0 ? '+' : '';
      deltaEl.textContent = `${sign}${metric.change_pct.toFixed(2)}%`;
      deltaEl.classList.remove('pos', 'neg', 'neu');
      deltaEl.classList.add(metric.change_pct > 0 ? 'pos' : metric.change_pct < 0 ? 'neg' : 'neu');
    }
    if (asOfEl && metric.as_of) {
      asOfEl.textContent = metric.as_of;
    }
  }

  async function loadData() {
    try {
      const res = await fetch(DATA_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error('data_live.json indisponível (' + res.status + ')');
      const data = await res.json();

      document.querySelectorAll('[data-metric]').forEach((el) => {
        const id = el.getAttribute('data-metric');
        applyMetric(el, data.metrics ? data.metrics[id] : null);
      });

      const stamp = document.getElementById('last-update');
      if (stamp && data.updated_at) {
        const d = new Date(data.updated_at);
        stamp.textContent = d.toLocaleString('pt-BR', {
          timeZone: 'America/Campo_Grande',
          day: '2-digit', month: '2-digit', year: 'numeric',
          hour: '2-digit', minute: '2-digit',
        }) + ' (Campo Grande)';
      }
    } catch (err) {
      console.warn('[LIQUIDEZ BTC] Falha ao carregar dados ao vivo:', err);
      const stamp = document.getElementById('last-update');
      if (stamp) stamp.textContent = 'dados ao vivo indisponíveis — exibindo placeholders';
    }
  }

  document.addEventListener('DOMContentLoaded', loadData);
})();
