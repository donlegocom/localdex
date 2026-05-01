import subprocess
from app.config import PROJECT_DIR, NODE_CMD


def run_localdex(prompt: str) -> str:
    try:
        result = subprocess.run(
            [NODE_CMD, "bin/localdex.js", prompt],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120
        )

        if result.returncode != 0:
            return result.stderr.strip() or "Error tanpa pesan"

        return result.stdout.strip() or "Kosong bro."

    except subprocess.TimeoutExpired:
        return "Timeout bro, mungkin model lagi berat."
    except Exception as e:
        return f"Error: {e}"