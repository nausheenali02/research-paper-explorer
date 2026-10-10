
const queryInput = document.getElementById("research-query");
const researchBtn = document.getElementById("research-btn");
const resultsSection = document.getElementById("results");
const resultsContent = document.getElementById("results-content");
const comparisonSection = document.getElementById("comparison");
const comparisonContent = document.getElementById("comparison-content");

// Safely display text returned by the API.
const escapeHTML = (value = "") =>
  String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[char]);

// Sidebar navigation: highlight only the selected section.
const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
  });
});

// Suggestion chips fill the search box.
document.querySelectorAll(".suggestion-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    queryInput.value = chip.dataset.query || chip.textContent.trim();
    queryInput.focus();
  });
});

// Search button.
researchBtn.addEventListener("click", runResearch);

// Enter starts research; Shift + Enter adds a new line.
queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    runResearch();
  }
});

// Create the Try Again button once.
function createNewResearchButton() {
  if (document.getElementById("new-research-btn")) return;

  const button = document.createElement("button");

  button.id = "new-research-btn";
  button.className = "primary-button";
  button.textContent = "↻ Try Again · New Research";

  button.addEventListener("click", startNewResearch);

  // Keep the button below the research results.
  resultsSection.appendChild(button);
}

// Clear the previous research and return to the search area.
function startNewResearch() {
  queryInput.value = "";

  resultsSection.hidden = true;
  comparisonSection.hidden = true;

  resultsContent.innerHTML = "";
  comparisonContent.innerHTML = "";

  const newResearchButton = document.getElementById("new-research-btn");
  if (newResearchButton) {
    newResearchButton.remove();
  }

  researchBtn.disabled = false;
  researchBtn.textContent = "Research papers";

  queryInput.focus();

  document.getElementById("search").scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}

// Send the research query to FastAPI.
async function runResearch() {
  const query = queryInput.value.trim();

  if (!query) {
    queryInput.focus();
    alert("Please enter a research question first.");
    return;
  }

  researchBtn.disabled = true;
  researchBtn.textContent = "Researching...";

  resultsSection.hidden = false;
  comparisonSection.hidden = true;

  resultsContent.innerHTML = `
    <div class="research-loading">
      <p>Researching your topic...</p>
      <p>Searching sources, analyzing papers and preparing comparisons.</p>
      <p>This may take a few minutes. Please keep this page open.</p>
    </div>
  `;

  resultsSection.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });

  try {
    const response = await fetch("http://127.0.0.1:8000/research", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Research request failed.");
    }

    renderResults(data);
    createNewResearchButton();

  } catch (error) {
    resultsContent.innerHTML = `
      <div class="research-error">
        <h3>Unable to complete research</h3>
        <p>${escapeHTML(error.message)}</p>
        <p>Please check that your FastAPI server is running.</p>
        <button
          type="button"
          class="primary-button"
          id="retry-research-btn"
        >
          Try Again
        </button>
      </div>
    `;

    document
      .getElementById("retry-research-btn")
      .addEventListener("click", runResearch);

  } finally {
    researchBtn.disabled = false;
    researchBtn.textContent = "Research papers";
  }
}

// Display papers and their summaries.
function renderResults(data) {
  const papers = data.papers || [];
  const summaries = data.summaries || [];

  resultsContent.innerHTML = `
    <div class="research-overview">
      <p><strong>Topic:</strong> ${escapeHTML(data.topic)}</p>
      <p><strong>Research task:</strong> ${escapeHTML(data.task)}</p>
      <p><strong>Research plan:</strong> ${escapeHTML(data.search_plan)}</p>
      <p><strong>Sources:</strong> ${escapeHTML((data.sources || []).join(", "))}</p>
      <p><strong>Relevant sources found:</strong> ${papers.length}</p>
    </div>

    ${
      papers.length
        ? papers.map((paper, index) => {
            const summary = summaries[index] || {};

            return `
              <article class="paper-card">
                <p class="paper-number">PAPER ${index + 1}</p>

                <h3>${escapeHTML(paper.title || "Untitled")}</h3>

                <p class="paper-authors">
                  ${escapeHTML(
                    (paper.authors || []).join(", ") ||
                    "Authors not provided"
                  )}
                </p>

                <p class="paper-source">
                  Source type: ${escapeHTML(paper.source_type || "unknown")}
                </p>

                ${
                  paper.url
                    ? `
                      <p>
                        <a
                          href="${escapeHTML(paper.url)}"
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View original source ↗
                        </a>
                      </p>
                    `
                    : ""
                }

                <div class="paper-summary">
                  <h4>Problem</h4>
                  <p>${escapeHTML(summary.problem || "Not available")}</p>

                  <h4>Approach</h4>
                  <p>${escapeHTML(summary.approach || "Not available")}</p>

                  <h4>Datasets / Benchmarks</h4>
                  <p>${escapeHTML(summary.datasets || "Not available")}</p>

                  <h4>Results</h4>
                  <p>${escapeHTML(summary.results || "Not available")}</p>

                  <h4>Limitations</h4>
                  <p>${escapeHTML(summary.limitations || "Not available")}</p>
                </div>
              </article>
            `;
          }).join("")
        : "<p>No relevant sources were found for this query.</p>"
    }
  `;

  // Display comparative analysis.
  const comparison = data.comparison || {};

  comparisonContent.innerHTML = `
    <article class="paper-card">
      <h3>Overall Comparison</h3>
      <p>${escapeHTML(
        comparison.overall_comparison || "Not available"
      )}</p>

      <h4>Similarities</h4>
      ${renderList(comparison.similarities)}

      <h4>Differences</h4>
      ${renderList(comparison.differences)}

      <h4>Strongest Approach</h4>
      <p>${escapeHTML(
        comparison.best_approach || "Not enough information"
      )}</p>
    </article>

    <p class="research-disclaimer">
      AI-generated summaries and comparisons may contain errors.
      Verify important claims against the original sources.
    </p>
  `;

  comparisonSection.hidden = false;
}

// Safely render comparison lists.
function renderList(items = []) {
  if (!items.length) {
    return "<p>Not available</p>";
  }

  return `
    <ul>
      ${items.map((item) => `<li>${escapeHTML(item)}</li>`).join("")}
    </ul>
  `;
}
