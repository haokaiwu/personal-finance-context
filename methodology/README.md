# Methodology

The source methodology for improving AI responses to questions with financial implications.

## Files

| File | Purpose |
|------|---------|
| [`methodology-master-doc.md`](methodology-master-doc.md) | Identity framing + core instructions (Sections 1–3). Works standalone. |
| [`loading-protocol.md`](loading-protocol.md) | Topic routing, snapshot handling, and how content layers combine. Loaded alongside category files. |
| [`implementation-guide.md`](implementation-guide.md) | Deployment scenarios (single-file, split, compressed) and verification checklists. |

## How It Works

The master document starts with **identity framing** — explicit permission for the AI to be direct and opinionated rather than hedging — followed by three sections:

1. **Activation Criteria** — When to engage the methodology (and when not to)
2. **Getting Sufficient Context** — Collect goal, expected role, feelings, and financial facts before answering. Pre-fill from any structured data already in the conversation.
3. **Response Instructions** — Answer + caveat + invitation cycle: give your best answer, note how 1–2 missing data points could change it, invite the user to share them. Repeat until nothing meaningful is missing.

## Deployment Modes

The master document is designed to work at multiple levels of specificity:

| Mode | Files loaded | Use case |
|------|-------------|----------|
| **General** | `methodology-master-doc.md` only | Standalone — universal context collection |
| **Category** | Master doc + `loading-protocol.md` + `{category}-overview.md` | Topic-specific data points and red flags |
| **Full** | Master doc + `loading-protocol.md` + overview + `{scenario}.md` | Deep scenario-specific guidance |

## Categories (6)

| Category | Folder |
|----------|--------|
| Career and Income | [`career/`](career/) |
| Lifestyle and Spending | [`spending/`](spending/) |
| Liquidity and Life Events | [`life-events/`](life-events/) |
| Retirement and Investing | [`investing/`](investing/) |
| Relationships and Teamwork on Finances | [`relationships/`](relationships/) |
| General Status Check | [`assessment/`](assessment/) |

Each folder contains a category overview file. Scenario files (deeper guidance for specific situations within a category) are planned but not yet written. Category overviews work standalone. See [`loading-protocol.md`](loading-protocol.md) for how layers combine.
