const input = document.getElementById('query');
const status = document.getElementById('search-status');
const sections = [...document.querySelectorAll('.field-section')];

function normalize(value) {
  return value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
}

input?.addEventListener('input', () => {
  const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const section of sections) {
    const fieldMatches = terms.every(term => normalize(section.dataset.search || '').includes(term));
    let sectionVisible = 0;
    for (const row of section.querySelectorAll('.event-row')) {
      const matches = fieldMatches || terms.every(term => normalize(row.dataset.search || '').includes(term));
      row.hidden = !matches;
      if (matches) sectionVisible++;
    }
    section.hidden = sectionVisible === 0;
    visible += sectionVisible;
  }
  status.textContent = terms.length ? `${visible} ${visible === 1 ? 'event' : 'events'} found` : '';
});
