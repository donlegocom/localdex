import readline from "readline/promises";
import { stdin as input, stdout as output } from "process";
import { runAgent } from "./agent.js";
import { config } from "./config.js";
import { loadMemory, clearMemory, formatMemory, addMemory } from "./memory.js";

export async function startUI() {
  console.clear();

  console.log("================================");
  console.log(" LocalDex");
  console.log(" local codex sederhana");
  console.log("================================");
  console.log("");
  console.log(`model : ${config.defaultModel}`);
  console.log(`folder: ${process.cwd()}`);
  console.log("");
  console.log("Command:");
  console.log("  /help          bantuan");
  console.log("  /memory        lihat memory");
  console.log("  /clear-memory  hapus memory");
  console.log("  /exit          keluar");
  console.log("");

  const rl = readline.createInterface({ input, output });

  while (true) {
    const prompt = await rl.question("localdex > ");

    if (!prompt.trim()) continue;

    if (prompt === "/exit") {
      console.log("bye bro.");
      rl.close();
      break;
    }

    if (prompt === "/help") {
      console.log("");
      console.log("Contoh:");
      console.log("  baca package.json");
      console.log("  baca package.json terus jelasin");
      console.log("  buat file notes.txt isinya belajar node js");
      console.log("  lihat semua file di folder ini");
      console.log("  jelasin lagi yang tadi");
      console.log("");
      continue;
    }

    if (prompt === "/memory") {
      const memory = await loadMemory();
      console.log("");
      console.log(formatMemory(memory) || "Memory masih kosong.");
      console.log("");
      continue;
    }

    if (prompt === "/clear-memory") {
      await clearMemory();
      console.log("");
      console.log("Memory sudah dihapus.");
      console.log("");
      continue;
    }

    if (prompt.startsWith("/remember ")) {
      const memoryText = prompt.replace("/remember ", "").trim();

      await addMemory("user", `Ingat ini: ${memoryText}`);

      console.log("");
      console.log(`Oke, gue inget: ${memoryText}`);
      console.log("");

      continue;
}

    try {
      console.log("");
      console.log("LocalDex lagi mikir...");
      console.log("");

      const result = await runAgent(prompt, {
        model: config.defaultModel
      });

      console.log(result);
      console.log("");
    } catch (err) {
      console.log("Error:", err.message);
      console.log("");
    }
  }
}