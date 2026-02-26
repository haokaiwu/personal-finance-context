# Financial Context Toolkit

A toolkit for improving the quality of AI responses to questions with financial implications. Built by [WorthIQ](https://worthiq.app).

## What This Is

Most AI assistants give generic financial guidance. This project provides a structured methodology that teaches AI to ask the right questions, gather personal context, and deliver advice tailored to the user's actual situation.

**This is a toolkit repo, not a skill repo.** It contains the source methodology, and will also contain tooling around it — test harnesses for evaluating methodology quality, platform-specific format outputs (Claude Skill, Custom GPT, Gemini Gem), and other utilities. The methodology itself is the core asset; everything else in this repo supports developing, testing, and deploying it.

## Repository Structure

```
financial-context-toolkit/
├── methodology/                    # The methodology (source of truth)
│   ├── methodology-master-doc.md   # Core AI instructions (Sections 1–4)
│   ├── loading-protocol.md         # How content layers combine
│   ├── implementation-guide.md     # Deployment scenarios & verification
│   ├── career/                     # One folder per financial topic
│   │   ├── career-overview.md      # Category overview (Layer 1)
│   │   └── changing-jobs.md        # Scenario file (Layer 2)
│   ├── spending/
│   ├── purchases/
│   ├── life-events/
│   ├── retirement/
│   ├── investing/
│   ├── dependents/
│   ├── conflicts/
│   ├── anxiety/
│   └── assessment/
├── README.md
├── LICENSE
└── CLAUDE.md
```

### Methodology content model

The methodology uses a **two-layer content model** for progressive context sharing:

| Layer | What it contains | Where it lives |
|-------|-----------------|----------------|
| **Category** | Shared questions, guidance, and red flags for an entire financial domain | `methodology/{category}/{category}-overview.md` |
| **Scenario** | Deep, narrow questions for a specific situation within a category | `methodology/{category}/{scenario}.md` |

Category overviews work standalone. Scenario files are additive — used alongside the overview, never instead of it. See [`methodology/loading-protocol.md`](methodology/loading-protocol.md) for the full protocol.

**Core AI instructions** (Sections 1–4 of [`methodology/methodology-master-doc.md`](methodology/methodology-master-doc.md)) define when to activate, how to gather context, and how to respond. They reference category/scenario files but work independently of any specific topic.

### Categories (10)

Career, spending, purchases, life-events, retirement, investing, dependents, conflicts, anxiety, assessment. Each folder contains one overview file and one or more scenario files.

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
