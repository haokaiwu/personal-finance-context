# Claude Skill Setup

Use Claude Code's [Skill](https://code.claude.com/docs/en/skills) feature to get context-aware financial guidance that loads topic-specific content automatically.

> **Note:** A pre-packaged skill folder is coming soon. For now, follow the manual setup below — it takes about 5 minutes.

## What you need

- [Claude Code](https://code.claude.com) installed
- The files from this repository (download or clone it)

## Setup

### 1. Create the skill directory

On your computer, create a folder for the skill. The exact location depends on your OS:

- **Mac/Linux:** `~/.claude/skills/personal-finance/`
- **Windows:** `%USERPROFILE%\.claude\skills\personal-finance\`

### 2. Create the SKILL.md file

Inside that folder, create a file called `SKILL.md` with this content:

```markdown
---
name: personal-finance
description: Gathers financial context before giving advice. Asks targeted questions, flags risks, and gives direct guidance.
---

```

Then paste the entire contents of `methodology/methodology-master-doc.md` below the frontmatter block (after the closing `---`).

### 3. Add topic files (recommended)

For topic-specific questions and red flags, create a `references/` subdirectory inside your skill folder and copy the category files into it:

```
personal-finance/
├── SKILL.md
└── references/
    ├── loading-protocol.md
    ├── career/
    │   └── career-overview.md
    ├── spending/
    │   └── spending-overview.md
    ├── life-events/
    │   └── life-events-overview.md
    ├── investing/
    │   └── investing-overview.md
    └── assessment/
        └── assessment-overview.md
```

Copy these files directly from the `methodology/` folder in this repository, keeping the folder structure.

Claude automatically surfaces resources from the `references/` directory when they're relevant, so it will pull in the right topic file based on what you're asking about.

### 4. Restart Claude

Close and reopen Claude (or Claude Code) so it picks up the new skill.

## Tips

- The `name` must be 64 characters or fewer, using only lowercase letters, numbers, and hyphens. The `description` should be concise — Claude uses it to decide when to auto-load the skill.
- SKILL.md should stay under 500 lines. The master doc fits well within this. Detailed topic files go in supporting directories, not in SKILL.md itself.
- You don't need `implementation-guide.md` or `methodology/README.md` — those are for developers, not for the AI.
- If you update the methodology files later, just copy the new versions into the same locations. Claude picks up changes on the next session.
- See the [official Skills documentation](https://code.claude.com/docs/en/skills) for advanced options like argument hints, tool permissions, and auto-invocation settings.

## Test that it works

1. **Ask a financial question** (e.g., "Should I take this job offer?") — the AI should ask you questions before answering.
2. **Try a different topic** (e.g., "What about my retirement savings?") — the AI should adjust its questions.
3. **Describe a red-flag scenario** (e.g., "I'm putting all my savings into one stock") — the AI should suggest seeing a professional.
