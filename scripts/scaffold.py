from pathlib import Path

ROOT = Path("localdex")

files = {
    "package.json": """{
  "name": "localdex",
  "version": "0.1.0",
  "type": "module",
  "bin": {
    "localdex": "./bin/localdex.js"
  },
  "scripts": {
    "start": "node bin/localdex.js"
  },
  "dependencies": {
    "dotenv": "^16.4.5",
    "commander": "^12.1.0"
  }
}
""",

    ".env.example": """OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen3
""",

    "README.md": """# LocalDex

Codex lokal minimal pakai Node.js + Ollama.

## Run

```bash
npm install
npm start -- "baca package.json"