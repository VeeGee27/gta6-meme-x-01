import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// Copy POST.json from this repository into the run's output directory.
// That is all this program has to do: the house reads the post from X.
// The placeholder URL in POST.json is replaced with the real post address
// by the entrant before submitting; this program never edits it.
const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
