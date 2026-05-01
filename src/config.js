import "dotenv/config";

export const config = {
  ollamaHost: process.env.OLLAMA_HOST || "http://localhost:11434",
  defaultModel: process.env.DEFAULT_MODEL || "qwen3-coder:30b"
};
