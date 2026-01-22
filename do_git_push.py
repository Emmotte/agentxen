#!/usr/bin/env python3
"""
Simple script to commit and push changes to GitHub
"""
import subprocess
import sys
import os

os.chdir('/workspaces/agentxen')

def run(cmd):
    """Run a command and show output"""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"❌ Command failed with code {result.returncode}")
        return False
    return True

print("🚀 Starting git push process...")
print("="*60)

# Stage all files
if not run("git add -A"):
    sys.exit(1)

# Show status
run("git status --short")

# Commit
commit_msg = """Add AgentXen MVP: Complete browser agent with Zen integration, Ollama/Gemma 1B, and multi-platform builds

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
using Zen Browser, Ollama with very small model (Gemma 1B), and executable packaging."""

if not run(f'git commit -m "{commit_msg}"'):
    print("\n⚠️ Nothing to commit or commit failed")
    # Check if there are already committed changes to push
    result = subprocess.run("git status", shell=True, capture_output=True, text=True)
    if "nothing to commit" in result.stdout:
        print("✅ All changes already committed")
    else:
        sys.exit(1)

# Push to origin
print("\n🚀 Pushing to GitHub...")
if not run("git push origin main"):
    sys.exit(1)

print("\n" + "="*60)
print("✅ Successfully pushed to GitHub!")
print("="*60)
print("\nNext steps:")
print("1. Visit: https://github.com/Emmotte/agentxen/actions")
print("2. Watch the build process")
print("3. Download artifacts when complete")
print("\nOr create a release tag for automatic GitHub release:")
print("   git tag v0.1.0")
print("   git push origin v0.1.0")
