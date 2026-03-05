# Personal Financial Context for AI

A toolkit for improving the quality of AI responses to personal finance questions. Built by [WorthIQ](https://worthiq.app).

## What This Is

People ask AI for advice even when they shouldn't. Rather than preaching abstinence, think of this as sex ed. This toolkit helps for personal finance or adjacent questions. For a full list of what is currently covered and what isn't, check the latest methodology doc.

---

## How to use it

There are a few paths to using it:

1. RECOMMENDED: Use with Claude as a Skill. See [here](instructions/claude-skill.md) for instructions.
2. RECOMMENDED: Add methodology folder into a Claude project, a custom GPT, or similar. See [here](instructions/README.md) for instructions.
3. Copy and paste the [general methodology doc](methodology/methodology-master-doc.md) into your system instructions. See [here](instructions/system-prompt.md) for instructions.

---

## Using with WorthIQ snapshots:

WorthIQ Snapshots summarize your finances in a way that makes conversations easier. That includes conversations with AI. Go to the website [here](https://worthiq.app) to summarize your finances.

Using them is **OPTIONAL**. The instructions work fine on their own, but the AI will be a little more annoying in asking you for context. 

To use WorthIQ snapshots:

1. Set up the instructions first. See the steps above.
2. Sign up, and make a snapshot which corresponds to your question.
3. Export the snapshot as text. 
4. Copy the snapshot above your question.

---

## How does it work?

Instructions tell the AI to ask you questions rather than respond immediately if you don't provide sufficient context. They also give AI a set of required and recommended data points to collect as context. Both of these instructions are helpful because it prevents the AI from jumping to conclusions based on limited information, which is particularly harmful for personal finance conversations.

The instructions also gives light guidance on how to give good responses, and it lightly jailbreaks the AI in cases when it's being overly cautious. 

The instructions don't activate unless it's a question that requires personalized context. It shouldn't guide behavior for factual questions, hypotheticals, and so on. The instructions are human-readable, so you can inspect it to see exactly what it's telling the AI to do.

--

## Support

For questions, you can reach me at kai@worthiq.app. I also set up a Discord server [here].

## Disclaimers

### NO financial advice 

Instructions explicitly avoid regulated financial advice. This includes personalized asset allocation and securities recommendations. It's illegal for AI to give this advice. 

### NO perfect answers 

These instructions will give you better results, but they don't guarantee perfection. Use with caution.

### NO conflict resolution

AI sucks at being a neutral 3rd party, so there are no instructions yet for handling money conflicts. Please contact Kai directly if you want to use instructions for this purpose.

## Repository Structure

| Folder | What's in it |
|--------|-------------|
| [`methodology/`](methodology/) | The core methodology — AI instructions for gathering financial context and delivering personalized guidance. This is the main asset. |
| [`instructions/`](instructions/) | Step-by-step setup guides for Claude, ChatGPT, Gemini, and generic system prompts. |
| [`test-harness/`](test-harness/) | CLI workbench for testing the methodology against real questions across Claude, GPT, and Gemini. Uses Google Sheets as a data store. |

## Status

Early stage. The core methodology and test harness are complete. Platform-specific implementations, example conversations, and contribution guidelines are coming soon.

## License

[MIT](LICENSE)
