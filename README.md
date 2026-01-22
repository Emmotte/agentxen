# AgentXen 🤖🌐

**An AI-Powered Agentic Browser**

AgentXen is a lightweight, intelligent browser agent built on Zen Browser (Firefox fork) that allows you to control web browsing through natural language commands. Using local AI with Ollama and Playwright automation, AgentXen can perform complex web tasks autonomously.

## ✨ Features

- 🗣️ **Natural Language Control**: Chat with your browser to perform tasks
- 🤖 **Local AI**: Uses Ollama with small, efficient models (no cloud dependency)
- 🎭 **Dual Mode Tabs**: Switch between agent-controlled and manual browsing
- ⚡ **Fast & Lightweight**: Optimized for local execution
- 🔒 **Privacy-First**: All processing happens on your machine
- 🎯 **Task-Oriented**: Perfect for web automation, research, and data extraction

## 🏗️ Architecture

- **Browser Base**: Zen Browser (Firefox fork)
- **AI Engine**: Ollama with Gemma 1B (ultra-lightweight, <2GB)
- **Automation**: Playwright for reliable browser control
- **UI**: Integrated chat interface for task input

## 🚀 Quick Start

### Installation
```bash
# Install for Zen Browser integration
chmod +x install-zen.sh
./install-zen.sh

# Load extension in Zen Browser (or Firefox)
# 1. Open: about:debugging#/runtime/this-firefox
# 2. Click: Load Temporary Add-on
# 3. Select: extension/manifest.json
```

See [ZEN_INTEGRATION.md](ZEN_INTEGRATION.md) for detailed instructions.

## 📋 Project Status

This project is currently in **initial development**. See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete roadmap and [PROGRESS.md](PROGRESS.md) for current status.

## 🤝 Contributing

This is an active development project. If you're another agent or contributor working in this space, please check and update [PROGRESS.md](PROGRESS.md) to coordinate efforts.

## 📚 Resources

- [Zen Browser](https://github.com/zen-browser/www)
- [Playwright](https://github.com/microsoft/playwright)
- [Ollama](https://github.com/ollama/ollama)

## � Building Executable Package

```bash
# Build distributable package
chmod +x build.sh
./build.sh

# Output: dist/AgentXen-[OS]-[ARCH].tar.gz
```

See [DISTRIBUTION.md](DISTRIBUTION.md) for distribution details.

## �📄 License

*(To be determined)*

---

**For detailed project planning and architecture, see [PROJECT_PLAN.md](PROJECT_PLAN.md)**