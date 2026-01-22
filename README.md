# agentxen

AgentXen — Minimal agentic browser demo that connects:
- A small web chat UI (xen-chat)
- An agent server (agent-server)
- Ollama local model (http://localhost:11434)
- Playwright controlling Firefox (headless by default)

Goals (MFP)
- User types a task in the chat UI.
- Agent server asks Ollama for a JSON action plan (structured).
- Server validates the actions and executes them with Playwright.
- Execution updates (and screenshot paths) stream back to the chat UI.

Requirements
- Node.js 18+
- Ollama installed & running (local API at http://localhost:11434)
- Playwright (will need browser binaries)

Quick start (local)
1. Clone this repo locally (or create repository on GitHub and push):
   - See section "Create the GitHub repo" below for commands.

2. Server setup:
   cd agent-server
   npm install
   npx playwright install

3. Start Ollama (desktop or server). Make sure http://localhost:11434 is reachable and you have a small local model pulled (e.g., `gpt-oss` or other small model):
   ollama pull gpt-oss

4. Start the agent server:
   cd agent-server
   npm run dev
   (The WebSocket server listens on ws://localhost:5200)

5. Serve xen-chat and open the UI:
   - Option A: Open xen-chat/chat.html directly in a browser (file:// may block ws connection depending on browser).
   - Option B (recommended): Run a simple static server:
     npx serve xen-chat
     Then open http://localhost:3000/chat.html (or as printed by serve).
   - Type a prompt like:
     "Open https://example.com, click the first link, take a screenshot, and return the page title."

Environment variables
- OLLAMA_URL (optional) — defaults to http://localhost:11434
- OLLAMA_MODEL (optional) — model name, defaults to `gpt-oss`

Create the GitHub repo and push (one-line sequence)
- If you want to make this a GitHub repo under your user (Emmotte) and you have `gh` CLI:
  git init
  git add .
  git commit -m "Initial agentxen MFP"
  gh repo create Emmotte/agentxen --public --source=. --remote=origin --push

Notes & next steps
- The model is instructed to return strictly a JSON array of actions. The server validates using Zod and retries a few times if invalid output appears.
- For more reliability, I can update the Ollama call to pass an explicit JSON schema via the `format` parameter — this reduces invalid outputs.
- For demo simplicity Playwright runs headless; you can set `headless: false` in the Playwright controller to view actions in an opened Firefox window.

License: MIT (see LICENSE file)