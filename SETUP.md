# AgentXen Setup & Usage Guide

## Prerequisites

- **Python 3.8+**
- **Node.js 16+** (for future extension development)
- **Ollama** - Local AI runtime
- **Git**

## Quick Setup

### 1. Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from [https://ollama.com/download](https://ollama.com/download)

### 2. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create Python virtual environment
- Install dependencies (Playwright, Ollama SDK)
- Download Playwright Firefox
- Pull Gemma 1B model

### 3. Start AgentXen

```bash
source venv/bin/activate
python src/agent.py
```

## Manual Setup

If the setup script doesn't work, follow these steps:

### Step 1: Python Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Install Playwright Browser

```bash
playwright install firefox
```

### Step 3: Pull AI Model

```bash
ollama pull gemma:1b
```

Make sure Ollama service is running:
```bash
ollama serve  # Run in a separate terminal
```

### Step 4: Run Agent

```bash
python src/agent.py
```

## Usage Examples

Once AgentXen is running, try these commands:

```
💬 You: Go to google.com
💬 You: Search for artificial intelligence
💬 You: Open reddit.com and show trending posts
💬 You: Navigate to github.com/trending
💬 You: Take a screenshot
```

## Troubleshooting

### Ollama Connection Failed

```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Pull the model if not present
ollama pull gemma:1b
```

### Playwright Browser Not Found

```bash
# Reinstall browsers
playwright install firefox

# Or install all browsers
playwright install
```

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Project Structure

```
agentxen/
├── src/
│   └── agent.py          # Main agent controller
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies (future)
├── setup.sh              # Automated setup script
└── README.md             # This file
```

## Next Steps

This is a basic MVP implementation. Upcoming features:

1. **Zen Browser Integration** - Custom browser UI with chat interface
2. **Advanced Action Planning** - Multi-step task execution
3. **Session Persistence** - Save and restore browsing sessions
4. **Security Sandbox** - Safe execution environment
5. **Extension System** - Plugin architecture for custom actions

## Development

To contribute or modify:

```bash
# Activate environment
source venv/bin/activate

# Run in development mode with auto-reload
nodemon src/agent.py  # Requires nodemon: npm i -g nodemon

# Run tests (when available)
pytest tests/
```

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Playwright Python](https://playwright.dev/python/)
- [Zen Browser](https://github.com/zen-browser/www)

---

**Status**: MVP - Basic functionality working
**Model**: Gemma 1B (ultra-lightweight, ~1GB)
**License**: MIT (to be confirmed)
