# Loading Protocol

How to layer and combine context files when using this methodology.

---

## Two-Layer Content Model

This repository organizes financial context into two layers. Each layer adds specificity:

| Layer | Files | Purpose |
|-------|-------|---------|
| 1 — Category | `{category}/{category}-overview.md` | Shared questions and guidance for an entire financial domain |
| 2 — Scenario | `{category}/{scenario}.md` | Deep questions for a specific situation within that domain |

**Layers are additive.** A scenario file builds on top of its category overview — it never replaces it.

---

## Topic Identification & Snapshot Handling

This section applies when category files are loaded alongside the master document.

### Workflow

1. Identify which topic the question falls into. Use your best guess; if your first 2 tries miss, confirm with the user: "It sounds like you're asking about career decisions — is that right?"
2. Check conversation context (including attached files) for a **snapshot** — a structured text block or image with WorthIQ branding and labeled financial fields (net worth, income, savings rate, emergency fund, account allocations, concern areas).
3. **If a snapshot is found**: parse all fields as established context, acknowledge briefly, then look up the topic's required/recommended data points in the relevant category overview and ask only for what's missing. Never question snapshot accuracy — treat it as the user's stated reality.
4. **If no snapshot is found**: proceed to context gathering using the master document's Section 2.

---

## How to Use

1. **Identify the category** the user's question falls into → open `{category}/{category}-overview.md`.
2. **Check for a matching scenario file** in the same folder. If one exists that fits the user's specific situation, also use it.
3. **Gather context in order:** Category overview first, then scenario-specific questions.
4. **If no scenario file matches**, the category overview is sufficient on its own. Every category overview is designed to work standalone.
5. **Multi-category situations** (e.g., a job change that also involves a major purchase): load multiple category overviews and their relevant scenarios. Deduplicate overlapping questions.

---

## Key Principles

- **Every category works without scenario files.** Category overviews are comprehensive enough for useful analysis on their own.
- **No duplication across layers.** Category-level questions live only in the overview. Scenario questions live only in the scenario file.
- **Scenario files are additive.** Never skip the category overview when using a scenario file.
- **The overview's "Available Scenarios" section** lists what scenario files exist. When none match, note that the overview is sufficient.

---

## Category Directory

| Category | Folder | Overview File |
|----------|--------|---------------|
| Career and Income | `career/` | `career-overview.md` |
| Lifestyle and Spending | `spending/` | `spending-overview.md` |
| Liquidity and Life Events | `life-events/` | `life-events-overview.md` |
| Retirement and Investing | `investing/` | `investing-overview.md` |
| Relationships and Teamwork on Finances | `relationships/` | `relationships-overview.md` |
| General Status Check | `assessment/` | `assessment-overview.md` |
