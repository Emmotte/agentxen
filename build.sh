#!/bin/bash

# AgentXen Build Script - Package to executable

set -e

echo "🚀 Building AgentXen Executable Package"
echo "========================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create/activate venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q -r requirements-build.txt

echo "✅ Dependencies installed"

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec 2>/dev/null || true

# Build native host
echo ""
echo "🔨 Building native host with PyInstaller..."
pyinstaller agentxen.spec --clean --noconfirm

echo "✅ Native host built"

# Build launcher
echo ""
echo "🔨 Building launcher GUI..."
pyinstaller --noconfirm --clean \
    --name=AgentXen \
    --windowed \
    --onefile \
    --add-data="extension:extension" \
    --add-data="native-manifest.json:." \
    launcher.py

echo "✅ Launcher built"

# Create distribution package
echo ""
echo "📦 Creating distribution package..."

DIST_DIR="dist/AgentXen-Package"
mkdir -p "$DIST_DIR"

# Copy executables
cp -r dist/agentxen-host "$DIST_DIR/"
cp dist/AgentXen "$DIST_DIR/"

# Copy extension
cp -r extension "$DIST_DIR/"

# Copy documentation
cp README.md "$DIST_DIR/"
cp ZEN_INTEGRATION.md "$DIST_DIR/"
cp SETUP.md "$DIST_DIR/"

# Create install script for Linux/Mac
cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash
echo "🚀 Installing AgentXen..."
INSTALL_DIR="$HOME/.agentxen"
mkdir -p "$INSTALL_DIR"
cp -r agentxen-host "$INSTALL_DIR/"
cp -r extension "$INSTALL_DIR/"
echo "✅ Installed to $INSTALL_DIR"
echo "Run: ./AgentXen to launch"
EOF

chmod +x "$DIST_DIR/install.sh"
chmod +x "$DIST_DIR/AgentXen"
chmod +x "$DIST_DIR/agentxen-host/agentxen-host"

# Create archive
echo ""
echo "📦 Creating archive..."
cd dist
tar -czf AgentXen-$(uname -s)-$(uname -m).tar.gz AgentXen-Package/
cd ..

echo ""
echo "================================"
echo "✅ Build Complete!"
echo "================================"
echo ""
echo "Package created:"
echo "  dist/AgentXen-$(uname -s)-$(uname -m).tar.gz"
echo ""
echo "Contents:"
echo "  - AgentXen (launcher GUI)"
echo "  - agentxen-host/ (native messaging host)"
echo "  - extension/ (browser extension)"
echo "  - Documentation files"
echo ""
echo "To distribute:"
echo "  1. Extract the archive"
echo "  2. Run ./AgentXen"
echo "  3. Follow the setup wizard"
echo ""
echo "Size: $(du -h dist/AgentXen-*.tar.gz | cut -f1)"
echo ""
