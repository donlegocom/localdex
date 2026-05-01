import fs from "fs/promises";
import { safePath } from "../utils/paths.js";

export async function writeFileTool(filePath, content) {
  await fs.writeFile(safePath(filePath), content, "utf8");
  return `Berhasil nulis ke ${filePath}`;
}