# AgentXen - Zen Browser Integration Guide

## 🎯 What This Does

AgentXen integrates directly into Zen Browser (or Firefox) as a native extension with:
- **Chat sidebar** for natural language commands
- **Native messaging** to connect browser ↔ Python agent
- **Ollama integration** for local AI processing
- **Full browser control** through the extension

## 📦 Architecture

```
┌─────────────────────────────────────┐
│     Zen Browser / Firefox           │
│  ┌─────────────────────────────┐    │
│  │  AgentXen Extension         │    │
│  │  - Sidebar UI               │    │
│  │  - Background Script        │    │
│  │  - Content Scripts          │    │
│  └──────────┬──────────────────┘    │
└─────────────┼───────────────────────┘
              │ Native Messaging
              ▼
┌─────────────────────────────────────┐
│  Native Messaging Host (Python)     │
│  - Receives commands from extension │
│  - Talks to Ollama                  │
│  - Controls browser automation      │
└──────────┬──────────────────────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌──────────┐
│ Ollama  │  │Playwright│
│(Gemma1B)│  │ (backup) │
└─────────┘  └──────────┘
```

## 🚀 Quick Installation

### Prerequisites
- Zen Browser (or Firefox) installed
- Python 3.8+
- Ollama installed

### Install Steps

```bash
# 1. Run the installation script
chmod +x install-zen.sh
./install-zen.sh

# 2. Load extension in Zen Browser
# Option A: Temporary (Development)
#   - Open: about:debugging#/runtime/this-firefox
#   - Click: Load Temporary Add-on
#   - Select: extension/manifest.json

# Option B: Permanent
#   - Open: about:addons
#   - Click gear → Install Add-on From File
#   - Select: agentxen-extension.xpi
```

## 🎮 Usage

### Open the Chat Sidebar
1. **Click the extension icon** in the toolbar
2. **Press Alt+Shift+A** (keyboard shortcut)
3. **Or**: Right-click → Sidebars → AgentXen Chat

### Try These Commands
```
Go to reddit.com
Search for AI news on google
Take a screenshot
Click the search button
Extract text from this page
```

### Agent Mode
- Click the extension icon → "Enable Agent Mode"
- The current tab will show a "🤖 Agent Mode" indicator
- Agent can directly interact with page elements

## 🔧 How It Works

### 1. Extension Components

**Sidebar (`sidebar.html` + `sidebar.js`)**
- Chat interface where you type commands
- Shows agent responses and status

**Background Script (`background.js`)**
- Manages native messaging connection
- Routes messages between UI and Python agent
- Handles tab management

**Content Script (`content.js`)**
- Injected into web pages
- Executes actions on the page (click, type, extract)
- Shows "Agent Mode" indicator

### 2. Native Messaging Bridge

**Native Host (`native_host.py`)**
- Python process that browser launches automatically
- Receives JSON messages from extension via stdin/stdout
- Forwards commands to AgentXen controller
- Uses Ollama for AI inference

**Manifest (`native-manifest.json`)**
- Tells browser where to find the Python script
- Installed in `~/.mozilla/native-messaging-hosts/`

### 3. Communication Flow

```
User types in sidebar
      ↓
sidebar.js → background.js
      ↓
Native Messaging (stdio)
      ↓
native_host.py → AgentXenController
      ↓
Ollama (Gemma 1B) → Plan actions
      ↓
Execute via Playwright or content scripts
      ↓
Results back to sidebar
```

## 📁 File Structure

```
agentxen/
├── extension/              # Browser extension
│   ├── manifest.json       # Extension config
│   ├── background.js       # Background service
│   ├── sidebar.html/js     # Chat UI
│   ├── content.js          # Page interaction
│   ├── popup.html/js       # Toolbar popup
│   └── icons/              # Extension icons
├── native_host.py          # Native messaging bridge
├── native-manifest.json    # Native host config
├── src/
│   └── agent.py            # Core agent logic
├── install-zen.sh          # Installation script
└── agentxen-extension.xpi  # Packaged extension
```

## 🐛 Debugging

### Check Native Host Status
```bash
# View native host logs
tail -f /tmp/agentxen-native.log

# Test native host manually
echo '{"type":"command","command":{"text":"test"}}' | python3 native_host.py
```

### Browser Console
1. Open Zen Browser
2. Press F12 → Console
3. Look for AgentXen messages
4. Or go to: `about:debugging#/runtime/this-firefox`

### Common Issues

**"Agent not connected"**
- Check if Ollama is running: `ollama serve`
- Check native host logs: `tail /tmp/agentxen-native.log`
- Verify manifest installed: `ls ~/.mozilla/native-messaging-hosts/`

**Extension won't load**
- Check manifest.json syntax
- Try loading as temporary add-on first
- Check browser console for errors

**Commands not working**
- Ensure Ollama model is pulled: `ollama pull gemma:1b`
- Check venv is activated in native host script
- Test standalone agent: `python src/agent.py`

## 🔄 Development Workflow

### Live Development
```bash
# 1. Start Ollama (separate terminal)
ollama serve

# 2. Load extension as temporary in Zen Browser
# about:debugging#/runtime/this-firefox

# 3. Make changes to extension files
# 4. Click "Reload" in about:debugging

# 5. Test in browser
```

### Testing Native Messaging
```bash
# Manual test
source venv/bin/activate
python3 native_host.py

# Type JSON messages (Ctrl+D to end):
{"type":"command","command":{"text":"test"}}
```

## 🚀 Next Steps

### Current Status: MVP ✅
- ✅ Extension loads in Zen Browser
- ✅ Sidebar chat interface
- ✅ Native messaging bridge
- ✅ Ollama integration (Gemma 1B)
- ✅ Basic browser actions

### Coming Soon
- [ ] Visual element picker (click to select)
- [ ] Multi-tab coordination
- [ ] Session persistence
- [ ] Advanced action chaining
- [ ] Custom Zen Browser build with AgentXen pre-installed

## 📚 Resources

- [Zen Browser](https://zen-browser.app/)
- [Firefox WebExtensions API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)
- [Native Messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging)
- [Ollama](https://ollama.com/)

---

**Status**: Ready to test!  
**Model**: Gemma 1B (fast & lightweight)  
**Compatibility**: Zen Browser, Firefox, LibreWolf, Waterfox
