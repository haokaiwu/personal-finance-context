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
| Career Decisions | `career/` | `career-overview.md` |
| Day-to-Day Spending | `spending/` | `spending-overview.md` |
| Major Purchases ($2k+) | `purchases/` | `purchases-overview.md` |
| Unexpected Life Events | `life-events/` | `life-events-overview.md` |
| Retirement Planning | `retirement/` | `retirement-overview.md` |
| Investing | `investing/` | `investing-overview.md` |
| Supporting Dependents | `dependents/` | `dependents-overview.md` |
| Money Conflicts | `conflicts/` | `conflicts-overview.md` |
| Money Anxiety | `anxiety/` | `anxiety-overview.md` |
| General Financial Assessment | `assessment/` | `assessment-overview.md` |
