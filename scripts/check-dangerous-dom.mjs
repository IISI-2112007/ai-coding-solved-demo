import { readdir, readFile } from "node:fs/promises";
import { extname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const sourceRoot = join(root, "src");
const forbidden = [
  { id: "A05", label: "innerHTML 指派", pattern: /\.innerHTML\s*=/u },
  { id: "A05", label: "outerHTML 指派", pattern: /\.outerHTML\s*=/u },
  { id: "A05", label: "insertAdjacentHTML", pattern: /\.insertAdjacentHTML\s*\(/u },
  { id: "A05", label: "document.write", pattern: /document\.write\s*\(/u },
  { id: "A05", label: "eval", pattern: /\beval\s*\(/u },
  { id: "A05", label: "Function constructor", pattern: /\bnew\s+Function\s*\(/u },
];

async function collectFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(
    entries.map((entry) => {
      const path = join(directory, entry.name);
      return entry.isDirectory() ? collectFiles(path) : [path];
    }),
  );
  return nested.flat().filter((path) => [".ts", ".js", ".mjs"].includes(extname(path)));
}

const findings = [];
for (const path of await collectFiles(sourceRoot)) {
  const content = await readFile(path, "utf8");
  const lines = content.split(/\r?\n/u);
  lines.forEach((line, index) => {
    forbidden.forEach((rule) => {
      if (rule.pattern.test(line)) {
        findings.push(`${relative(root, path)}:${index + 1} ${rule.id} ${rule.label}`);
      }
    });
  });
}

if (findings.length > 0) {
  console.error("DOM XSS 安全閘門失敗：\n" + findings.join("\n"));
  process.exitCode = 1;
} else {
  console.log(`DOM XSS 安全閘門通過：已檢查 ${sourceRoot}`);
}
