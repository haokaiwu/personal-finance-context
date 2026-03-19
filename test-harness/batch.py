"""Batch testing: run multiple model×mode combos in parallel."""

import queue
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Optional

from config import MODEL_ALIASES, MODEL_REGISTRY, resolve_model
from models import get_adapter
from session import (
    _build_system_prompt,
    _build_tools,
    _get_tool_handler,
)
from sheets import SheetStore, get_store

# Default models and modes for batch runs
DEFAULT_BATCH_MODELS = list(MODEL_ALIASES.keys())  # ops, snt, gpt, gmn
DEFAULT_BATCH_MODES = ["without", "general", "category"]

# Map shorthand -> column prefix (uppercase)
SHORTHAND_PREFIX = {v: k.upper() for k, v in MODEL_ALIASES.items()}


def resolve_mode(model: str, mode: str) -> str:
    """Map user-facing mode to actual mode per provider.

    'category' -> 'category' for Anthropic (dynamic tool loading)
    'category' -> 'category-all' for OpenAI/Google (static context)
    """
    if mode != "category":
        return mode
    full_name = resolve_model(model)
    entry = MODEL_REGISTRY.get(full_name)
    if not entry:
        return mode
    if entry["provider"] == "anthropic":
        return "category"
    return "category-all"


def _col_name(model_shorthand: str, mode: str) -> str:
    """Build a Batch tab column name like 'OPS-general'."""
    prefix = model_shorthand.upper()
    return f"{prefix}-{mode}"


def _generate_batch_id() -> str:
    """Generate a batch ID like B-20260318-143022."""
    now = datetime.now(timezone.utc)
    return f"B-{now.strftime('%Y%m%d-%H%M%S')}"


# ── Sheet writer thread ──────────────────────────────────────────────

def _sheet_writer(store: SheetStore, q: queue.Queue):
    """Drain write tasks from the queue, serializing all sheet writes."""
    while True:
        task = q.get()
        if task is None:
            break
        try:
            method, args, kwargs = task
            getattr(store, method)(*args, **kwargs)
        except Exception as e:
            store.log_error(f"Batch writer error: {e}")
        finally:
            q.task_done()


# ── Single-session workers ────────────────────────────────────────────

def _run_single_start(
    model: str,
    actual_mode: str,
    question_text: str,
    session_id: str,
    turn_id_user: int,
    turn_id_asst: int,
    write_queue: queue.Queue,
) -> dict:
    """Worker: send the first message to one model and return results."""
    system_prompt = _build_system_prompt(actual_mode)
    tools = _build_tools(actual_mode)
    tool_handler = _get_tool_handler(actual_mode)
    adapter = get_adapter(model)

    resp = adapter.send(
        messages=[{"role": "user", "content": question_text}],
        system_prompt=system_prompt,
        tools=tools,
        tool_handler=tool_handler,
    )

    now = datetime.now(timezone.utc).isoformat()

    # Queue turn writes
    write_queue.put(("append_row", ("Turns", {
        "id": turn_id_user,
        "session_id": session_id,
        "turn_number": 1,
        "role": "user",
        "content": question_text,
        "timestamp": now,
    }), {}))

    write_queue.put(("append_row", ("Turns", {
        "id": turn_id_asst,
        "session_id": session_id,
        "turn_number": 2,
        "role": "assistant",
        "content": resp.content,
        "timestamp": now,
    }), {}))

    return {
        "session_id": session_id,
        "model": model,
        "mode": actual_mode,
        "content": resp.content,
        "input_tokens": resp.input_tokens,
        "output_tokens": resp.output_tokens,
        "tools_used": resp.tools_used,
    }


def _run_single_inject(
    model: str,
    actual_mode: str,
    session_id: str,
    profile: dict,
    history: list[dict],
    turn_id_user: int,
    turn_id_asst: int,
    user_turn_number: int,
    write_queue: queue.Queue,
) -> dict:
    """Worker: generate a profile-based reply and send it to the model."""
    last_assistant = history[-1]["content"] if history else ""

    # Generate natural reply from profile
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

    adapter = get_adapter(model)
    inject_resp = adapter.send(
        messages=[{"role": "user", "content": inject_prompt}],
    )
    user_reply = inject_resp.content

    # Now send the generated reply as follow-up in the actual session
    system_prompt = _build_system_prompt(actual_mode)
    tools = _build_tools(actual_mode)
    tool_handler = _get_tool_handler(actual_mode)

    messages = history + [{"role": "user", "content": user_reply}]
    resp = adapter.send(
        messages=messages,
        system_prompt=system_prompt,
        tools=tools,
        tool_handler=tool_handler,
    )

    now = datetime.now(timezone.utc).isoformat()

    # Queue turn writes
    write_queue.put(("append_row", ("Turns", {
        "id": turn_id_user,
        "session_id": session_id,
        "turn_number": user_turn_number,
        "role": "user",
        "content": user_reply,
        "timestamp": now,
    }), {}))

    write_queue.put(("append_row", ("Turns", {
        "id": turn_id_asst,
        "session_id": session_id,
        "turn_number": user_turn_number + 1,
        "role": "assistant",
        "content": resp.content,
        "timestamp": now,
    }), {}))

    return {
        "session_id": session_id,
        "model": model,
        "mode": actual_mode,
        "user_reply": user_reply,
        "content": resp.content,
        "input_tokens": resp.input_tokens,
        "output_tokens": resp.output_tokens,
        "tools_used": resp.tools_used,
    }


# ── Public API ────────────────────────────────────────────────────────

def batch_start(
    question_id: str,
    models: Optional[list[str]] = None,
    modes: Optional[list[str]] = None,
) -> tuple[str, list[dict]]:
    """Start sessions for all model×mode combos in parallel.

    Returns:
        (batch_id, list of result dicts)
    """
    store = get_store()
    models = models or DEFAULT_BATCH_MODELS
    modes = modes or DEFAULT_BATCH_MODES

    # Resolve question
    q = store.get_by_id("Questions", question_id)
    if not q:
        raise ValueError(f"Question id={question_id} not found")
    question_text = q["text"]

    batch_id = _generate_batch_id()

    # Pre-allocate all IDs in main thread
    combos = []
    next_session = store.next_id("Sessions")
    next_turn = store.next_id("Turns")

    for model_short in models:
        full_model = resolve_model(model_short)
        for mode in modes:
            actual_mode = resolve_mode(model_short, mode)
            session_id = str(next_session)
            turn_id_user = next_turn
            turn_id_asst = next_turn + 1
            combos.append({
                "model_short": model_short,
                "full_model": full_model,
                "user_mode": mode,
                "actual_mode": actual_mode,
                "session_id": session_id,
                "turn_id_user": turn_id_user,
                "turn_id_asst": turn_id_asst,
            })
            next_session += 1
            next_turn += 2

    # Write all session rows upfront (main thread, serialized)
    now = datetime.now(timezone.utc).isoformat()
    for c in combos:
        store.append_row("Sessions", {
            "id": c["session_id"],
            "question_id": question_id,
            "profile_id": "",
            "model": c["full_model"],
            "mode": c["actual_mode"],
            "status": "active",
            "created_at": now,
            "batch_id": batch_id,
        })

    # Start writer thread
    write_queue = queue.Queue()
    writer = threading.Thread(
        target=_sheet_writer, args=(store, write_queue), daemon=True
    )
    writer.start()

    # Submit workers
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {}
        for c in combos:
            f = executor.submit(
                _run_single_start,
                model=c["full_model"],
                actual_mode=c["actual_mode"],
                question_text=question_text,
                session_id=c["session_id"],
                turn_id_user=c["turn_id_user"],
                turn_id_asst=c["turn_id_asst"],
                write_queue=write_queue,
            )
            futures[f] = c

        for f in as_completed(futures):
            c = futures[f]
            try:
                result = f.result()
                result["model_short"] = c["model_short"]
                result["user_mode"] = c["user_mode"]
                results.append(result)
            except Exception as e:
                store.log_error(
                    f"Batch start failed: {c['full_model']} {c['actual_mode']}: {e}",
                    c["session_id"],
                )
                results.append({
                    "session_id": c["session_id"],
                    "model": c["full_model"],
                    "model_short": c["model_short"],
                    "mode": c["actual_mode"],
                    "user_mode": c["user_mode"],
                    "content": f"ERROR: {e}",
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "tools_used": [],
                })

    # Drain write queue
    write_queue.put(None)
    writer.join()

    # Write to Batch tab
    # Turn 1: user question (same in all columns)
    turn1_results = {}
    turn2_results = {}
    for r in results:
        col = _col_name(r["model_short"], r["user_mode"])
        turn1_results[col] = question_text
        turn2_results[col] = r["content"]

    store.write_batch_turn(batch_id, question_id, question_text, 1, turn1_results)
    store.write_batch_turn(batch_id, question_id, question_text, 2, turn2_results)

    store.log_info(f"Batch {batch_id} started: {len(results)} sessions")
    return batch_id, results


def batch_inject(
    batch_id: str,
    profile_id: str,
    filter_models: Optional[list[str]] = None,
    filter_modes: Optional[list[str]] = None,
) -> list[dict]:
    """Inject profile-based replies into batch sessions.

    Only callable after batch_start completes (synchronous gating).
    """
    store = get_store()

    profile = store.get_by_id("Profiles", profile_id)
    if not profile:
        raise ValueError(f"Profile id={profile_id} not found")

    # Find matching sessions
    all_sessions = store.get_filtered("Sessions", {"batch_id": batch_id})
    if not all_sessions:
        raise ValueError(f"No sessions found for batch {batch_id}")

    # Apply filters
    if filter_models:
        resolved_models = {resolve_model(m) for m in filter_models}
        all_sessions = [s for s in all_sessions if s["model"] in resolved_models]

    if filter_modes:
        # "category" filter matches both "category" and "category-all"
        expanded_modes = set()
        for m in filter_modes:
            expanded_modes.add(m)
            if m == "category":
                expanded_modes.add("category-all")
        all_sessions = [s for s in all_sessions if s["mode"] in expanded_modes]

    if not all_sessions:
        raise ValueError("No sessions match the given filters")

    # Cache turn history for each session (main thread)
    all_turns = store.get_all("Turns")
    session_histories = {}
    for s in all_sessions:
        sid = str(s["id"])
        turns = [t for t in all_turns if str(t["session_id"]) == sid]
        turns.sort(key=lambda t: int(t["turn_number"]))
        session_histories[sid] = [
            {"role": t["role"], "content": t["content"]} for t in turns
        ]

    # Link profile to sessions
    for s in all_sessions:
        if not s.get("profile_id"):
            store.update_cell_by_id("Sessions", str(s["id"]), "profile_id", profile_id)

    # Pre-allocate turn IDs
    next_turn = store.next_id("Turns")
    inject_combos = []
    for s in all_sessions:
        sid = str(s["id"])
        history = session_histories[sid]
        if not history or history[-1]["role"] != "assistant":
            continue
        user_turn_number = len(history) + 1
        inject_combos.append({
            "session": s,
            "history": history,
            "user_turn_number": user_turn_number,
            "turn_id_user": next_turn,
            "turn_id_asst": next_turn + 1,
        })
        next_turn += 2

    # Start writer thread
    write_queue = queue.Queue()
    writer = threading.Thread(
        target=_sheet_writer, args=(store, write_queue), daemon=True
    )
    writer.start()

    # Submit inject workers
    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {}
        for ic in inject_combos:
            s = ic["session"]
            f = executor.submit(
                _run_single_inject,
                model=s["model"],
                actual_mode=s["mode"],
                session_id=str(s["id"]),
                profile=profile,
                history=ic["history"],
                turn_id_user=ic["turn_id_user"],
                turn_id_asst=ic["turn_id_asst"],
                user_turn_number=ic["user_turn_number"],
                write_queue=write_queue,
            )
            futures[f] = ic

        for f in as_completed(futures):
            ic = futures[f]
            s = ic["session"]
            try:
                result = f.result()
                # Determine shorthand and user-facing mode
                full_model = s["model"]
                result["model_short"] = SHORTHAND_PREFIX.get(full_model, full_model[:3]).lower()
                actual_mode = s["mode"]
                result["user_mode"] = "category" if actual_mode in ("category", "category-all") else actual_mode
                result["user_turn_number"] = ic["user_turn_number"]
                results.append(result)
            except Exception as e:
                store.log_error(
                    f"Batch inject failed: {s['model']} {s['mode']}: {e}",
                    str(s["id"]),
                )

    # Drain write queue
    write_queue.put(None)
    writer.join()

    # Write inject turns to Batch tab
    if results:
        # Get question info from first session
        first_session = all_sessions[0]
        question_id = str(first_session.get("question_id", ""))
        q = store.get_by_id("Questions", question_id) if question_id else None
        question_text = q["text"] if q else ""

        # Group by turn numbers (user reply = turn N, assistant = turn N+1)
        user_turn_results = {}
        asst_turn_results = {}
        user_turn_num = None
        asst_turn_num = None
        for r in results:
            col = _col_name(r["model_short"], r["user_mode"])
            utn = r["user_turn_number"]
            atn = utn + 1
            user_turn_num = utn
            asst_turn_num = atn
            user_turn_results[col] = r.get("user_reply", "")
            asst_turn_results[col] = r["content"]

        if user_turn_num:
            store.write_batch_turn(batch_id, question_id, question_text, user_turn_num, user_turn_results)
            store.write_batch_turn(batch_id, question_id, question_text, asst_turn_num, asst_turn_results)

    store.log_info(f"Batch {batch_id} inject: {len(results)} sessions injected")
    return results


def batch_show(batch_id: str) -> list[dict]:
    """Get summary of all sessions in a batch."""
    store = get_store()
    sessions = store.get_filtered("Sessions", {"batch_id": batch_id})
    if not sessions:
        raise ValueError(f"No sessions found for batch {batch_id}")
    return sessions


def batch_end(batch_id: str) -> int:
    """Mark all active sessions in a batch as complete. Returns count."""
    store = get_store()
    sessions = store.get_filtered("Sessions", {"batch_id": batch_id})
    count = 0
    for s in sessions:
        if s.get("status") == "active":
            store.update_cell_by_id("Sessions", str(s["id"]), "status", "complete")
            count += 1
    store.log_info(f"Batch {batch_id} ended: {count} sessions marked complete")
    return count
