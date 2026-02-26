# Financial Context Toolkit

A toolkit for improving the quality of AI responses to questions with financial implications. Built by [WorthIQ](https://worthiq.app).

## What This Is

Most AI assistants give generic financial guidance. This project provides a structured methodology that teaches AI to ask the right questions, gather personal context, and deliver advice tailored to the user's actual situation.

**This is a toolkit repo, not a skill repo.** It contains the source methodology, and will also contain tooling around it — test harnesses for evaluating methodology quality, platform-specific format outputs (Claude Skill, Custom GPT, Gemini Gem), and other utilities. The methodology itself is the core asset; everything else in this repo supports developing, testing, and deploying it.

## Repository Structure

```
financial-context-toolkit/
├── methodology/                    # The methodology (source of truth)
│   ├── methodology-master-doc.md   # Core AI instructions (Sections 1–3)
│   ├── loading-protocol.md         # Topic routing, snapshot handling, content layering
│   ├── implementation-guide.md     # Deployment scenarios & verification
│   ├── career/                     # One folder per financial topic
│   │   └── career-overview.md      # Category overview (scenario files TBD)
│   ├── spending/
│   ├── life-events/
│   ├── investing/
│   ├── relationships/
│   └── assessment/
├── README.md
├── LICENSE
└── CLAUDE.md
```

## How It Works

The methodology is built around a **three-section master document** ([`methodology/methodology-master-doc.md`](methodology/methodology-master-doc.md)) that works standalone or with topic-specific files:

1. **Activation Criteria** — When to engage the methodology (and when not to)
2. **Getting Sufficient Context** — Universal context collection framework: Goal, Expected role, Feelings, and Facts. Falls back to general data points and red flags when no topic-specific files are loaded.
3. **Response Instructions** — Core advice philosophy, tone, handling missing context, and edge cases

### Three-version deployment

The master document is designed to work at three levels of specificity:

| Version | Files loaded | Use case |
|---------|-------------|----------|
| **General** | `methodology-master-doc.md` only | Standalone — no topic routing needed |
| **Category** | Master doc + `loading-protocol.md` + `{category}-overview.md` | Topic-specific data points and red flags |
| **Full** | Master doc + `loading-protocol.md` + overview + `{scenario}.md` | Deep scenario-specific guidance |

### Content model

The methodology uses a **two-layer content model** for progressive specificity:

| Layer | What it contains | Where it lives |
|-------|-----------------|----------------|
| **Category** | Shared questions, guidance, and red flags for an entire financial domain | `methodology/{category}/{category}-overview.md` |
| **Scenario** | Deep, narrow questions for a specific situation within a category | `methodology/{category}/{scenario}.md` |

Category overviews work standalone. Scenario files are additive — used alongside the overview, never instead of it. See [`methodology/loading-protocol.md`](methodology/loading-protocol.md) for the full protocol.

### Categories (6)

| Category | Folder |
|----------|--------|
| Career and Income | `methodology/career/` |
| Lifestyle and Spending | `methodology/spending/` |
| Liquidity and Life Events | `methodology/life-events/` |
| Retirement and Investing | `methodology/investing/` |
| Relationships and Teamwork on Finances | `methodology/relationships/` |
| General Status Check | `methodology/assessment/` |

## Philosophy

- **Harm Reduction**: AI isn't going away. Even if Anthropic and OpenAI go bankrupt tomorrow, AI is here to stay. Rather than teach abstinence DARE style, help people do better with what they have while encouraging safer alternatives.
- **Inherited Security Rules**: No handrolling permissions or guidelines. These instructions enhance the models as is. It takes no responsibility for security guardrails in the responses or lack thereof.
- **No Strings Attached**: Go do what you want with it. Download it, remake it, whatever.
- **Contributors Welcome**: Whether you're just trying it out or have some domain expertise, happy to have help.

## Goals

- **Context-first responses** — Gather relevant financial details before answering, not after
- **Structured topic coverage** — Consistent data-point checklists for career decisions, spending, investing, retirement, and more
- **Red flag detection** — Know when to recommend a professional instead of answering
- **Platform-agnostic** — Deploy as a Claude Skill, Custom GPT, Gemini Gem, or raw prompt

## Status

Early stage. The core methodology is complete. Platform-specific implementations, test harness, example conversations, and contribution guidelines are coming soon.

## License

[MIT](LICENSE)
