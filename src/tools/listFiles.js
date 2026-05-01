import fs from "fs/promises";
import { safePath } from "../utils/paths.js";

export async function listFilesTool(dirPath = ".") {
  const items = await fs.readdir(safePath(dirPath), {
    withFileTypes: true
  });

  return items
    .map((item) => item.isDirectory() ? item.name + "/" : item.name)
    .join("\n");
}