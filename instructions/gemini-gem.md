# Gemini Gem Setup

Create a Google Gemini [Gem](https://support.google.com/gemini/answer/15236321) that gathers financial context before giving advice.

## What you need

- A Google Gemini account

## Setup

### 1. Create a new Gem

Go to [gemini.google.com](https://gemini.google.com), open the side menu, and click **Gems** → **New Gem**.

### 2. Set up the Gem

- **Name:** Something like "Personal Finance Coach" (your choice)

### 3. Paste the instructions

In the **Instructions** field, paste the entire contents of `methodology/methodology-master-doc.md`.

The master doc is roughly 12,000 characters, which fits within the Gem instruction field. No splitting needed.

That's the basics done.

### 4. Add topic content

First, download the zip folder of the methodology files using this link: 

[https://github.com/haokaiwu/personal-finance-coach/releases/download/latest/methodology-files.zip](https://github.com/haokaiwu/personal-finance-coach/releases/download/latest/methodology-files.zip)

Extract the files from the zip folder. 

In the Gem editor, click **Add files** under the **Knowledge** section and upload all the files.

### 5. Save the Gem

Click **Save**. Your Gem is ready to use.

## Tips

- File uploads (Option A) are the most reliable approach since the content is always available and doesn't eat into your instruction space.
- If pasting everything into the instructions field, the identity framing (top of the master doc) and Sections 2–3 are the most important parts to keep if you run close to the limit.
- See Google's [tips for creating custom Gems](https://support.google.com/gemini/answer/15235603) for more guidance on writing effective Gem instructions.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
