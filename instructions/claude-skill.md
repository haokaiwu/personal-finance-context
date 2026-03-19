# Claude Skill Setup

Use Claude Code's [Skill](https://code.claude.com/docs/en/skills) feature to get context-aware financial guidance that loads topic-specific content automatically.

## What you need

- [Claude Code](https://code.claude.com) installed
- The files from this repository (download or clone it)

## Setup

### 1. Copy the skill folder

Copy `toolkit/claude-skill/` to your Claude skills directory:

- **Mac/Linux:** `~/.claude/skills/personal-finance/`
- **Windows:** `%USERPROFILE%\.claude\skills\personal-finance\`

The folder contains the SKILL.md (methodology + frontmatter) and all category reference files:

```
personal-finance/
├── SKILL.md
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

### 2. Restart Claude

Close and reopen Claude (or Claude Code) so it picks up the new skill.

### 3. Start a conversation

Ask a financial question. Claude will auto-invoke the skill and ask you follow-up questions before giving advice.

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
