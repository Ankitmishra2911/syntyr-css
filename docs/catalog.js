/* Optional documentation-only enhancement. Syntyr CSS requires no JavaScript. */
(() => {
  'use strict';
  const search = document.getElementById('catalog-search');
  const controls = document.getElementById('catalog-controls');
  const results = document.getElementById('catalog-results');
  const filters = document.getElementById('catalog-filters');
  const empty = document.getElementById('catalog-empty');
  const cards = [...document.querySelectorAll('.catalog-card')];
  if (!search || !controls || !filters || !results || !empty || !cards.length) return;

  const filterButtons = [...filters.querySelectorAll('[data-catalog-filter]')];
  let activeCategory = 'all';
  const searchable = cards.map((card) => ({
    card,
    terms: `${card.querySelector('h2')?.textContent || ''} ${card.dataset.catalogCategory || ''} ${card.dataset.catalogKeywords || ''} ${card.querySelector('.syn-badge')?.textContent || ''} ${card.querySelector('.syn-muted')?.textContent || ''}`.toLocaleLowerCase(),
  }));

  function updateResults() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const {card, terms: text} of searchable) {
      const matchesCategory = activeCategory === 'all' || card.dataset.catalogCategory === activeCategory;
      const match = matchesCategory && terms.every((term) => text.includes(term));
      card.hidden = !match;
      if (match) count += 1;
    }
    empty.hidden = count !== 0;
    results.textContent = `Showing ${count} of ${cards.length} examples.`;
  }

  controls.hidden = false;
  filters.hidden = false;
  for (const button of filterButtons) {
    button.addEventListener('click', () => {
      activeCategory = button.dataset.catalogFilter;
      for (const option of filterButtons) option.setAttribute('aria-pressed', String(option === button));
      updateResults();
    });
  }
  search.addEventListener("input", updateResults);
  updateResults();

  for (const card of cards) {
    const button = card.querySelector('[data-catalog-copy]');
    const code = card.querySelector('.catalog-source code');
    if (!button || !code) continue;
    button.hidden = false;
    button.addEventListener('click', async () => {
      const value = code.textContent.trim();
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard API unavailable');
        await navigator.clipboard.writeText(value);
        results.textContent = `${card.querySelector('h2').textContent} HTML copied.`;
      } catch {
        code.closest('details').open = true;
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection?.removeAllRanges();
        selection?.addRange(range);
        results.textContent = 'HTML selected. Use your keyboard to copy it.';
      }
    });
  }
})();
