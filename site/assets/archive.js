const toolbar = document.querySelector("#toolbar");
const buttons = [...toolbar.querySelectorAll("[data-filter]")];
const search = document.querySelector("#search");
const count = document.querySelector("#result-count");
const emptyState = document.querySelector("#empty-state");
const emptyTitle = document.querySelector("#empty-title");
const emptyDescription = document.querySelector("#empty-description");
const reports = [...document.querySelectorAll("#report-list > li")].map((row) => ({
  row,
  type: row.dataset.kind,
  text: normalize(`${row.querySelector("h3").textContent} ${row.querySelector(".report-type").textContent}`),
}));

function normalize(text) {
  return text.normalize("NFKC").trim().toLocaleLowerCase();
}

function updateResults() {
  const type = buttons.find((button) => button.getAttribute("aria-pressed") === "true").dataset.filter;
  const terms = normalize(search.value).split(/\s+/).filter(Boolean);
  let visibleCount = 0;

  for (const report of reports) {
    const typeMatches = type === "all" || report.type === type;
    const searchMatches = terms.every((term) => report.text.includes(term));
    report.row.hidden = !(typeMatches && searchMatches);
    if (!report.row.hidden) visibleCount += 1;
  }

  count.textContent = `${visibleCount} ${visibleCount === 1 ? "document" : "documents"}`;
  emptyState.hidden = visibleCount !== 0;

  if (visibleCount === 0) {
    emptyTitle.textContent = "No matching documents";
    emptyDescription.textContent = "Try another search or document type.";
  }
}

for (const button of buttons) {
  button.addEventListener("click", () => {
    for (const filter of buttons) {
      filter.setAttribute("aria-pressed", String(filter === button));
    }
    updateResults();
  });
}

search.addEventListener("input", updateResults);
toolbar.hidden = reports.length === 0;
