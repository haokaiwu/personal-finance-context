# Test Harness

A CLI workbench for testing the financial context methodology against real questions across multiple AI models (Claude, GPT, Gemini). Uses Google Sheets as the data store for questions, profiles, sessions, and analysis results.

## Architecture

```
Google Sheet (data store)          CLI (workbench)
┌─────────────────────┐            ┌──────────────────┐
│ Questions (manual)   │◄──────────│ add-question      │
│ Profiles  (manual)   │◄──────────│ gen-profile       │
│ Sessions  (append)   │◄──────────│ start / reply     │
│ Turns     (append)   │◄──────────│   / inject        │
│ Analysis  (append)   │◄──────────│ check-* / tag     │
│ Logs      (append)   │◄──────────│ (auto-logged)     │
└─────────────────────┘            └──────────────────┘
                                          │
                                   ┌──────┴──────┐
                                   │ Model APIs  │
                                   │ Anthropic   │
                                   │ OpenAI      │
                                   │ Google      │
                                   └─────────────┘
```

## Setup

### 1. Create virtual environment and install dependencies

```bash
cd test-harness
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# or: .venv/bin/pip install -r requirements.txt  # macOS/Linux
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

You need at least one model API key. All three are optional — you only need keys for providers you want to test:

| Variable | Required for |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Claude models |
| `OPENAI_API_KEY` | GPT models |
| `GOOGLE_API_KEY` | Gemini models |

The methodology path defaults to `../methodology` (the sibling folder). Override with `METHODOLOGY_DIR` in `.env` if needed.

### 3. Google Sheets setup

1. Create a Google Cloud project with the **Google Sheets API** and **Google Drive API** enabled
2. Create a service account and download its JSON key file
3. Place the key file in `test-harness/` as `service-account.json` (or set `GOOGLE_SERVICE_ACCOUNT_FILE` in `.env`)
4. Create a blank Google Sheet (any name — set `GOOGLE_SHEET_NAME` in `.env`, defaults to "WorthiQ Test Harness")
5. Share the sheet with your service account email (Editor access)
6. Run: `.venv/Scripts/python cli.py setup`

This creates 6 tabs: Questions, Profiles, Sessions, Turns, Analysis, Logs.

### 4. Add test data

You can add questions and profiles in two ways:

**Directly in the sheet** — After `setup` creates the tabs, edit the Questions and Profiles tabs by hand. This is the easiest way to bulk-import questions from Reddit or other sources. Just make sure each row has a unique integer `id`.

**Via CLI** — Use `add-question` or `gen-profile` commands (see Usage below).

## Usage

All commands run from the `test-harness/` directory using the venv:

```bash
# Shorthand (set once per terminal session)
alias wiq=".venv/Scripts/python cli.py"
```

### Setup & maintenance

```bash
wiq setup                          # Initialize sheet tabs
wiq refresh --all                  # Clear Sessions/Turns/Analysis/Logs
wiq refresh --logs                 # Clear only Logs
wiq models                         # List available models
```

### Create test inputs

```bash
# Add questions via CLI (or edit the Questions tab directly in the sheet)
wiq add-question -t "Should I quit my job to start a business?" -e yes -s personalfinance
wiq add-question -t "What is a Roth IRA?" -e no
wiq add-question -t "What should I do about my tax situation?" -e recognized_not_supported

# Generate a synthetic profile (saved to Profiles tab — editable in the sheet)
wiq gen-profile -c "30yo married couple, dual income, anxious about house"
```

### Run sessions

```bash
wiq start -m claude-sonnet-4-5 -c with -q 1       # Start with methodology
wiq start -m gpt-4o -c without -q 1               # Start without (control)
wiq reply -s 1 -t "I'm 28, married, make 120k"    # Reply manually
wiq inject -s 1 -p 3                               # Reply using profile #3
wiq end -s 1                                       # Mark session complete
```

### Analyze

```bash
wiq check-activation -s 1                          # Did it activate correctly?
wiq check-questions -s 1                           # Did it ask the right things?
wiq check-response -s 1                            # Answer + caveat + invitation?
wiq tag -s 1 --stage activation --notes "Good" --score 5  # Manual tag
```

### Review & export

```bash
wiq show -s 1                                      # Show full conversation
wiq compare --a 1 --b 2                            # Side-by-side comparison
wiq list sessions                                  # List all sessions
wiq list analysis                                  # List all analysis results
wiq export analysis -o results.json                # Export to JSON
```

## Test Workflows

### Activation testing

Does the model correctly recognize when to activate the methodology?

```bash
# 1. Add questions with different expected activations (or edit in sheet)
wiq add-question -t "Should I take a 20% pay cut to work remotely?" -e yes
wiq add-question -t "What is a Roth IRA?" -e no
wiq add-question -t "What should I do about my tax situation?" -e recognized_not_supported

# 2. Run each through the methodology
wiq start -m claude-sonnet-4-5 -c with -q 1
wiq check-activation -s 1

# 3. Compare with vs. without
wiq start -m claude-sonnet-4-5 -c without -q 1
wiq compare --a 1 --b 2
```

### Full conversation with inject

Test the full context-gathering and response cycle using a generated persona.

```bash
# 1. Generate a persona (or create one manually in the Profiles tab)
wiq gen-profile -c "late 20s, single, tech salary, wants to buy a condo"

# 2. Start session with a matching question
wiq start -m claude-sonnet-4-5 -c with -q 5

# 3. Model asks follow-up questions → inject profile data
wiq inject -s 3 -p 1

# 4. Continue manually if needed
wiq reply -s 3 -t "I also have about 30k in student loans"

# 5. Run full analysis
wiq check-questions -s 3
wiq check-response -s 3
wiq end -s 3
```

## Sheet Structure

| Tab | Editable by | Purpose |
|-----|-------------|---------|
| **Questions** | You (manual or CLI) | Test questions with expected activation tags |
| **Profiles** | You (manual or CLI) | Financial personas for `inject` — manual or AI-generated |
| **Sessions** | CLI (append) | Session metadata (model, condition, status) |
| **Turns** | CLI (append) | Conversation turn history |
| **Analysis** | CLI (append) | Evaluation results (LLM-as-judge + manual tags) |
| **Logs** | CLI (append) | Error traces and info logs |

### Questions columns

`id` · `text` · `source_url` · `subreddit` · `topic_category` · `expected_activation` · `edge_cases` · `notes`

The `expected_activation` field should be `yes`, `no`, or `recognized_not_supported`. The `check-activation` analyzer compares against this.

### Profiles columns

`id` · `name` · `age` · `income` · `net_worth` · `partnership` · `dependents` · `feelings` · `location` · `goals` · `debts` · `milestones` · `is_synthetic` · `notes`

Generated profiles have `is_synthetic = TRUE`. You can create or edit profiles directly in the sheet.

## Models

| Name | Provider | Notes |
|------|----------|-------|
| `claude-sonnet-4-5` | Anthropic | Default. Good balance of quality/cost |
| `claude-haiku-4-5` | Anthropic | Fast/cheap for volume testing |
| `claude-opus-4` | Anthropic | Highest quality |
| `gpt-4o` | OpenAI | Main GPT model |
| `gpt-4o-mini` | OpenAI | Fast/cheap |
| `o3-mini` | OpenAI | Reasoning model |
| `gemini-2.0-flash` | Google | Fast |
| `gemini-2.5-pro` | Google | Highest quality |
