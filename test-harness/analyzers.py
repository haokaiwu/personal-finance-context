"""Analyzer tools: check activation, question quality, response structure."""

import json
from datetime import datetime, timezone
from typing import Optional

from models import get_adapter
from sheets import get_store


def _get_session_turns(session_id: str) -> list[dict]:
    store = get_store()
    all_turns = store.get_all("Turns")
    session_turns = [
        t for t in all_turns if str(t["session_id"]) == str(session_id)
    ]
    session_turns.sort(key=lambda t: int(t["turn_number"]))
    return session_turns


def _save_analysis(
    session_id: str,
    stage: str,
    method: str,
    result: dict,
    notes: str = "",
):
    store = get_store()
    store.append_row("Analysis", {
        "id": store.next_id("Analysis"),
        "session_id": session_id,
        "stage": stage,
        "method": method,
        "result": json.dumps(result),
        "notes": notes,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })


# ── Check: Activation ────────────────────────────────────────────────

_ACTIVATION_JUDGE_PROMPT = """You are evaluating whether an AI financial advisor correctly activated
a financial context methodology. Activation means the AI:
1. Recognized the question has personal financial implications
2. Signaled it would ask follow-up questions before answering
3. Did NOT just answer directly without gathering context

The user's question was:
---
{question}
---

The AI's first response was:
---
{response}
---

Evaluate and return ONLY valid JSON (no markdown fences):
{{
  "activated": true/false,
  "signaled_followup": true/false,
  "asked_questions": true/false,
  "went_straight_to_advice": true/false,
  "explanation": "brief explanation"
}}"""


def check_activation(
    session_id: str,
    method: str = "llm",
    judge_model: str = "claude-sonnet-4-5",
) -> dict:
    """Check if the model correctly activated (or didn't) for this session.

    Args:
        session_id: session to evaluate
        method: "manual" (just records your input) or "llm" (uses a judge model)
        judge_model: which model to use as judge

    Returns:
        Analysis result dict.
    """
    store = get_store()
    session = store.get_by_id("Sessions", session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found")

    turns = _get_session_turns(session_id)
    if len(turns) < 2:
        raise ValueError("Session needs at least a user turn and assistant turn")

    question = turns[0]["content"]
    first_response = turns[1]["content"]

    # Look up expected activation
    expected = ""
    if session.get("question_id"):
        q = store.get_by_id("Questions", session["question_id"])
        if q:
            expected = q.get("expected_activation", "")

    if method == "llm":
        adapter = get_adapter(judge_model)
        prompt = _ACTIVATION_JUDGE_PROMPT.format(
            question=question, response=first_response,
        )
        resp = adapter.send(
            messages=[{"role": "user", "content": prompt}],
        )
        result = json.loads(resp.content)
        result["expected_activation"] = expected
        result["match"] = (
            (expected == "yes" and result.get("activated"))
            or (expected == "no" and not result.get("activated"))
            or expected == ""
        )
    else:
        # Manual: return the data for the user to evaluate
        result = {
            "question_preview": question[:200],
            "response_preview": first_response[:500],
            "expected_activation": expected,
            "note": "Use 'tag' command to record your manual evaluation.",
        }

    _save_analysis(session_id, "activation", method, result)
    store.log_info(f"Activation check for session {session_id}: {method}", session_id)
    return result


# ── Check: Question Quality ──────────────────────────────────────────

_QUESTIONS_JUDGE_PROMPT = """You are evaluating whether an AI financial advisor asked the right
follow-up questions before giving advice. The methodology requires:

REQUIRED data points (should ask for ALL upfront):
- Goal: what the user is trying to accomplish
- Expected role: what the user expects from the AI
- Feelings: emotional state about the financial topic
- Age (range ok)
- Partnership situation
- Dependents
- Annual income (range ok)
- Total net worth (range ok)

RECOMMENDED data points (should surface through caveats, not upfront):
- Monthly savings, debt sources, cash on hand, planned milestones,
  location, retirement accounts, investment allocation

Review ALL assistant messages in this conversation and return ONLY valid JSON:
{{
  "required_asked": ["list of required data points that were asked for"],
  "required_missing": ["list of required data points NOT asked for"],
  "feelings_addressed": true/false,
  "feelings_quality": "brief assessment of how feelings were handled",
  "recommended_surfaced": ["list of recommended data points surfaced as caveats"],
  "asked_too_much_upfront": true/false,
  "overall_score": 1-5,
  "explanation": "brief explanation"
}}

The conversation:
---
{conversation}
---"""


def check_questions(
    session_id: str,
    method: str = "llm",
    judge_model: str = "claude-sonnet-4-5",
) -> dict:
    """Evaluate the quality of follow-up questions in a session.

    Returns:
        Analysis result dict.
    """
    store = get_store()
    turns = _get_session_turns(session_id)

    conversation = "\n\n".join(
        f"**{t['role'].upper()}**: {t['content']}" for t in turns
    )

    if method == "llm":
        adapter = get_adapter(judge_model)
        prompt = _QUESTIONS_JUDGE_PROMPT.format(conversation=conversation)
        resp = adapter.send(
            messages=[{"role": "user", "content": prompt}],
        )
        result = json.loads(resp.content)
    else:
        result = {
            "conversation_preview": conversation[:2000],
            "note": "Use 'tag' command to record your manual evaluation.",
        }

    _save_analysis(session_id, "questions", method, result)
    store.log_info(f"Questions check for session {session_id}: {method}", session_id)
    return result


# ── Check: Response Quality ──────────────────────────────────────────

_RESPONSE_JUDGE_PROMPT = """You are evaluating a financial advisor AI's final response.
The methodology requires every response to include:

1. ANSWER: Best advice based on context provided
2. CAVEAT: How 1-2 specific missing data points could change the answer
3. INVITATION: Invite the user to provide those specific data points

Also evaluate:
- Tone: conversational, warm, direct, empathetic?
- Did it weigh feelings alongside numbers?
- Did it avoid universal prescriptions?
- Did it catch any red flags that warrant professional referral?

Return ONLY valid JSON:
{{
  "has_answer": true/false,
  "has_caveat": true/false,
  "caveat_specific": true/false,
  "has_invitation": true/false,
  "tone_appropriate": true/false,
  "feelings_weighted": true/false,
  "avoids_prescriptions": true/false,
  "red_flags_caught": "list or 'none detected'",
  "overall_score": 1-5,
  "explanation": "brief explanation"
}}

The full conversation:
---
{conversation}
---"""


def check_response(
    session_id: str,
    method: str = "llm",
    judge_model: str = "claude-sonnet-4-5",
) -> dict:
    """Evaluate the response quality of a completed session.

    Returns:
        Analysis result dict.
    """
    store = get_store()
    turns = _get_session_turns(session_id)

    conversation = "\n\n".join(
        f"**{t['role'].upper()}**: {t['content']}" for t in turns
    )

    if method == "llm":
        adapter = get_adapter(judge_model)
        prompt = _RESPONSE_JUDGE_PROMPT.format(conversation=conversation)
        resp = adapter.send(
            messages=[{"role": "user", "content": prompt}],
        )
        result = json.loads(resp.content)
    else:
        result = {
            "conversation_preview": conversation[:2000],
            "note": "Use 'tag' command to record your manual evaluation.",
        }

    _save_analysis(session_id, "response", method, result)
    store.log_info(f"Response check for session {session_id}: {method}", session_id)
    return result
