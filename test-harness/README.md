# WorthiQ Test Harness

A CLI workbench for testing WorthiQ's financial context methodology against real questions across multiple AI models (Claude, GPT, Gemini).

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

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys and service account path
```

### 3. Google Sheets setup

1. Create a Google Cloud service account with Sheets API enabled
2. Download the JSON key file and set `GOOGLE_SERVICE_ACCOUNT_FILE` in `.env`
3. Create a blank Google Sheet named "WorthiQ Test Harness" (or set `GOOGLE_SHEET_NAME`)
4. Share the sheet with your service account email (Editor access)
5. Run: `python cli.py setup`

### 4. Add methodology

Place your methodology `.md` files in the `./methodology/` directory. All `.md` files are concatenated as the system prompt for the "with" condition. The "without" condition uses no system prompt (model default).

## Usage

### Quick reference

```bash
# Alias for convenience
alias wiq="python cli.py"

# Setup & maintenance
wiq setup                          # Initialize sheet tabs
wiq refresh --all                  # Clear Sessions/Turns/Analysis/Logs
wiq refresh --logs                 # Clear only Logs
wiq models                        # List available models

# Create test inputs
wiq gen-profile -c "30yo married couple, dual income, anxious about house"
wiq add-question -t "Should I quit my job to start a business?" -e yes -s personalfinance

# Run sessions
wiq start -m claude-sonnet-4-5 -c with -q 1       # Start with methodology
wiq start -m gpt-4o -c without -q 1              # Start without (control)
wiq reply -s 1 -t "I'm 28, married, make 120k"   # Reply manually
wiq inject -s 1 -p 3                             # Reply using profile #3
wiq end -s 1                                     # Mark session complete

# Analyze
wiq check-activation -s 1                        # Did it activate correctly?
wiq check-questions -s 1                         # Did it ask the right things?
wiq check-response -s 1                          # Answer + caveat + invitation?
wiq tag -s 1 --stage activation --notes "Good" --score 5  # Manual tag

# Review
wiq show -s 1                                    # Show full conversation
wiq compare --a 1 --b 2                          # Side-by-side comparison
wiq list sessions                                # List all sessions
wiq list analysis                                # List all analysis results
wiq export analysis -o results.json              # Export to JSON
```

### Test workflow: Activation testing

```bash
# 1. Import questions (some should activate, some shouldn't)
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

### Test workflow: Full conversation with inject

```bash
# 1. Generate a persona
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

## Sheet structure

| Tab | Editable by | Purpose |
|-----|-------------|---------|
| Questions | You (manual) | Test questions with expected activation tags |
| Profiles | You + CLI | Financial personas (manual or generated) |
| Sessions | CLI (append) | Session metadata |
| Turns | CLI (append) | Conversation turn history |
| Analysis | CLI (append) | Evaluation results (LLM + manual) |
| Logs | CLI (append) | Error traces and info logs |

## Models

| Name | Provider | Notes |
|------|----------|-------|
| claude-sonnet-4-5 | Anthropic | Default. Good balance of quality/cost |
| claude-haiku-4-5 | Anthropic | Fast/cheap for volume testing |
| claude-opus-4 | Anthropic | Highest quality |
| gpt-4o | OpenAI | Main GPT model |
| gpt-4o-mini | OpenAI | Fast/cheap |
| o3-mini | OpenAI | Reasoning model |
| gemini-2.0-flash | Google | Fast |
| gemini-2.5-pro | Google | Highest quality |
