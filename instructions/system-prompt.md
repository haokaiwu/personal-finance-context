# System Prompt Setup (Any AI)

Paste the methodology into your AI's system prompt or instructions field. Works with any platform. If you're using Claude, ChatGPT, or Gemini, consider the platform-specific guides instead — [Claude Project](claude-project.md), [Custom GPT](custom-gpt.md), or [Gemini Gem](gemini-gem.md) — which give you a better setup with knowledge files.

## What you need

- Access to an AI that lets you set a system prompt or custom instructions
- The files from this repository (download or clone it)

## Setup

### 1. Copy the master doc

Open `methodology/methodology-master-doc.md` and copy the entire contents.

### 2. Paste it into your AI's instructions

Where you paste depends on the platform. Look for fields labeled "system prompt," "custom instructions," "system message," or similar. Paste the full contents there.

If your platform has a character limit that's too short for the full document (~12,000 characters), keep the identity framing (the text at the very top, before Section 1) and Sections 2–3. Section 1 (activation criteria) is the safest to trim.

### 3. Add topic content (optional)

For topic-specific questions and red flags, also paste or upload:

- `methodology/loading-protocol.md`
- `methodology/career/career-overview.md`
- `methodology/spending/spending-overview.md`
- `methodology/life-events/life-events-overview.md`
- `methodology/investing/investing-overview.md`
- `methodology/assessment/assessment-overview.md`

If your platform supports file uploads, upload them separately. If it only has a text field, paste them after the master doc content.

### 4. Start a conversation

Ask a financial question. The AI should ask you follow-up questions before giving advice.

## Tips

- The identity framing at the top of the master doc is important — it tells the AI to be direct instead of hedging. Don't skip it.
- If you can only fit one file, `methodology-master-doc.md` is the one to use. It works well on its own.
- Some platforms (like ChatGPT's "Custom Instructions" in settings) have very short character limits (~1,500 chars). In that case, focus on the core philosophy tenets and required data points — see the methodology for what those are.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
