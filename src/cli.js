import { Command } from "commander";
import { runAgent } from "./agent.js";
import { startUI } from "./ui.js";

export async function runCli() {
  const program = new Command();

  program
    .name("localdex")
    .argument("[prompt...]", "prompt")
    .option("-m, --model <model>", "model ollama")
    .action(async (promptParts, options) => {
      const prompt = promptParts.join(" ");

      if (!prompt) {
        await startUI();
        return;
      }

      try {
        const result = await runAgent(prompt, options);
        console.log(result);
      } catch (err) {
        console.error("Error:", err.message);
        process.exitCode = 1;
      }
    });

  await program.parseAsync(process.argv);
}