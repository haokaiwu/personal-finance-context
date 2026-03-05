# Claude Project Setup

Add the methodology to a [Claude Project](https://support.claude.com/en/articles/9517075-what-are-projects) so every conversation in that project gets financial context guidance.

## What you need

- A Claude account — free accounts can create up to 5 projects, paid plans (Pro, Max, Team, Enterprise) have no limit
- The files from this repository (download or clone it)

## Setup

### 1. Create a new project

Go to [claude.ai](https://claude.ai), hover over the left sidebar, and click **Projects** → **New Project**. Give it a name like "Financial Advisor" or whatever you want.

### 2. Set the project instructions

Inside the project, click **Set project instructions**. Paste the entire contents of `methodology/methodology-master-doc.md` into the text area, then click **Save instructions**.

That's the basics done. The AI will now ask you targeted questions before giving financial advice.

### 3. Add topic files (recommended)

For topic-specific questions and red flags, click the **+** button in the project's knowledge panel and upload these files:

- `methodology/loading-protocol.md`
- `methodology/career/career-overview.md`
- `methodology/spending/spending-overview.md`
- `methodology/life-events/life-events-overview.md`
- `methodology/investing/investing-overview.md`
- `methodology/assessment/assessment-overview.md`

Project knowledge files are available in context automatically. If you upload more content than fits in the context window, Claude enables retrieval (RAG) behind the scenes — no configuration needed.

### 4. Start a conversation

Open a new conversation inside the project and ask a financial question. The AI should ask you follow-up questions before giving advice.

## Tips

- You don't need `implementation-guide.md` or `methodology/README.md` — those are for developers, not for the AI.
- Project instructions apply to every conversation in the project, so you can start fresh chats and the methodology carries over.
- If you update the methodology files later, replace the instructions and re-upload the knowledge files.
- See [How to create and manage Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) for more details on the project UI.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
