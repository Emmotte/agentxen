# AgentXen Distribution Package

## 📦 What's Included

This is a self-contained distribution of AgentXen that includes:
- **AgentXen Launcher** - GUI installer and manager
- **Native Host** - Packaged Python agent with Ollama integration
- **Browser Extension** - Firefox/Zen Browser extension
- **Documentation** - Setup guides and usage instructions

## 🚀 Quick Start

### 1. Prerequisites

**Install Ollama** (required):
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- **macOS**: `brew install ollama` or download from [ollama.com](https://ollama.com)
- **Windows**: Download from [ollama.com/download](https://ollama.com/download)

**Install Zen Browser** (or Firefox):
- Download from [zen-browser.app](https://zen-browser.app/)
- Or use Firefox, LibreWolf, Waterfox, etc.

### 2. Extract and Run

```bash
# Extract the package
tar -xzf AgentXen-*.tar.gz
cd AgentXen-Package

# Run the launcher
./AgentXen
```

### 3. Installation Steps

The launcher GUI will guide you through:

1. **Check Dependencies** - Verifies Ollama is installed
2. **Download Model** - Pulls Gemma 1B (1-2 GB download)
3. **Install Native Host** - Sets up browser communication
4. **Configure Extension** - Prepares browser extension

### 4. Load Browser Extension

After installation:

1. **Open your browser** (Zen Browser or Firefox)
2. **Go to**: `about:debugging#/runtime/this-firefox`
3. **Click**: "Load Temporary Add-on"
4. **Select**: `extension/manifest.json` from the installation directory
5. **Open Sidebar**: Press `Alt+Shift+A` or click the extension icon

## 📖 Usage

Once installed, open the sidebar and try these commands:

```
Go to reddit.com
Search for AI news on google
Take a screenshot
Navigate to github.com/trending
Extract the main heading from this page
```

## 🏗️ Architecture

```
┌─────────────────────┐
│   Zen Browser       │
│   ┌─────────────┐   │
│   │  Extension  │   │
│   │  (Sidebar)  │   │
│   └──────┬──────┘   │
└──────────┼──────────┘
           │ Native Messaging
           ▼
┌─────────────────────┐
│  agentxen-host      │
│  (Python Agent)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Ollama (Gemma 1B)  │
│  (Local AI)         │
└─────────────────────┘
```

## 📁 Package Contents

```
AgentXen-Package/
├── AgentXen              # Launcher GUI (run this)
├── agentxen-host/        # Packaged native host
│   ├── agentxen-host     # Main executable
│   └── [dependencies]    # Bundled Python libs
├── extension/            # Browser extension
│   ├── manifest.json
│   ├── sidebar.html/js
│   ├── background.js
│   └── [other files]
├── README.md             # Main documentation
├── ZEN_INTEGRATION.md    # Integration guide
├── SETUP.md              # Setup instructions
└── install.sh            # CLI installation script
```

## 🔧 Manual Installation (Advanced)

If you prefer not to use the GUI launcher:

```bash
# 1. Install to home directory
./install.sh

# 2. Pull Ollama model
ollama pull gemma:1b

# 3. Install native manifest
mkdir -p ~/.mozilla/native-messaging-hosts
cp native-manifest.json ~/.mozilla/native-messaging-hosts/agentxen.json

# 4. Update manifest path
# Edit ~/.mozilla/native-messaging-hosts/agentxen.json
# Set "path" to full path of agentxen-host executable

# 5. Load extension in browser
# about:debugging → Load Temporary Add-on → select extension/manifest.json
```

## 🐛 Troubleshooting

### "Ollama not found"
Install Ollama from [ollama.com](https://ollama.com)

### "Agent not connected"
1. Check if Ollama is running: `ollama serve`
2. Check native host logs: 
   - Linux/Mac: `/tmp/agentxen-native.log`
   - Windows: `%TEMP%\agentxen-native.log`
3. Verify manifest is installed: `ls ~/.mozilla/native-messaging-hosts/`

### Extension won't load
1. Check browser console (F12)
2. Try loading as temporary add-on first
3. Ensure manifest.json has correct permissions

### Commands not working
1. Verify model is downloaded: `ollama list`
2. Test Ollama: `ollama run gemma:1b "hello"`
3. Check extension is connected (status indicator in sidebar)

## 📊 System Requirements

- **OS**: Linux, macOS, or Windows
- **RAM**: 4GB minimum (8GB recommended for Gemma 1B)
- **Storage**: 3GB (2GB for model, 1GB for application)
- **Browser**: Zen Browser, Firefox 91+, or compatible fork

## 🔒 Privacy

- ✅ **100% Local** - All processing on your machine
- ✅ **No Cloud** - No data sent to external servers
- ✅ **Open Source** - Inspect the code anytime
- ✅ **Private** - Your browsing and commands stay with you

## 📚 Documentation

- **README.md** - Project overview
- **ZEN_INTEGRATION.md** - Browser integration details
- **SETUP.md** - Development setup guide
- **Online**: [github.com/Emmotte/agentxen](https://github.com/Emmotte/agentxen)

## 🆘 Support

For issues or questions:
1. Check the documentation files
2. Review logs in `/tmp/agentxen-native.log`
3. Open an issue on GitHub
4. Check browser console for errors

## 📄 License

MIT (to be confirmed)

---

**Version**: 0.1.0  
**Build Date**: 2026-01-22  
**Model**: Gemma 1B (via Ollama)  
**Compatible**: Zen Browser, Firefox, LibreWolf, Waterfox
