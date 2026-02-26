"""Google Sheets data layer.

One spreadsheet, multiple worksheet tabs. Questions and Profiles are
manually edited by the user. Sessions, Turns, Analysis, and Logs are
append-only from the CLI.
"""

import json
import traceback
from datetime import datetime, timezone
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from config import GOOGLE_SERVICE_ACCOUNT_FILE, GOOGLE_SHEET_NAME

# ── Schema: header rows for each tab ──────────────────────────────────

TAB_HEADERS = {
    "Questions": [
        "id", "text", "source_url", "subreddit", "topic_category",
        "expected_activation", "edge_cases", "notes",
    ],
    "Profiles": [
        "id", "name", "age", "income", "net_worth", "partnership",
        "dependents", "feelings", "location", "goals", "debts",
        "milestones", "is_synthetic", "notes",
    ],
    "Sessions": [
        "id", "question_id", "profile_id", "model", "condition",
        "status", "created_at",
    ],
    "Turns": [
        "id", "session_id", "turn_number", "role", "content", "timestamp",
    ],
    "Analysis": [
        "id", "session_id", "stage", "method", "result", "notes", "created_at",
    ],
    "Logs": [
        "timestamp", "level", "session_id", "message", "traceback",
    ],
}

# Tabs that get wiped on refresh (preserves Questions & Profiles)
REFRESHABLE_TABS = ["Sessions", "Turns", "Analysis", "Logs"]


class SheetStore:
    """Thin wrapper around a Google Sheets spreadsheet."""

    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_FILE, scopes=scopes,
        )
        self.gc = gspread.authorize(creds)
        self.spreadsheet = self.gc.open(GOOGLE_SHEET_NAME)

    # ── Bootstrap ─────────────────────────────────────────────────────

    def ensure_tabs(self):
        """Create any missing tabs and set headers."""
        existing = {ws.title for ws in self.spreadsheet.worksheets()}
        for tab_name, headers in TAB_HEADERS.items():
            if tab_name not in existing:
                ws = self.spreadsheet.add_worksheet(
                    title=tab_name, rows=1000, cols=len(headers),
                )
                ws.append_row(headers)
            else:
                ws = self.spreadsheet.worksheet(tab_name)
                if not ws.row_values(1):
                    ws.append_row(headers)

    # ── Generic read/write ────────────────────────────────────────────

    def get_all(self, tab: str) -> list[dict]:
        """Return all rows as dicts (header-keyed)."""
        ws = self.spreadsheet.worksheet(tab)
        return ws.get_all_records()

    def get_by_id(self, tab: str, row_id: str) -> Optional[dict]:
        """Find a row by its 'id' column."""
        rows = self.get_all(tab)
        for r in rows:
            if str(r.get("id")) == str(row_id):
                return r
        return None

    def append_row(self, tab: str, data: dict):
        """Append a single row. Keys must match headers."""
        ws = self.spreadsheet.worksheet(tab)
        headers = TAB_HEADERS[tab]
        row = [str(data.get(h, "")) for h in headers]
        ws.append_row(row, value_input_option="RAW")

    def update_cell_by_id(self, tab: str, row_id: str, col: str, value: str):
        """Update a single cell identified by row id and column name."""
        ws = self.spreadsheet.worksheet(tab)
        headers = ws.row_values(1)
        col_idx = headers.index(col) + 1  # 1-indexed
        all_vals = ws.col_values(1)  # id column
        for i, v in enumerate(all_vals):
            if str(v) == str(row_id) and i > 0:  # skip header
                ws.update_cell(i + 1, col_idx, value)
                return
        raise ValueError(f"Row id={row_id} not found in {tab}")

    def next_id(self, tab: str) -> int:
        """Return the next sequential integer id for a tab."""
        rows = self.get_all(tab)
        if not rows:
            return 1
        ids = [int(r["id"]) for r in rows if str(r.get("id", "")).isdigit()]
        return max(ids, default=0) + 1

    # ── Refresh (clear data tabs, keep Questions & Profiles) ──────────

    def refresh(self, tabs: Optional[list[str]] = None):
        """Clear data rows (keep headers) for the specified tabs.

        Default: clears Sessions, Turns, Analysis, Logs.
        """
        targets = tabs or REFRESHABLE_TABS
        for tab_name in targets:
            ws = self.spreadsheet.worksheet(tab_name)
            headers = TAB_HEADERS[tab_name]
            ws.clear()
            ws.append_row(headers)

    # ── Structured logging ────────────────────────────────────────────

    def log(
        self,
        level: str,
        message: str,
        session_id: str = "",
        tb: str = "",
    ):
        """Append a log entry to the Logs tab."""
        self.append_row("Logs", {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "session_id": session_id,
            "message": message[:1000],  # cap to avoid sheet cell limits
            "traceback": tb[:2000],
        })

    def log_error(self, message: str, session_id: str = ""):
        """Log an error with automatic traceback capture."""
        self.log("ERROR", message, session_id, traceback.format_exc())

    def log_info(self, message: str, session_id: str = ""):
        self.log("INFO", message, session_id)


# ── Module-level convenience ──────────────────────────────────────────

_store: Optional[SheetStore] = None


def get_store() -> SheetStore:
    """Singleton accessor."""
    global _store
    if _store is None:
        _store = SheetStore()
        _store.ensure_tabs()
    return _store
