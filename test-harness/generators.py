"""Generator tools: create test profiles and import questions."""

import json
from typing import Optional

from models import get_adapter
from sheets import get_store

# ── Profile generation ────────────────────────────────────────────────

_PROFILE_SYSTEM = """You are a persona generator for financial advice testing.
Generate a realistic financial persona as JSON with exactly these keys:
  name, age, income, net_worth, partnership, dependents,
  feelings, location, goals, debts, milestones

Rules:
- age: integer
- income, net_worth: integers (annual USD)
- partnership: one of "single", "married", "partnered", "divorced", "widowed"
- dependents: integer
- feelings: a short paragraph describing their emotional relationship with money
- location: city, state
- goals: 1-3 sentence description
- debts: brief summary or "none"
- milestones: upcoming life events, or "none planned"

If constraints are provided, incorporate them. Otherwise invent a coherent persona.
Return ONLY valid JSON, no markdown fences."""


def gen_profile(
    constraints: str = "",
    model: str = "claude-sonnet-4-5",
) -> dict:
    """Generate a synthetic persona and save it to the Profiles sheet.

    Args:
        constraints: free-text constraints like "late 20s, high income, anxious about money"
        model: which model to use for generation

    Returns:
        The saved profile dict including its assigned id.
    """
    store = get_store()
    adapter = get_adapter(model)

    prompt = "Generate a financial persona."
    if constraints:
        prompt += f"\n\nConstraints: {constraints}"

    resp = adapter.send(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=_PROFILE_SYSTEM,
    )

    data = json.loads(resp.content)

    profile_id = store.next_id("Profiles")
    row = {
        "id": profile_id,
        "name": data.get("name", ""),
        "age": data.get("age", ""),
        "income": data.get("income", ""),
        "net_worth": data.get("net_worth", ""),
        "partnership": data.get("partnership", ""),
        "dependents": data.get("dependents", ""),
        "feelings": data.get("feelings", ""),
        "location": data.get("location", ""),
        "goals": data.get("goals", ""),
        "debts": data.get("debts", ""),
        "milestones": data.get("milestones", ""),
        "is_synthetic": "TRUE",
        "notes": f"Generated with {model}. Constraints: {constraints or 'none'}",
    }

    store.append_row("Profiles", row)
    store.log_info(f"Generated profile id={profile_id} name={row['name']}")
    return row


# ── Question import ───────────────────────────────────────────────────

def add_question(
    text: str,
    expected_activation: str = "yes",
    source_url: str = "",
    subreddit: str = "",
    topic_category: str = "",
    edge_cases: str = "",
    notes: str = "",
) -> dict:
    """Manually add a question to the Questions sheet.

    Returns:
        The saved question dict.
    """
    store = get_store()
    q_id = store.next_id("Questions")
    row = {
        "id": q_id,
        "text": text,
        "source_url": source_url,
        "subreddit": subreddit,
        "topic_category": topic_category,
        "expected_activation": expected_activation,
        "edge_cases": edge_cases,
        "notes": notes,
    }
    store.append_row("Questions", row)
    store.log_info(f"Added question id={q_id}")
    return row
