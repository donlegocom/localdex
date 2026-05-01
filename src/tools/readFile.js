import fs from "fs/promises";
import { safePath } from "../utils/paths.js";

export async function readFileTool(filePath) {
  return fs.readFile(safePath(filePath), "utf8");
}