"""Session tools: start conversations, reply, inject profile data."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import METHODOLOGY_DIR, MAX_TURNS, VALID_MODES
from models import get_adapter
from models.base import ModelResponse
from sheets import get_store


def _load_methodology(mode: str) -> str:
    """Load methodology files based on the deployment mode.

    - general: methodology-master-doc.md only
    - category: master doc + loading-protocol.md (categories loaded via tools)
    - category-all: master doc + loading-protocol.md + all category overviews
    """
    md_dir = Path(METHODOLOGY_DIR)
    if not md_dir.exists():
        raise FileNotFoundError(
            f"Methodology directory not found: {md_dir.resolve()}\n"
            "Create the directory and place your .md files in it."
        )

    files: list[Path] = []

    # Master doc is always included
    master = md_dir / "methodology-master-doc.md"
    if not master.exists():
        raise FileNotFoundError(f"Master doc not found: {master.resolve()}")
    files.append(master)

    if mode in ("category", "category-all"):
        # Loading protocol tells the model how to use category files
        protocol = md_dir / "loading-protocol.md"
        if not protocol.exists():
            raise FileNotFoundError(f"Loading protocol not found: {protocol.resolve()}")
        files.append(protocol)

    if mode == "category-all":
        # Load all category overview files into context
        for subdir in sorted(md_dir.iterdir()):
            if subdir.is_dir():
                overview = subdir / f"{subdir.name}-overview.md"
                if overview.exists():
                    files.append(overview)

    parts = [f.read_text() for f in files]
    return "\n\n---\n\n".join(parts)


# ── Category tools (for dynamic loading via tool use) ─────────────────

# Map category names to their overview files
CATEGORY_MAP = {
    "career": "career/career-overview.md",
    "spending": "spending/spending-overview.md",
    "life-events": "life-events/life-events-overview.md",
    "investing": "investing/investing-overview.md",
    "assessment": "assessment/assessment-overview.md",
}

CATEGORY_TOOL = {
    "name": "load_category_context",
    "description": (
        "Load the detailed methodology for a specific financial category. "
        "Call this after identifying which category the user's question falls into. "
        "You may call this multiple times for multi-category questions. "
        "Available categories: "
        "career (job changes, salary, career transitions), "
        "spending (budgeting, purchases, lifestyle decisions), "
        "life-events (emergency funds, major life changes, liquidity needs), "
        "investing (investment strategy, retirement planning, portfolio), "
        "assessment (overall financial health check)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": list(CATEGORY_MAP.keys()),
                "description": "The financial category to load",
            },
        },
        "required": ["category"],
    },
}


def _category_tool_handler(tool_name: str, tool_input: dict) -> str:
    """Handle load_category_context tool calls by returning file contents."""
    if tool_name != "load_category_context":
        return f"Unknown tool: {tool_name}"

    category = tool_input.get("category", "")
    rel_path = CATEGORY_MAP.get(category)
    if not rel_path:
        return f"Unknown category: {category}. Valid: {', '.join(CATEGORY_MAP.keys())}"

    md_dir = Path(METHODOLOGY_DIR)
    file_path = md_dir / rel_path
    if not file_path.exists():
        return f"Category file not found: {file_path}"

    return file_path.read_text()


def _build_system_prompt(mode: str) -> Optional[str]:
    """Return system prompt for the mode, or None for control."""
    if mode == "without":
        return None
    return _load_methodology(mode)


def _build_tools(mode: str) -> Optional[list[dict]]:
    """Return tool definitions for the mode, or None."""
    if mode == "category":
        return [CATEGORY_TOOL]
    return None


def _get_tool_handler(mode: str):
    """Return the tool handler callback for the mode, or None."""
    if mode == "category":
        return _category_tool_handler
    return None


def _get_turns(session_id: str) -> list[dict]:
    """Reconstruct message history from the Turns sheet."""
    store = get_store()
    all_turns = store.get_all("Turns")
    session_turns = [
        t for t in all_turns if str(t["session_id"]) == str(session_id)
    ]
    session_turns.sort(key=lambda t: int(t["turn_number"]))
    return [{"role": t["role"], "content": t["content"]} for t in session_turns]


def _save_turn(session_id: str, turn_number: int, role: str, content: str):
    store = get_store()
    store.append_row("Turns", {
        "id": store.next_id("Turns"),
        "session_id": session_id,
        "turn_number": turn_number,
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


def start(
    model: str,
    mode: str,
    question_id: Optional[str] = None,
    question_text: Optional[str] = None,
) -> tuple[str, ModelResponse]:
    """Start a new test session.

    Provide either question_id (to look up from sheet) or question_text (inline).

    Returns:
        (session_id, model_response)
    """
    store = get_store()

    # Resolve the question
    if question_id:
        q = store.get_by_id("Questions", question_id)
        if not q:
            raise ValueError(f"Question id={question_id} not found")
        text = q["text"]
    elif question_text:
        text = question_text
        question_id = ""
    else:
        raise ValueError("Provide --question-id or --question-text")

    if mode not in VALID_MODES:
        raise ValueError(f"Mode must be one of: {', '.join(VALID_MODES)}")

    # Create session
    session_id = str(store.next_id("Sessions"))
    store.append_row("Sessions", {
        "id": session_id,
        "question_id": question_id,
        "profile_id": "",
        "model": model,
        "mode": mode,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    # Save user turn
    _save_turn(session_id, 1, "user", text)

    # Send to model
    system_prompt = _build_system_prompt(mode)
    tools = _build_tools(mode)
    tool_handler = _get_tool_handler(mode)
    adapter = get_adapter(model)

    try:
        resp = adapter.send(
            messages=[{"role": "user", "content": text}],
            system_prompt=system_prompt,
            tools=tools,
            tool_handler=tool_handler,
        )
    except Exception as e:
        store.log_error(f"Model call failed: {e}", session_id)
        raise

    # Save assistant turn
    _save_turn(session_id, 2, "assistant", resp.content)
    tools_note = f" tools={resp.tools_used}" if resp.tools_used else ""
    store.log_info(
        f"Session {session_id} started: model={model} mode={mode} "
        f"tokens={resp.input_tokens}+{resp.output_tokens}{tools_note}",
        session_id,
    )

    return session_id, resp


def reply(session_id: str, user_message: str) -> ModelResponse:
    """Send a follow-up message in an existing session.

    Returns:
        The model's response.
    """
    store = get_store()
    session = store.get_by_id("Sessions", session_id)
    if not session:
        raise ValueError(f"Session id={session_id} not found")
    if session["status"] != "active":
        raise ValueError(f"Session {session_id} is {session['status']}, not active")

    turns = _get_turns(session_id)
    if len(turns) >= MAX_TURNS:
        raise ValueError(f"Session {session_id} has hit the {MAX_TURNS}-turn limit")

    turn_num = len(turns) + 1
    _save_turn(session_id, turn_num, "user", user_message)

    messages = turns + [{"role": "user", "content": user_message}]
    system_prompt = _build_system_prompt(session["mode"])
    tools = _build_tools(session["mode"])
    tool_handler = _get_tool_handler(session["mode"])
    adapter = get_adapter(session["model"])

    try:
        resp = adapter.send(
            messages=messages,
            system_prompt=system_prompt,
            tools=tools,
            tool_handler=tool_handler,
        )
    except Exception as e:
        store.log_error(f"Model call failed on reply: {e}", session_id)
        raise

    _save_turn(session_id, turn_num + 1, "assistant", resp.content)
    tools_note = f" tools={resp.tools_used}" if resp.tools_used else ""
    store.log_info(
        f"Session {session_id} reply turn={turn_num + 1} "
        f"tokens={resp.input_tokens}+{resp.output_tokens}{tools_note}",
        session_id,
    )

    return resp


def inject(session_id: str, profile_id: str) -> ModelResponse:
    """Auto-respond using a saved profile's data.

    Reads the last assistant message, constructs a natural user reply
    from the profile data, and sends it.
    """
    store = get_store()
    profile = store.get_by_id("Profiles", profile_id)
    if not profile:
        raise ValueError(f"Profile id={profile_id} not found")

    session = store.get_by_id("Sessions", session_id)
    if not session:
        raise ValueError(f"Session id={session_id} not found")

    # Link profile to session if not already linked
    if not session.get("profile_id"):
        store.update_cell_by_id("Sessions", session_id, "profile_id", profile_id)

    turns = _get_turns(session_id)
    if not turns or turns[-1]["role"] != "assistant":
        raise ValueError("Last turn must be from the assistant to inject a reply")

    last_assistant = turns[-1]["content"]

    # Use a model to generate a natural reply from the profile data
    inject_prompt = f"""You are role-playing as a person seeking financial advice.
A financial advisor just said the following to you:

---
{last_assistant}
---

You are this person:
- Name: {profile.get('name', 'N/A')}
- Age: {profile.get('age', 'N/A')}
- Annual income: ${profile.get('income', 'N/A')}
- Net worth: ${profile.get('net_worth', 'N/A')}
- Partnership: {profile.get('partnership', 'N/A')}
- Dependents: {profile.get('dependents', 'N/A')}
- Location: {profile.get('location', 'N/A')}
- Goals: {profile.get('goals', 'N/A')}
- Debts: {profile.get('debts', 'N/A')}
- Upcoming milestones: {profile.get('milestones', 'N/A')}
- How you feel about money: {profile.get('feelings', 'N/A')}

Respond naturally as this person would. Answer the questions the advisor asked
using your profile information. Keep it conversational — don't list everything
unless asked. Only share what's relevant to what they asked. Be brief."""

    # Use the same model as the session for consistency
    adapter = get_adapter(session["model"])
    inject_resp = adapter.send(
        messages=[{"role": "user", "content": inject_prompt}],
    )

    # Now send the generated reply as the user
    return reply(session_id, inject_resp.content)


def end_session(session_id: str):
    """Mark a session as complete."""
    store = get_store()
    store.update_cell_by_id("Sessions", session_id, "status", "complete")
    store.log_info(f"Session {session_id} marked complete", session_id)
