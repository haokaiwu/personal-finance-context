# Appendix: Implementation Guide

*These notes are for the methodology author, not for the AI.*

### How the document splits

This methodology has two functional layers:

- **Core instructions (Sections 1-3)**: Activation criteria, context-gathering behavior (with general fallback data points, red flags, and conversation guidance), response philosophy, tone, and edge cases. These are process instructions — they tell the AI *how* to behave.
- **Topic reference (category folders)**: Per-topic scope, required/recommended data points, conversation guidance, red flags, and example exchanges organized in category folders with overview and scenario files. This is reference data — it tells the AI *what* to ask and *what* to watch for within each topic. See [loading-protocol.md](loading-protocol.md) for how layers combine and for the topic identification and snapshot handling workflow.

The core instructions depend on the topic reference at three points:

| Dependency | Where | Risk if topic reference is unavailable |
|---|---|---|
| **Data-point lookup** | `loading-protocol.md` (snapshot handling), Section 2 (context gathering) | **Medium.** Section 2 provides general data points as a fallback. AI still gathers useful context but is less targeted without topic-specific data points. |
| **Red-flag detection** | Section 3 ("Know your limits" tenet) | **Medium.** Section 2 provides general red flags. AI catches severe cases but misses subtler structured triggers (e.g., concentrated portfolio, high DTI). |
| **Conversation guidance** | Section 2 (conversation guidance) | **Low.** Section 2 includes general conversation guidance. Quality degrades gracefully without topic-specific phrasing. |

To reduce synchronous dependency, the core instructions check whether topic-specific files are loaded and fall back to general data points, red flags, and conversation guidance in Section 2 if not. Topic identification and snapshot handling are documented in [loading-protocol.md](loading-protocol.md), which is loaded alongside category files.

### Deployment scenarios

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
- **Dependency handling**: Claude Skills automatically surface resources when relevant. The topic identification workflow in `loading-protocol.md` and the fallback guidance in Section 2 align with this behavior. Lowest-risk split.

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

### What to verify after any deployment

1. **Topic routing works**: Ask a question from each implemented topic and confirm the AI identifies the correct category.
2. **Data-point gathering is structured**: Confirm the AI asks for specific required data points, not generic open-ended questions.
3. **Red flags trigger correctly**: Test at least one red-flag scenario per topic and confirm the AI suggests professional consultation.
4. **Snapshot recognition works**: Paste a sample snapshot and confirm the AI parses it, skips redundant questions, and asks only for missing data.
5. **Edge cases are respected**: Test an impatient-user scenario and a multi-topic question to confirm correct handling.
