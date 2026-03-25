# Methodology

The source methodology for improving AI responses to questions with financial implications.

## Quick Start

Load `methodology-master-doc.md` into any AI platform. It works standalone with universal context collection. For topic-specific depth, also load the relevant category overview file(s).

## Files

| File | Purpose |
|------|---------|
| `methodology-master-doc.md` | Identity framing + core instructions (Sections 1–3). Works standalone. |
| `{category}/{category}-overview.md` | Topic-specific data points, red flags, conversation guidance, and example exchanges. |

## How It Works

The master document starts with **identity framing** — explicit permission for the AI to be direct and opinionated rather than hedging — followed by three sections:

1. **Activation Criteria** — When to engage the methodology (and when not to)
2. **Getting Sufficient Context** — Collect goal, expected role, feelings, and financial facts before answering. Pre-fill from any structured data already in the conversation.
3. **Response Instructions** — Answer + caveat + invitation cycle: give your best answer, note how 1–2 missing data points could change it, invite the user to share them. Repeat until nothing meaningful is missing.

## Categories

| Category | Folder | Overview File |
|----------|--------|---------------|
| Career and Income | `career/` | `career-overview.md` |
| Lifestyle and Spending | `spending/` | `spending-overview.md` |
| Liquidity and Life Events | `life-events/` | `life-events-overview.md` |
| Retirement and Investing | `investing/` | `investing-overview.md` |
| General Status Check | `assessment/` | `assessment-overview.md` |

Each folder contains a category overview file. Scenario files (deeper guidance for specific situations within a category) are planned but not yet written. Category overviews work standalone.

---

## For Contributors and Forkers

Everything below is for the methodology author or contributors — not for the AI.

### Content Model

This methodology has two layers. Each layer adds specificity:

| Layer | Files | Purpose |
|-------|-------|---------|
| 1 — Category | `{category}/{category}-overview.md` | Shared questions and guidance for an entire financial domain |
| 2 — Scenario | `{category}/{scenario}.md` | Deep questions for a specific situation within that domain |

Layers are additive. A scenario file builds on top of its category overview — it never replaces it.

**Key principles:**
- Every category works without scenario files. Category overviews are comprehensive enough for useful analysis on their own.
- No duplication across layers. Category-level questions live only in the overview. Scenario questions live only in the scenario file.
- Scenario files are additive. Never skip the category overview when using a scenario file.

### How the Document Splits

The methodology has two functional layers:

- **Core instructions (Sections 1-3)**: Activation criteria, context-gathering behavior (with general fallback data points, red flags, and conversation guidance), response philosophy, tone, and edge cases. These are process instructions — they tell the AI *how* to behave.
- **Topic reference (category folders)**: Per-topic scope, required/recommended data points, conversation guidance, red flags, and example exchanges organized in category folders with overview and scenario files. This is reference data — it tells the AI *what* to ask and *what* to watch for within each topic.

The core instructions depend on the topic reference at three points:

| Dependency | Where | Risk if topic reference is unavailable |
|---|---|---|
| **Data-point lookup** | Section 2 (snapshot handling, context gathering) | **Medium.** Section 2 provides general data points as a fallback. AI still gathers useful context but is less targeted without topic-specific data points. |
| **Red-flag detection** | Section 3 ("Know your limits" tenet) | **Medium.** Section 2 provides general red flags. AI catches severe cases but misses subtler structured triggers (e.g., concentrated portfolio, high DTI). |
| **Conversation guidance** | Section 2 (conversation guidance) | **Low.** Section 2 includes general conversation guidance. Quality degrades gracefully without topic-specific phrasing. |

To reduce synchronous dependency, the core instructions check whether topic-specific files are loaded and fall back to general data points, red flags, and conversation guidance in Section 2 if not.

### Deployment Scenarios

#### Single-file deployments (topic reference included)

Use when the platform can handle the full document in one place.

**Paste-at-start (any platform)**
- Full master document with a brief instruction header: "Please follow this methodology when I ask you financial questions. Read through it, then wait for my question."
- Works on any AI platform. Estimated cost: ~5,000-6,000 tokens.

**Gemini Gem instructions**
- The full document fits within Gem instruction limits (~15,000 chars).
- No splitting required.

#### Split deployments (topic reference separate)

Use when the platform has a short instruction limit but supports attached/uploaded files.

**Claude Skill**
- Sections 1-3 go into SKILL.md body (~120 lines, well within 500-line limit).
- Category folders (with overview and scenario files) go into a `references/` subdirectory, preserving the folder structure. Claude loads resources on demand.
- Frontmatter: `name` ≤64 chars, `description` ≤200 chars.
- **Dependency handling**: Claude Skills automatically surface resources when relevant. The topic identification workflow and the fallback guidance in Section 2 align with this behavior. Lowest-risk split.

**Custom GPT (system prompt + knowledge file)**
- Sections 1-3 go into the system prompt (~7,500 chars, within the ~8,000 char limit).
- Full master document (or category overview and scenario files combined) uploaded as a knowledge file.
- Add to the end of the system prompt: "When you identify the user's topic, search the uploaded knowledge file for that topic's required data points, recommended data points, conversation guidance, and red flags before asking follow-up questions."
- **Dependency handling**: GPTs search knowledge files reactively. The explicit retrieval instruction in Section 2 helps, but adding the system-prompt reminder above makes retrieval more reliable.

**Claude / ChatGPT Project instructions + project files**
- Same pattern as Custom GPT. Sections 1-3 in project instructions, category files as project files.
- Project-attached files are generally available in context automatically, making this more reliable than knowledge-file search.

#### Compressed deployments (heavily reduced)

Use when the platform allows very limited instruction space and no file uploads.

**ChatGPT / Grok Custom Instructions (~1,500 chars)**
- Consolidate Sections 1-3 into a single compressed block. Preserve the Core Philosophy Tenets in full — do not compress or paraphrase them.
- For topic coverage: include only the **scope explainer** and **required data points** for each topic. Drop recommended data points, conversation guidance, red flags, and examples.
- Compress everything else to essentials: 1 sentence on purpose, 3-4 key behavioral rules (ask before answering, max 3 questions per message, show trade-offs, quantify), tone reminder.
- This format delivers a meaningfully structured version of the methodology — the AI will know *what* to ask for each topic and *how* to think about responses — but without the full conversation guidance, red flags, or recommended data points.

### Deployment Modes

The master document is designed to work at multiple levels of specificity:

| Mode | Files loaded | Use case |
|------|-------------|----------|
| **General** | `methodology-master-doc.md` only | Standalone — universal context collection |
| **Category** | Master doc + `{category}-overview.md` | Topic-specific data points and red flags |
| **Full** | Master doc + overview + `{scenario}.md` | Deep scenario-specific guidance |

### Verification Checklist

After any deployment, verify:

1. **Topic routing works**: Ask a question from each implemented topic and confirm the AI identifies the correct category.
2. **Data-point gathering is structured**: Confirm the AI asks for specific required data points, not generic open-ended questions.
3. **Red flags trigger correctly**: Test at least one red-flag scenario per topic and confirm the AI suggests professional consultation.
4. **Snapshot recognition works**: Paste a sample snapshot and confirm the AI parses it, skips redundant questions, and asks only for missing data.
5. **Edge cases are respected**: Test an impatient-user scenario and a multi-topic question to confirm correct handling.
