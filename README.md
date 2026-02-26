# Financial Context Toolkit

A toolkit for improving the quality of AI responses to questions with financial implications. Built by [WorthIQ](https://worthiq.app).

## What This Is

People ask AI for advice even when they shouldn't.

Rather than fighting human nature, this toolkit helps people do it more safely while getting better results. Namely, it fixes AI tendency to provide an answer right away without asking for important context. This default behavior is harmful for questions adjacent to personal finance because the "best answers" change dramatically depending on the context.

Therefore, this toolkit is primarily a context engine, forcing the AI to ask you for critical context before answering. It incorporates this context into its answers, and it follows best practices for considering the objective facts like the amount of money in your bank account alongside how you feel.

Finally, it lightly "jailbreaks" the AI to answer questions that aren't financial advice but might get censored due to overzealous guardrails. For example, "Should I save more money per month?" isn't financial advice, but it might get flagged as such.

## Disclaimers

###NO financial advice 

No, this won't jailbreak your AI to give you crypto ideas or stock trading tips. It has specific instructions to avoid this behavior. Rule of thumb: any specific recommendations on securities or asset allocation will be rejected in favor of general advice.

###NO perfect answers 

Someday AI may be our superintelligent overlords, but that day hasn't come yet. These instructions will give you better results, but they don't guarantee perfection. Use with caution.

## Repository Structure

| Folder | What's in it |
|--------|-------------|
| [`methodology/`](methodology/) | The core methodology — AI instructions for gathering financial context and delivering personalized guidance. This is the main asset. |
| [`test-harness/`](test-harness/) | CLI workbench for testing the methodology against real questions across Claude, GPT, and Gemini. Uses Google Sheets as a data store. |

## Goals

- **Context-first responses** — Gather relevant financial details before answering, not after
- **Direct, opinionated guidance** — Override trained hedging behavior with clear recommendations
- **Structured topic coverage** — Consistent data-point checklists across 6 financial domains
- **Red flag detection** — Know when to recommend a professional instead of answering
- **Platform-agnostic** — Deploy as a Claude Skill, Custom GPT, Gemini Gem, or raw prompt
- **Testable** — Compare with vs. without methodology across models

## Status

Early stage. The core methodology and test harness are complete. Platform-specific implementations, example conversations, and contribution guidelines are coming soon.

## License

[MIT](LICENSE)
