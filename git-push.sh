#!/bin/bash
set -e

cd /workspaces/agentxen

echo "📝 Staging all files..."
git add -A

echo "📋 Checking status..."
git status --short

echo "💾 Committing..."
git commit -m "Add AgentXen MVP: Complete browser agent with Zen integration, Ollama/Gemma 1B, and multi-platform builds

- Python agent with Ollama (Gemma 1B) and Playwright integration
- Complete Firefox/Zen Browser extension with native messaging
- Chat sidebar UI for natural language commands  
- Native messaging bridge for extension ↔ agent communication
- GUI launcher with Tkinter for easy installation
- PyInstaller packaging for standalone executables
- Build scripts for Windows/Linux/macOS (build.sh, build.ps1)
- GitHub Actions workflow for automated multi-platform builds
- Comprehensive documentation (README, setup guides, integration docs)

This commit implements the full MVP as requested: lightweight agentic browser
using Zen Browser, Ollama with very small model (Gemma 1B), and executable packaging."

echo "🚀 Pushing to origin..."
git push origin main

echo "✅ Push complete!"
echo ""
echo "Next steps:"
echo "1. Go to GitHub Actions tab to see the build"
echo "2. Or create a release tag: git tag v0.1.0 && git push origin v0.1.0"
