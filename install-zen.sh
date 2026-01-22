#!/bin/bash

# AgentXen Installation Script for Zen Browser Integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/bin"
NATIVE_MANIFEST_DIR="$HOME/.mozilla/native-messaging-hosts"

echo "🚀 Installing AgentXen for Zen Browser"
echo "========================================"
echo ""

# Check for required commands
for cmd in python3 ollama; do
  if ! command -v $cmd &> /dev/null; then
    echo "❌ $cmd is not installed. Please install it first."
    exit 1
  fi
done

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q playwright
playwright install firefox

echo "✅ Python dependencies installed"

# Step 2: Pull Ollama model
echo ""
echo "🤖 Pulling Gemma 1B model..."
ollama pull gemma:1b
echo "✅ Model ready"

# Step 3: Install native messaging host
echo ""
echo "🔧 Installing native messaging host..."

# Create wrapper script
sudo tee "$INSTALL_DIR/agentxen-host" > /dev/null << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
source venv/bin/activate
python3 "$SCRIPT_DIR/native_host.py"
EOF

sudo chmod +x "$INSTALL_DIR/agentxen-host"
echo "✅ Native host installed"

# Step 4: Install native manifest
echo ""
echo "📝 Installing native messaging manifest..."
mkdir -p "$NATIVE_MANIFEST_DIR"

# Update manifest with correct path
cat native-manifest.json | \
  sed "s|/usr/local/bin/agentxen-host|$INSTALL_DIR/agentxen-host|" > \
  "$NATIVE_MANIFEST_DIR/agentxen.json"

echo "✅ Manifest installed at: $NATIVE_MANIFEST_DIR/agentxen.json"

# Step 5: Extension icons
echo ""
echo "🎨 Creating extension icons..."
mkdir -p extension/icons

# Create simple placeholder icons (you can replace with actual icons)
cat > extension/icons/icon-48.png << 'ICON_DATA'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==
ICON_DATA

cp extension/icons/icon-48.png extension/icons/icon-96.png

echo "✅ Icons created"

# Step 6: Package extension
echo ""
echo "📦 Packaging extension..."
cd extension
zip -r ../agentxen-extension.xpi * > /dev/null
cd ..
echo "✅ Extension packaged: agentxen-extension.xpi"

echo ""
echo "================================"
echo "✅ Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Download Zen Browser: https://zen-browser.app/"
echo "  2. Open Zen Browser"
echo "  3. Go to: about:addons"
echo "  4. Click gear icon → Install Add-on From File"
echo "  5. Select: $SCRIPT_DIR/agentxen-extension.xpi"
echo "  6. Open the sidebar (Alt+Shift+A or click extension icon)"
echo ""
echo "Or for development:"
echo "  1. Go to: about:debugging#/runtime/this-firefox"
echo "  2. Click 'Load Temporary Add-on'"
echo "  3. Select: $SCRIPT_DIR/extension/manifest.json"
echo ""
echo "Test the connection:"
echo "  - Open Zen Browser"
echo "  - The extension should auto-connect to the native host"
echo "  - Check /tmp/agentxen-native.log for debug info"
echo ""
