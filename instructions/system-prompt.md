# System Prompt Setup (Any AI)

Paste the methodology into your AI's system prompt or instructions field. Works with any platform. If you're using Claude, ChatGPT, or Gemini, consider the platform-specific guides instead — [Claude Project](claude-project.md), [Custom GPT](custom-gpt.md), or [Gemini Gem](gemini-gem.md) — which give you a better setup with knowledge files.

## What you need

- Access to an AI that lets you set a system prompt or custom instructions
- The files from this repository (download or clone it)

## Which version to use

There are two versions of the methodology you can paste:

| Version | File | Size | Best for |
|---------|------|------|----------|
| **Full** | [`methodology/methodology-master-doc.md`](../methodology/methodology-master-doc.md) | ~12,000 chars | Platforms with large instruction fields (API system prompts, open-source model configs) |
| **Compressed** | [`toolkit/compressed-instructions/compressed-master.md`](../toolkit/compressed-instructions/compressed-master.md) | ~1,500 chars | Platforms with short limits (ChatGPT Custom Instructions, Grok, etc.) |

The compressed version preserves the core methodology — identity framing, required/recommended data points, the answer-caveat-invitation cycle, and all five principles. It trims activation criteria and tone guidance to fit.

## Setup

### 1. Pick your version and copy it

If your platform's instruction field can hold ~12,000 characters, use the full version. If it caps out around 1,500–8,000 characters, use the compressed version.

Open the file and copy the entire contents.

### 2. Paste it into your AI's instructions

Where you paste depends on the platform. Look for fields labeled "system prompt," "custom instructions," "system message," or similar. Paste the full contents there.

### 3. Start a conversation

Ask a financial question. The AI should ask you follow-up questions before giving advice.

## Tips

- The identity framing at the top of the full version (or the first paragraph of the compressed version) is the most important part — it tells the AI to be direct instead of hedging. Don't skip it.
- If you're using the full version and need to trim, cut Section 1 (activation criteria) first. The compressed version has already done this for you.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
