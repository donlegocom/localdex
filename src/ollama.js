import { config } from "./config.js";

export async function askOllama(prompt, model = config.defaultModel) {
  const projectBrief = `
Kamu adalah LocalDex, asisten coding lokal buatan user.

Tentang LocalDex:
- LocalDex adalah codex lokal sederhana.
- Dibuat dengan Node.js, Python UI, Ollama, dan model qwen3.
- Tujuannya membantu user membaca file, menulis file, edit file, memahami project, dan ngobrol soal coding.
- LocalDex BUKAN crypto, BUKAN decentralized exchange, BUKAN DEX blockchain.
- Jawab santai pakai bahasa Indonesia.
- Jawaban harus ringkas, jelas, dan praktis.
- Jangan tampilkan thinking atau reasoning panjang.
`;

  const noThinkPrompt = `/no_think

${projectBrief}

User:
${prompt}`;

  const res = await fetch(`${config.ollamaHost}/api/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model,
      prompt: noThinkPrompt,
      stream: false,
      options: {
        temperature: 0.5
      }
    })
  });

  if (!res.ok) {
    throw new Error(`Ollama error: ${res.status}`);
  }

  const data = await res.json();

  let output = data.response || "";

  output = output
    .replace(/<think>[\s\S]*?<\/think>/gi, "")
    .replace(/Thinking[\s\S]*?\.\.\.done thinking\./gi, "")
    .trim();

  return output;
}