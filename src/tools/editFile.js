import fs from "fs/promises";
import { safePath } from "../utils/paths.js";
import { askOllama } from "../ollama.js";
import { config } from "../config.js";

export async function editFileTool(filePath, instruction, options = {}) {
  const path = safePath(filePath);
  const model = options.model || config.defaultModel;

  const oldContent = await fs.readFile(path, "utf8");

  const prompt = `
Kamu adalah AI code editor.

Tugas kamu:
Edit file berdasarkan instruksi user.

File path:
${filePath}

Isi file saat ini:
\`\`\`
${oldContent}
\`\`\`

Instruksi edit:
${instruction}

Aturan output:
- Balas HANYA isi file versi baru secara lengkap.
- Jangan kasih penjelasan.
- Jangan pakai markdown.
- Jangan bungkus dengan triple backtick.
- Jangan tulis "berhasil edit".
`;

  let newContent = await askOllama(prompt, model);

  newContent = newContent
    .replace(/^```[a-zA-Z]*\n?/, "")
    .replace(/```$/, "")
    .trim();

  await fs.writeFile(path, newContent, "utf8");

  return `Berhasil AI edit ${filePath}`;
}