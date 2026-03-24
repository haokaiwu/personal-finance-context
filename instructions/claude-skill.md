# Claude Skill Setup

Add the methodology to Claude as a Skill so it automatically kicks in whenever you ask a financial question.

## What you need

- A Claude account at [claude.ai](https://claude.ai)
- The skill files from this repository inside toolkit/claude-skill

## Setup

### 1. Download the skill

Download/clone the repository. The files are inside the `toolkit/claude-skill` folder.

### 2. Upload the skill to Claude

1. Open [claude.ai](https://claude.ai)
2. In the left panel, click **Customize**
3. Click **Skills**
4. Click the **+** button
5. Click **Upload a skill**
6. Drop in the `claude-skill` folder (or browse to select it)

### 3. Restart Claude

Close Claude completely and reopen it so the skill takes effect.

### 4. Start a conversation

Ask a financial question. Claude will automatically activate the skill and ask you follow-up questions before giving advice — no need to mention the skill or do anything special.

## Tips

- The skill activates automatically when Claude detects a financial question. You don't need to turn it on or refer to it.
- If you update to a newer version of the skill, repeat the upload steps above — the new version will replace the old one.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
