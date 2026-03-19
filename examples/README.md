# Examples

Real conversations between AI models and users asking financial questions. Each example starts with a real question from [r/personalfinance](https://www.reddit.com/r/personalfinance/) and shows how four different models respond — with and without the methodology loaded.

## Examples

| Example | Topic |
|---------|-------|
| [55k in savings, beginner investor](investing-55k-savings-beginner/) | What to do with idle savings, no investing experience |
| [Financial review, 29yo in NY](financial-review-29yo-ny/) | Top-down financial review with detailed budget breakdown |
| [Savings & Roth IRA, 25yo married in SoCal](savings-roth-ira-advice-25yo-socal/) | Optimizing surplus income, credit cards, emergency fund vs. Roth IRA |

## Structure

Each example folder contains:

- **README.md** — The original question, source link, and a table linking to all conversations
- **12 conversation files** — One per model/mode combination, named `{model}_{mode}.md`

The 12 files cover a grid of 4 models and 3 modes:

**Models:** Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.4, Gemini 3.1 Pro

**Modes:**

| Mode | What the model receives |
|------|------------------------|
| Without Guidance | The question only — no methodology or context files |
| General Methodology | The question + the [master methodology document](../methodology/methodology-master-doc.md) |
| Category-Specific | The question + the master document + topic-specific category files |

In "without" mode, models typically answer immediately with generic advice. With the methodology loaded, models ask follow-up questions to understand the user's situation before giving personalized guidance. The category-specific mode adds deeper, topic-relevant questions and red flags.