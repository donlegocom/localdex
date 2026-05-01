import { askOllama } from "./ollama.js";
import { config } from "./config.js";
import { readFileTool } from "./tools/readFile.js";
import { writeFileTool } from "./tools/writeFile.js";
import { editFileTool } from "./tools/editFile.js";
import { listFilesTool } from "./tools/listFiles.js";
import { loadMemory, addMemory, formatMemory } from "./memory.js";

async function plan(prompt, model) {
  const systemPrompt = `
Kamu adalah AI planner untuk CLI lokal bernama LocalDex.

Tugas:
ubah instruksi user jadi JSON.

Format:
{
  "action": "read | write | edit | list | chat",
  "file": "string optional",
  "content": "string optional",
  "from": "string optional",
  "to": "string optional",
  "followup": "string optional"
}

Rules:
- baca file → action: read
- lihat folder → action: list
- buat file → action: write
- edit file → action: edit
- selain itu → action: chat
- Output HARUS JSON valid
- Jangan kasih teks selain JSON
`;

  const result = await askOllama(`${systemPrompt}\nUser: ${prompt}`, model);

  try {
    const jsonText = result.match(/\{[\s\S]*\}/)?.[0];
    return JSON.parse(jsonText);
  } catch {
    return { action: "chat" };
  }
}

export async function runAgent(prompt, options = {}) {
  const model = options.model || config.defaultModel;
  const memory = await loadMemory();
  const memoryText = formatMemory(memory);

  await addMemory("user", prompt);

    // ⚡ shortcut: kalau bukan perintah file → langsung chat
  const simpleChat =
    !prompt.toLowerCase().includes("baca") &&
    !prompt.toLowerCase().includes("file") &&
    !prompt.toLowerCase().includes("buat") &&
    !prompt.toLowerCase().includes("edit") &&
    !prompt.toLowerCase().includes("list");

if (simpleChat) {
  const memory = await loadMemory();
  const memoryText = formatMemory(memory);

  await addMemory("user", prompt);

  const result = await askOllama(
    `Memory:
${memoryText}

User:
${prompt}`,
    model
  );

  await addMemory("assistant", result);

  return result;
}

// kalau bukan simple → pakai planner
const planResult = await plan(prompt, model);

  let result = "";

  switch (planResult.action) {
    case "read": {
      const content = await readFileTool(planResult.file);

      if (planResult.followup) {
        result = await askOllama(
          `Memory percakapan sebelumnya:
${memoryText}

Isi file ${planResult.file}:
${content}

Instruksi user:
${planResult.followup}`,
          model
        );
      } else {
        result = content;
      }

      break;
    }

    case "write":
      result = await writeFileTool(planResult.file, planResult.content || "");
      break;

    case "edit":
      result = await editFileTool(
        planResult.file,
        planResult.from,
        planResult.to
      );
      break;

    case "list":
      result = await listFilesTool(".");
      break;

    case "chat":
    default:
      result = await askOllama(
        `Memory percakapan sebelumnya:
${memoryText}

User:
${prompt}`,
        model
      );
      break;
  }

  await addMemory("assistant", result);

  return result;
}