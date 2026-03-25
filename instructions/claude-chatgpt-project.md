# Project Setup (Claude & ChatGPT)

Add the methodology to a project in [Claude](https://support.claude.com/en/articles/9517075-what-are-projects) or [ChatGPT](https://help.openai.com/en/articles/10164163-projects-in-chatgpt) so every conversation in that project gets financial context guidance.

Both platforms work the same way: you set project instructions and upload knowledge files. The steps below apply to either one.

## What you need

- A Claude or ChatGPT account (free or paid — both support projects)
- The files from this repository (download or clone it)

## Setup

### 1. Create a new project

**Claude:** Go to [claude.ai](https://claude.ai), hover over the left sidebar, and click **Projects** → **New Project** on Desktop. On mobile, click the plus sign. 

**ChatGPT:** Go to [chatgpt.com](https://chatgpt.com), open the left sidebar, and click **New Project**.

Give it a name like "Personal Finance Coach" or whatever you want.

### 2. Set the project instructions

Paste the entire contents of [methodology/methodology-master-doc.md](https://raw.githubusercontent.com/haokaiwu/personal-finance-coach/refs/heads/main/methodology/methodology-master-doc.md) into the project instructions field, then save.

**Claude:** Click the Plus button next to the **Instructions** on the right sidebar, paste in the text box, and click **Save instructions**.

**ChatGPT:** Click **Project Instructions** in the top right ... button. In the **Instructions** box, copy and paste. Press save on the bottom right.

That's the basics done. The AI will now ask you targeted questions before giving financial advice.

### 3. Add topic files

First, download the zip folder of the methodology files using this link: 

[https://github.com/haokaiwu/personal-finance-coach/releases/download/latest/methodology-files.zip](https://github.com/haokaiwu/personal-finance-coach/releases/download/latest/methodology-files.zip)

Extract the files from the zip folder, and then copy the files into your project. 

**Claude:** Click the **+** button next to **Files** in the knowledge panel on the right and upload the files.

**ChatGPT:** Click **Sources** beneath the chat window and upload the files.

### 4. Start a conversation

Open a new conversation inside the project and ask a personal finance question. The AI should ask you follow-up questions before giving advice.

## Tips

- You don't need `implementation-guide.md` or `methodology/README.md` — those are for developers, not for the AI.
- Project instructions apply to every conversation in the project, so you can start fresh chats and the methodology carries over.
- If you update the methodology files later, replace the instructions and re-upload the knowledge files.

## Test that it works

1. **Ask a personal finance question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should stick to general pointers while referring you to a professional.
