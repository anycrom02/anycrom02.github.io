'use strict';
// Master selection-record explorer. Progressive enhancement keeps all records readable without JS.
const explorerCards = [...document.querySelectorAll('.explorer-card')];
const cohortSelect = document.querySelector('#cohort-select');
const explorerField = document.querySelector('#explorer-field');
const companySearch = document.querySelector('#company-search');
const showCompanies = document.querySelector('#show-companies');
let recordLimit = 12;
function renderExplorer(reset = false) {
  if (!explorerCards.length) return;
  if (reset) recordLimit = 12;
  const term = companySearch.value.trim().toLocaleLowerCase('ko');
  const matching = explorerCards.filter(card => (cohortSelect.value === 'all' || card.dataset.cohort === cohortSelect.value) && (explorerField.value === 'all' || card.dataset.field === explorerField.value) && card.dataset.name.toLocaleLowerCase('ko').includes(term));
  explorerCards.forEach(card => { card.hidden = true; });
  matching.slice(0, recordLimit).forEach(card => { card.hidden = false; });
  document.querySelector('#explorer-status').textContent = `${matching.length}개 선정기록 · ${Math.min(recordLimit,matching.length)}개 표시`;
  showCompanies.hidden = matching.length <= recordLimit;
}
if (explorerCards.length) {
  cohortSelect.addEventListener('change', () => renderExplorer(true));
  explorerField.addEventListener('change', () => renderExplorer(true));
  companySearch.addEventListener('input', () => renderExplorer(true));
  showCompanies.addEventListener('click', () => { recordLimit += 12; renderExplorer(); });
  renderExplorer();
}
document.querySelectorAll('.rank-bar').forEach(bar => {
  const update = () => { document.querySelector('#rank-detail').textContent = bar.getAttribute('aria-label'); };
  bar.addEventListener('pointerenter', update);
  bar.addEventListener('focus', update);
  bar.addEventListener('click', update);
});
// Optional enhancements only: no fetch, imports, analytics, external libraries or remote requests.
const fieldSelect = document.querySelector('#field-filter');
const points = [...document.querySelectorAll('#scatter-chart .company-dot')];
const statusText = document.querySelector('#filter-status');
const detail = document.querySelector('#point-detail');
if (fieldSelect) fieldSelect.addEventListener('change', () => {
  const field = fieldSelect.value;
  points.forEach(point => { point.style.display = field === 'all' || point.dataset.field === field ? '' : 'none'; });
  // Desktop and mobile SVG contain the same values; count one SVG only.
  const visible = document.querySelectorAll('#scatter-chart .chart-desktop .company-dot:not([style*="none"])').length;
  statusText.textContent = `${visible}개 기업`;
  detail.textContent = '기존 기업별 EDA 값을 선택한 선정분야로 표시합니다. 전체 수치는 아래 표에서 확인할 수 있습니다.';
});
points.forEach(point => {
  const show = () => { detail.textContent = point.getAttribute('aria-label'); };
  point.addEventListener('mouseenter', show);
  point.addEventListener('focus', show);
  point.addEventListener('click', show);
});
if ('IntersectionObserver' in window) {
  const navLinks = [...document.querySelectorAll('.site-head nav a')];
  const observer = new IntersectionObserver(entries => {
    const first = entries.find(entry => entry.isIntersecting);
    if (first) navLinks.forEach(link => {
      if (link.hash === `#${first.target.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin: '-12% 0px -65% 0px'});
  navLinks.forEach(link => { const section = document.querySelector(link.hash); if (section) observer.observe(section); });
}
