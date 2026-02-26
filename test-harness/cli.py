#!/usr/bin/env python3
"""WorthiQ Test Harness CLI.

A workbench for testing financial context methodology instructions
against real questions across multiple AI models.
"""

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.columns import Columns

from config import DEFAULT_MODEL, MODEL_REGISTRY
from sheets import get_store

app = typer.Typer(
    name="wiq",
    help="WorthiQ methodology test harness.",
    no_args_is_help=True,
)
console = Console()


# ── Setup ─────────────────────────────────────────────────────────────

@app.command()
def setup():
    """Initialize the Google Sheet with all required tabs."""
    with console.status("Connecting to Google Sheets..."):
        store = get_store()
        store.ensure_tabs()
    console.print("[green]✓[/green] Sheet initialized with all tabs.")


@app.command()
def refresh(
    all_data: bool = typer.Option(False, "--all", help="Clear ALL data tabs (Sessions, Turns, Analysis, Logs)"),
    logs_only: bool = typer.Option(False, "--logs", help="Clear only Logs tab"),
):
    """Clear data tabs for a fresh test run. Preserves Questions & Profiles."""
    store = get_store()
    if logs_only:
        tabs = ["Logs"]
    elif all_data:
        tabs = None  # defaults to all refreshable
    else:
        console.print("Specify --all (Sessions+Turns+Analysis+Logs) or --logs (Logs only)")
        raise typer.Exit(1)

    store.refresh(tabs)
    console.print(f"[green]✓[/green] Cleared: {', '.join(tabs or ['Sessions', 'Turns', 'Analysis', 'Logs'])}")


# ── Generators ────────────────────────────────────────────────────────

@app.command("gen-profile")
def cmd_gen_profile(
    constraints: str = typer.Option("", "--constraints", "-c", help="Persona constraints, e.g. 'late 20s, high income'"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="Model for generation"),
):
    """Generate a synthetic financial persona and save to Profiles sheet."""
    from generators import gen_profile

    with console.status("Generating profile..."):
        profile = gen_profile(constraints=constraints, model=model)

    table = Table(title=f"Profile #{profile['id']}: {profile['name']}")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    for k, v in profile.items():
        if k not in ("id", "is_synthetic", "notes"):
            table.add_row(k, str(v))
    console.print(table)


@app.command("add-question")
def cmd_add_question(
    text: str = typer.Option(..., "--text", "-t", help="The question text"),
    expected: str = typer.Option("yes", "--expected", "-e", help="Expected activation: yes/no/recognized_not_supported"),
    source_url: str = typer.Option("", "--url", help="Reddit/source URL"),
    subreddit: str = typer.Option("", "--subreddit", "-s", help="Source subreddit"),
    topic: str = typer.Option("", "--topic", help="Topic category"),
    edge_cases: str = typer.Option("", "--edge-cases", help="Comma-separated edge case tags"),
    notes: str = typer.Option("", "--notes", "-n", help="Notes"),
):
    """Add a test question to the Questions sheet."""
    from generators import add_question

    q = add_question(
        text=text,
        expected_activation=expected,
        source_url=source_url,
        subreddit=subreddit,
        topic_category=topic,
        edge_cases=edge_cases,
        notes=notes,
    )
    console.print(f"[green]✓[/green] Question #{q['id']} added.")


# ── Session ───────────────────────────────────────────────────────────

@app.command()
def start(
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="Model to test"),
    condition: str = typer.Option(..., "--condition", "-c", help="'with' or 'without' methodology"),
    question_id: Optional[str] = typer.Option(None, "--question-id", "-q", help="Question ID from sheet"),
    question_text: Optional[str] = typer.Option(None, "--text", "-t", help="Inline question text"),
):
    """Start a new test session. Sends the first message and shows the response."""
    from session import start as session_start

    with console.status(f"Sending to {model} ({condition})..."):
        session_id, resp = session_start(
            model=model,
            condition=condition,
            question_id=question_id,
            question_text=question_text,
        )

    console.print(f"\n[bold green]Session #{session_id}[/bold green] "
                  f"({model}, {condition})\n")
    console.print(Panel(resp.content, title="Assistant", border_style="blue"))
    console.print(f"\n[dim]Tokens: {resp.input_tokens} in / {resp.output_tokens} out[/dim]")
    console.print(f"[dim]Reply with:[/dim]  wiq reply --session {session_id} --text \"your message\"")


@app.command("reply")
def cmd_reply(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    text: str = typer.Option(..., "--text", "-t", help="Your message"),
):
    """Send a follow-up message in an active session."""
    from session import reply as session_reply

    with console.status("Sending reply..."):
        resp = session_reply(session_id=session, user_message=text)

    console.print(Panel(resp.content, title="Assistant", border_style="blue"))
    console.print(f"\n[dim]Tokens: {resp.input_tokens} in / {resp.output_tokens} out[/dim]")


@app.command()
def inject(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    profile: str = typer.Option(..., "--profile", "-p", help="Profile ID to inject"),
):
    """Auto-reply using a saved profile's data."""
    from session import inject as session_inject

    with console.status("Generating and sending profile-based reply..."):
        resp = session_inject(session_id=session, profile_id=profile)

    console.print(Panel(resp.content, title="Assistant (after inject)", border_style="blue"))
    console.print(f"\n[dim]Tokens: {resp.input_tokens} in / {resp.output_tokens} out[/dim]")


@app.command()
def end(
    session: str = typer.Option(..., "--session", "-s", help="Session ID to close"),
):
    """Mark a session as complete."""
    from session import end_session
    end_session(session)
    console.print(f"[green]✓[/green] Session #{session} marked complete.")


# ── Analyzers ─────────────────────────────────────────────────────────

@app.command("check-activation")
def cmd_check_activation(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    method: str = typer.Option("llm", "--method", help="'llm' or 'manual'"),
    judge: str = typer.Option(DEFAULT_MODEL, "--judge", "-j", help="Judge model (for llm method)"),
):
    """Check if the model correctly activated the methodology."""
    from analyzers import check_activation

    with console.status("Evaluating activation..."):
        result = check_activation(session_id=session, method=method, judge_model=judge)

    _print_analysis("Activation Check", result)


@app.command("check-questions")
def cmd_check_questions(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    method: str = typer.Option("llm", "--method", help="'llm' or 'manual'"),
    judge: str = typer.Option(DEFAULT_MODEL, "--judge", "-j", help="Judge model"),
):
    """Evaluate the quality of follow-up questions asked."""
    from analyzers import check_questions

    with console.status("Evaluating questions..."):
        result = check_questions(session_id=session, method=method, judge_model=judge)

    _print_analysis("Question Quality Check", result)


@app.command("check-response")
def cmd_check_response(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    method: str = typer.Option("llm", "--method", help="'llm' or 'manual'"),
    judge: str = typer.Option(DEFAULT_MODEL, "--judge", "-j", help="Judge model"),
):
    """Evaluate the response quality (answer + caveat + invitation)."""
    from analyzers import check_response

    with console.status("Evaluating response..."):
        result = check_response(session_id=session, method=method, judge_model=judge)

    _print_analysis("Response Quality Check", result)


# ── Listing & Comparison ─────────────────────────────────────────────

@app.command("list")
def cmd_list(
    tab: str = typer.Argument(..., help="Tab to list: questions, profiles, sessions, analysis"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max rows to show"),
):
    """List rows from a sheet tab."""
    store = get_store()
    tab_map = {
        "questions": "Questions",
        "profiles": "Profiles",
        "sessions": "Sessions",
        "analysis": "Analysis",
        "logs": "Logs",
    }
    tab_name = tab_map.get(tab.lower())
    if not tab_name:
        console.print(f"[red]Unknown tab '{tab}'. Use: {', '.join(tab_map.keys())}[/red]")
        raise typer.Exit(1)

    rows = store.get_all(tab_name)
    if not rows:
        console.print(f"[dim]No rows in {tab_name}.[/dim]")
        return

    table = Table(title=tab_name)
    headers = list(rows[0].keys())
    for h in headers:
        table.add_column(h, max_width=60)

    for row in rows[-limit:]:
        table.add_row(*[str(row.get(h, ""))[:60] for h in headers])

    console.print(table)


@app.command()
def compare(
    session_a: str = typer.Option(..., "--a", help="First session ID"),
    session_b: str = typer.Option(..., "--b", help="Second session ID"),
):
    """Side-by-side comparison of two sessions' conversations."""
    store = get_store()
    all_turns = store.get_all("Turns")

    def get_turns(sid):
        turns = [t for t in all_turns if str(t["session_id"]) == str(sid)]
        turns.sort(key=lambda t: int(t["turn_number"]))
        return turns

    turns_a = get_turns(session_a)
    turns_b = get_turns(session_b)

    sess_a = store.get_by_id("Sessions", session_a) or {}
    sess_b = store.get_by_id("Sessions", session_b) or {}

    def format_session(turns, sess, label):
        header = f"{label} — {sess.get('model', '?')} ({sess.get('condition', '?')})"
        parts = [f"[bold]{header}[/bold]\n"]
        for t in turns:
            role_color = "green" if t["role"] == "user" else "blue"
            content = str(t["content"])[:500]
            parts.append(f"[{role_color}]{t['role'].upper()}[/{role_color}]: {content}\n")
        return "\n".join(parts)

    text_a = format_session(turns_a, sess_a, f"Session #{session_a}")
    text_b = format_session(turns_b, sess_b, f"Session #{session_b}")

    console.print(Columns(
        [Panel(text_a, expand=True), Panel(text_b, expand=True)],
        equal=True,
    ))


@app.command()
def tag(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
    stage: str = typer.Option(..., "--stage", help="activation/questions/response/edge_case"),
    notes: str = typer.Option(..., "--notes", "-n", help="Your evaluation notes"),
    score: Optional[int] = typer.Option(None, "--score", help="Optional 1-5 score"),
):
    """Add a manual analysis tag to a session."""
    store = get_store()
    result = {"manual_notes": notes}
    if score is not None:
        result["manual_score"] = score
    store.append_row("Analysis", {
        "id": store.next_id("Analysis"),
        "session_id": session,
        "stage": stage,
        "method": "manual",
        "result": json.dumps(result),
        "notes": notes,
        "created_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
    })
    console.print(f"[green]✓[/green] Tagged session #{session} ({stage}).")


@app.command()
def models():
    """List available models."""
    table = Table(title="Available Models")
    table.add_column("Name", style="bold")
    table.add_column("Provider")
    table.add_column("API Model")
    for name, info in sorted(MODEL_REGISTRY.items()):
        table.add_row(name, info["provider"], info["api_model"])
    console.print(table)


@app.command()
def show(
    session: str = typer.Option(..., "--session", "-s", help="Session ID"),
):
    """Show full conversation for a session."""
    store = get_store()
    sess = store.get_by_id("Sessions", session)
    if not sess:
        console.print(f"[red]Session {session} not found.[/red]")
        raise typer.Exit(1)

    all_turns = store.get_all("Turns")
    turns = [t for t in all_turns if str(t["session_id"]) == str(session)]
    turns.sort(key=lambda t: int(t["turn_number"]))

    console.print(f"\n[bold]Session #{session}[/bold] — "
                  f"{sess['model']} ({sess['condition']}) — {sess['status']}\n")

    for t in turns:
        role_color = "green" if t["role"] == "user" else "blue"
        console.print(f"[{role_color} bold]{t['role'].upper()}[/{role_color} bold]")
        console.print(t["content"])
        console.print()


@app.command()
def export(
    tab: str = typer.Argument(..., help="Tab to export: sessions, analysis, turns, logs"),
    output: str = typer.Option("export.json", "--output", "-o", help="Output file path"),
):
    """Export a tab's data to JSON."""
    store = get_store()
    tab_map = {
        "sessions": "Sessions",
        "analysis": "Analysis",
        "turns": "Turns",
        "logs": "Logs",
        "questions": "Questions",
        "profiles": "Profiles",
    }
    tab_name = tab_map.get(tab.lower())
    if not tab_name:
        console.print(f"[red]Unknown tab.[/red]")
        raise typer.Exit(1)

    rows = store.get_all(tab_name)
    with open(output, "w") as f:
        json.dump(rows, f, indent=2)
    console.print(f"[green]✓[/green] Exported {len(rows)} rows to {output}")


# ── Helpers ───────────────────────────────────────────────────────────

def _print_analysis(title: str, result: dict):
    """Pretty-print an analysis result."""
    console.print(f"\n[bold]{title}[/bold]\n")
    for k, v in result.items():
        if k in ("conversation_preview", "response_preview", "question_preview"):
            console.print(f"  [dim]{k}:[/dim]")
            console.print(Panel(str(v)[:500], border_style="dim"))
        else:
            style = ""
            if isinstance(v, bool):
                style = "green" if v else "red"
            console.print(f"  [bold]{k}:[/bold] [{style}]{v}[/{style}]")
    console.print()


if __name__ == "__main__":
    app()
