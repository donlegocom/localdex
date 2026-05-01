import json
from datetime import datetime
from pathlib import Path

from app.config import PROJECT_DIR

HISTORY_DIR = PROJECT_DIR / ".localdex"
HISTORY_FILE = HISTORY_DIR / "chat_history.json"


def load_history():
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_history(history):
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def add_chat(role, content):
    history = load_history()

    history.append({
        "role": role,
        "content": content,
        "time": datetime.now().isoformat(timespec="seconds")
    })

    history = history[-100:]
    save_history(history)


def clear_history():
    save_history([])


def format_history():
    history = load_history()

    if not history:
        return "Belum ada history."

    lines = []

    for item in history[-20:]:
        role = item.get("role", "unknown")
        content = item.get("content", "")
        lines.append(f"{role}: {content}")

    return "\n\n".join(lines)