# Custom GPT Setup

Create a [Custom GPT](https://help.openai.com/en/articles/8554397-creating-a-gpt) in ChatGPT that gathers financial context before giving advice.

## What you need

- A ChatGPT Plus, Pro, or Team subscription (creating Custom GPTs requires paid access)
- The files from this repository (download or clone it)

## Setup

### 1. Create a new Custom GPT

Go to [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor) (or click your profile icon → **My GPTs** → **Create a GPT**). Switch to the **Configure** tab.

### 2. Fill in the basics

- **Name:** Something like "Financial Context Advisor" (your choice)
- **Description:** A short line like "Asks the right questions before giving financial guidance."

### 3. Set the system prompt

In the **Instructions** field, paste the entire contents of `methodology/methodology-master-doc.md`.

The master doc is roughly 12,000 characters. Custom GPT instructions have a limit of 8,000 characters, so it won't all fit. Paste the identity framing (the text at the very top) plus Sections 2–3. If you still need room, trim Section 1 (activation criteria) — it's the safest to cut.

Then add this line at the very end of the instructions:

> When you identify the user's topic, search the uploaded knowledge file for that topic's required data points, recommended data points, conversation guidance, and red flags before asking follow-up questions.

This tells the GPT to actually use the knowledge files you'll upload next.

### 4. Upload topic files (recommended)

For topic-specific questions and red flags, scroll down to **Knowledge** and upload these files:

- `methodology/loading-protocol.md`
- `methodology/career/career-overview.md`
- `methodology/spending/spending-overview.md`
- `methodology/life-events/life-events-overview.md`
- `methodology/investing/investing-overview.md`
- `methodology/assessment/assessment-overview.md`

### 5. Save and publish

Click **Save** (or **Update**). Choose whether to keep it private, share via link, or publish to the GPT Store.

## Tips

- The 8,000-character instruction limit means you'll need to trim. Priority order: identity framing first, then Sections 2–3, then Section 1. You can also put the full master doc in a knowledge file and add a line in the instructions telling the GPT to read it.
- The knowledge file retrieval instruction you added in step 3 matters — without it, the GPT often ignores uploaded files.
- Knowledge files may not load until after the GPT's first response. The most important behavioral instructions (ask before answering, gather context) should live in the Instructions field, not only in knowledge files.
- See OpenAI's [Creating a GPT](https://help.openai.com/en/articles/8554397-creating-a-gpt) guide and [Knowledge in GPTs](https://help.openai.com/en/articles/8843948-knowledge-in-gpts) for more details.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
