import path from "path";

const root = process.cwd();

export function safePath(inputPath) {
  const resolved = path.resolve(root, inputPath);

  if (!resolved.startsWith(root)) {
    throw new Error("Akses keluar folder ditolak");
  }

  return resolved;
}