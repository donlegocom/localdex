import fs from "fs/promises";
import path from "path";

const memoryDir = path.resolve(process.cwd(), ".localdex");
const memoryFile = path.join(memoryDir, "memory.json");

export async function loadMemory() {
  try {
    const content = await fs.readFile(memoryFile, "utf8");
    return JSON.parse(content);
  } catch {
    return [];
  }
}

export async function saveMemory(memory) {
  await fs.mkdir(memoryDir, { recursive: true });
  await fs.writeFile(memoryFile, JSON.stringify(memory, null, 2), "utf8");
}

export async function addMemory(role, content) {
  const memory = await loadMemory();

  memory.push({
    role,
    content,
    time: new Date().toISOString()
  });

  const limitedMemory = memory.slice(-20);

  await saveMemory(limitedMemory);
}

export async function clearMemory() {
  await saveMemory([]);
}

export function formatMemory(memory) {
  if (!memory.length) return "";

  return memory
    .map((item) => `${item.role}: ${item.content}`)
    .join("\n");
}