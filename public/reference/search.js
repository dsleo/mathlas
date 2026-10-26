const $ = id => document.getElementById(id);
const input = $('query'), status = $('search-status'), period = $('period'), tier = $('tier');
const sections = [...document.querySelectorAll('.field-section')];
let index = null;

const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();

function apply() {
  const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
  const [lo, hi] = period.value ? period.value.split(',').map(Number) : [-Infinity, Infinity];
  let visible = 0;
  for (const section of sections) {
    const fieldMatches = terms.every(t => normalize(section.dataset.search || '').includes(t));
    let sectionVisible = 0;
    for (const row of section.querySelectorAll('.event-row')) {
      const text = normalize(index?.[row.dataset.pid] || row.dataset.search || '');
      const y = +row.dataset.y;
      const matches = (fieldMatches || terms.every(t => text.includes(t))) && y >= lo && y <= hi && (!tier.value || row.dataset.tier === tier.value);
      row.hidden = !matches;
      if (matches) sectionVisible++;
    }
    section.hidden = sectionVisible === 0;
    visible += sectionVisible;
  }
  status.textContent = terms.length || period.value || tier.value ? `${visible} ${visible === 1 ? 'event' : 'events'} found` : '';
}

// The full-text index is ~MBs: fetch it on first use, not on page load.
function load() {
  if (index !== null) return;
  index = {};
  fetch('search-index.json').then(r => r.json()).then(j => { index = j; apply(); }).catch(() => {});
}
input?.addEventListener('focus', load);
input?.addEventListener('input', () => { load(); apply(); });
period?.addEventListener('change', apply);
tier?.addEventListener('change', apply);
