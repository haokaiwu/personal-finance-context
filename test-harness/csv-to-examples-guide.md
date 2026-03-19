# Converting Test Harness CSV to Markdown Examples

## Prerequisites

- Python 3 with `pandas`
- A CSV export from the WorthIQ test harness batch runner

## Expected CSV Format

The script expects these columns:

| Column | Description |
| --- | --- |
| `batch_id` | Unique batch identifier (e.g. `B-20260318-160636`) |
| `question_id` | Numeric question ID |
| `question_text` | The full user question (same across all rows) |
| `turn` | Turn number (1, 2, 3, 4...) |
| `{MODEL}-{MODALITY}` | Response text for each model × modality combination |

Model prefixes: `OPS` (Claude Opus), `SNT` (Claude Sonnet), `GPT`, `GMN` (Gemini)

Modality suffixes: `without`, `general`, `category`

So response columns are: `OPS-without`, `OPS-general`, `OPS-category`, `SNT-without`, etc.

Turn numbering: odd turns are user messages, even turns are model responses. Turn 1 is always the original question. `NaN` values indicate the conversation ended (e.g. "without" modality is single-turn, so turns 3–4 are `NaN`).

## Output Structure

```
examples/
└── {question-slug}/
    ├── README.md                              ← landing page with table
    ├── claude-opus_without-guidance.md
    ├── claude-opus_general-methodology.md
    ├── claude-opus_category-specific.md
    ├── claude-sonnet_without-guidance.md
    ├── claude-sonnet_general-methodology.md
    ├── claude-sonnet_category-specific.md
    ├── gpt_without-guidance.md
    ├── gpt_general-methodology.md
    ├── gpt_category-specific.md
    ├── gemini_without-guidance.md
    ├── gemini_general-methodology.md
    └── gemini_category-specific.md
```

## The Script

Save this as `csv_to_examples.py` and run it with:

```bash
python3 csv_to_examples.py path/to/batch.csv "question-slug-goes-here"
```

```python
#!/usr/bin/env python3
"""
Convert a WorthIQ test harness batch CSV into a folder of
markdown conversation files + a README with a linking table.

Usage:
    python3 csv_to_examples.py <csv_path> <folder_slug>

Example:
    python3 csv_to_examples.py exports/batch.csv personal-finance-25yo-married-socal
"""

import sys
import os
import pandas as pd

# ---------------------------------------------------------------------------
# Config: models and modalities
# ---------------------------------------------------------------------------

MODELS = {
    "OPS": {"label": "Claude Opus",   "slug": "claude-opus"},
    "SNT": {"label": "Claude Sonnet", "slug": "claude-sonnet"},
    "GPT": {"label": "GPT",           "slug": "gpt"},
    "GMN": {"label": "Gemini",        "slug": "gemini"},
}

MODALITIES = {
    "without":  {"label": "Without Guidance",           "slug": "without-guidance"},
    "general":  {"label": "With General Methodology",   "slug": "general-methodology"},
    "category": {"label": "With Category-Specific Files","slug": "category-specific"},
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Normalize line endings from CSV export."""
    return text.replace("\\r\\n", "\n").replace("\r\n", "\n")


def get_conversation(df: pd.DataFrame, model_key: str, mod_key: str) -> list:
    """Extract non-NaN turns for a given model × modality."""
    col = f"{model_key}-{mod_key}"
    turns = []
    for _, row in df.iterrows():
        val = row[col]
        if pd.isna(val):
            continue
        turns.append((int(row["turn"]), clean_text(str(val))))
    return turns


def build_conversation_md(turns: list, model_label: str) -> list:
    """
    Format a list of (turn_number, text) into markdown lines.
    Odd turns = User, even turns = Model.
    User messages are blockquoted; model responses are raw markdown.
    """
    lines = []
    for turn_num, text in turns:
        if turn_num % 2 == 1:  # user
            lines.append("### User")
            lines.append("")
            lines.append("> " + text.replace("\n", "\n> "))
            lines.append("")
        else:  # model
            lines.append(f"### {model_label}")
            lines.append("")
            lines.append(text)
            lines.append("")
    return lines


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def write_conversation_file(
    filepath: str,
    model_label: str,
    mod_label: str,
    turns: list,
    batch_id: str,
    question_title: str,
):
    lines = [
        f"# {model_label} — {mod_label}",
        "",
        f"**Question:** {question_title}",
        f"**Turns:** {len(turns)} | **Batch:** `{batch_id}`",
        "",
        "---",
        "",
    ]
    lines.extend(build_conversation_md(turns, model_label))

    with open(filepath, "w") as f:
        f.write("\n".join(lines))


def write_readme(
    folder: str,
    question_text: str,
    question_title: str,
    batch_id: str,
    question_id: int,
    turn_counts: dict,
):
    lines = [
        f"# {question_title}",
        "",
        f"**Batch:** `{batch_id}` | **Question ID:** `{question_id}`",
        "",
        "## Question",
        "",
        "> " + question_text.replace("\n", "\n> "),
        "",
        "## Responses",
        "",
        "| Model | Without Guidance | General Methodology | Category-Specific |",
        "| :--- | :---: | :---: | :---: |",
    ]

    for model_key, model_info in MODELS.items():
        row = f"| **{model_info['label']}** "
        for mod_key, mod_info in MODALITIES.items():
            filename = f"{model_info['slug']}_{mod_info['slug']}.md"
            turns = turn_counts[(model_key, mod_key)]
            row += f"| [{turns}-turn](./{filename}) "
        row += "|"
        lines.append(row)

    lines.extend([
        "",
        "## What You're Looking At",
        "",
        "Each link above is a full conversation transcript. The three columns represent increasing levels of methodology applied to the model:",
        "",
        "1. **Without Guidance** — The model gets the question cold, with no methodology or context files",
        "2. **General Methodology** — The model receives the [universal personal finance context framework](https://github.com/haokaiwu/personal-finance-context)",
        "3. **Category-Specific** — The model receives both the universal framework and scenario-specific guidance files",
        "",
    ])

    with open(os.path.join(folder, "README.md"), "w") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 csv_to_examples.py <csv_path> <folder_slug>")
        print("Example: python3 csv_to_examples.py batch.csv personal-finance-25yo-socal")
        sys.exit(1)

    csv_path = sys.argv[1]
    folder_slug = sys.argv[2]
    output_dir = os.path.join("examples", folder_slug)

    # Read CSV
    df = pd.read_csv(csv_path)

    # Extract metadata from turn 1
    question_text = clean_text(df.loc[df["turn"] == 1, "question_text"].values[0])
    batch_id = df["batch_id"].values[0]
    question_id = int(df["question_id"].values[0])

    # Derive a human-readable title from the slug
    question_title = folder_slug.replace("-", " ").title()

    os.makedirs(output_dir, exist_ok=True)

    # Write 12 conversation files + collect turn counts
    turn_counts = {}
    for model_key, model_info in MODELS.items():
        for mod_key, mod_info in MODALITIES.items():
            turns = get_conversation(df, model_key, mod_key)
            turn_counts[(model_key, mod_key)] = len(turns)

            filename = f"{model_info['slug']}_{mod_info['slug']}.md"
            filepath = os.path.join(output_dir, filename)

            write_conversation_file(
                filepath=filepath,
                model_label=model_info["label"],
                mod_label=mod_info["label"],
                turns=turns,
                batch_id=batch_id,
                question_title=question_title,
            )

    # Write README
    write_readme(
        folder=output_dir,
        question_text=question_text,
        question_title=question_title,
        batch_id=batch_id,
        question_id=question_id,
        turn_counts=turn_counts,
    )

    # Report
    print(f"\nCreated {len(os.listdir(output_dir))} files in {output_dir}/\n")
    for f in sorted(os.listdir(output_dir)):
        size = os.path.getsize(os.path.join(output_dir, f))
        print(f"  {f:50s} {size:>8,} bytes")


if __name__ == "__main__":
    main()
```

## Step-by-Step: What the Script Does

1. **Reads the CSV** into a pandas DataFrame (4 rows = 4 turns, 16 columns).

2. **Extracts metadata** from turn 1: the question text, batch ID, and question ID.

3. **Loops through all 12 combinations** (4 models × 3 modalities). For each:
   - Pulls every non-`NaN` turn from that column
   - Formats user messages (odd turns) as blockquoted markdown (`> ...`)
   - Leaves model responses (even turns) as raw markdown so their original formatting is preserved
   - Writes one `.md` file per conversation

4. **Writes the README** with the question as a blockquote and a 4×3 table linking to each conversation file with turn counts.

## Adding a New Question

```bash
# Export a new batch from the test harness
python3 csv_to_examples.py exports/new-batch.csv debt-payoff-strategy-30yo-dual-income
```

This creates `examples/debt-payoff-strategy-30yo-dual-income/` with 13 files.

## Customizing

**To add metadata columns to the README table** (e.g. scores, word counts), edit the `write_readme` function's table-building loop. The table header and row format are just string concatenation — add columns as needed.

**To add or remove models**, edit the `MODELS` dict at the top of the script. The key must match the CSV column prefix.

**To change the question title**, pass a better slug or edit `question_title` derivation in `main()`. Currently it just title-cases the slug.
