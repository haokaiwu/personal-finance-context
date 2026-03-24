# AI Personal Finance Coach

Turn AI into a personal finance coach. Built by Kai from [WorthIQ](https://worthiq.app).

## What It Does

People ask AI anything these days. Personal finance is probably no different. This toolkit helps you get better responses, especially for high-impact questions.

## How Does It Work

It's a set of instructions which changes your AI's behavior. Whenever you ask a personal finance question with it installed, it checks if the question requires personalized context to answer. If it does, it asks you for critical context, and then it uses this context to produce an answer. Without this instruction, AI typically jumps straight into an answer without asking for context.

## Why It Matters

Important personal finance questions require the right context to answer. People often don't know what context to give, and AI usually doesn't know what to ask. These instructions help break that habit. They aren't perfect (see disclaimers), but it improves the quality of responses.

## Examples

See the examples folder for the instructions in action. 

## How to use it

There are a few paths to using it:

1. RECOMMENDED: Use as a Claude Skill. See [here](instructions/claude-skill.md) for instructions.
2. RECOMMENDED: Use in a Claude Project, ChatGPT Project, or Gemini Gem. See [here](instructions/README.md) for instructions.
3. Copy and paste the [general methodology doc](methodology/methodology-master-doc.md) into your system instructions. See [here](instructions/system-prompt.md) for instructions.

Ask questions with the most advanced models only. As of current release, they are Opus 4.6, Sonnect 4.6, GPT 5.4, and Gemini Pro 3.1 Preview.

## Using with WorthIQ snapshots:

WorthIQ Snapshots summarize your finances to make conversations easier. It asks you simple questions and returns a shareable image or block of text which you can copy-and-paste directly into an AI chat window. Go to the website [here](https://worthiq.app) to sign up.

Using them is **OPTIONAL**. The instructions work fine on their own, though the AI will only ask for critical context by default.

## Support

You can reach me at kai@worthiq.app. I also set up a Discord server [here]. General questions are free, but personal tech support is not. I do product research on Reddit under [u/CryptoMemeEconomy](https://www.reddit.com/user/CryptoMemeEconomy/) 

## License

MIT License, so you can do what you want with it. I built this repo to start a conversation, not to make money.

## Disclaimers

### NO regulated financial advice 

The instructions purposely avoid regulated financial advice, which deals with recommendations on securities (stocks, funds, etc.) or asset allocation. If that's what you're looking for, find a professional. 

### NO perfect answers 

These instructions will give you better results, but they don't guarantee perfection. Current AI was tuned to immediately give answers, not probe for context. These instructions go against their fundamental "programming" to an extent, so you may see weird behavior sometimes. Use with caution.

### NO conflict resolution

AI sucks at being a neutral 3rd party, so there are no instructions yet for handling money conflicts. Please contact me if you'd like instructions for this.

## Repository Structure

| Folder | What's in it |
|--------|-------------|
| [`methodology/`](methodology/) | The core methodology — AI instructions for gathering financial context and delivering personalized guidance. This is the main asset. |
| [`toolkit/`](toolkit/) | Ready-to-use implementations of the methodology — compressed instructions, Claude Skills, and other platform packages. |
| [`instructions/`](instructions/) | Step-by-step setup guides for Claude, ChatGPT, Gemini, and generic system prompts. |
| [`test-harness/`](test-harness/) | CLI workbench for testing the methodology against real questions across Claude, GPT, and Gemini. Uses Google Sheets as a data store. |

## License

[MIT](LICENSE)
