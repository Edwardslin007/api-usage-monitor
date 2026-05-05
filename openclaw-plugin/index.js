import { readFileSync } from "node:fs";
import path from "node:path";
import os from "node:os";

const CACHE_FILE = path.join(os.homedir(), ".openclaw/scripts/usage_cache.txt");

function getUsageInfo() {
  try {
    return readFileSync(CACHE_FILE, "utf-8").trim();
  } catch {
    return null;
  }
}

export default {
  id: "aicodee-usage-hook",
  name: "Aicodee Usage Hook",
  description: "Appends API usage info to agent replies",
  register(api) {
    api.on("message_sending", async (event) => {
      const usage = getUsageInfo();
      if (!usage || !event.content) return;
      if (event.content.includes("📊")) return;
      return { content: event.content + "\n\n> _📊 " + usage + "_" };
    });
  },
};
