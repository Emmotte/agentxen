# Building AgentXen Executables

This guide covers building executable packages for Windows, Linux, and macOS.

## 🔧 Build Methods

### Method 1: GitHub Actions (Recommended)

The easiest way to build Windows executables is using GitHub Actions, which runs on actual Windows machines.

**Steps:**

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add build workflow"
   git push origin main
   ```

2. **Trigger Build**:
   - Go to GitHub: `Actions` tab
   - Click `Build Windows Executable`
   - Click `Run workflow`

3. **Download**:
   - Once complete, download artifacts
   - `AgentXen-Windows-x64.zip`
   - `AgentXen-Linux-x64.tar.gz`
   - `AgentXen-macOS-x64.tar.gz`

**Or create a release:**
```bash
git tag v0.1.0
git push origin v0.1.0
```

This automatically builds and creates a GitHub release with all platform binaries.

### Method 2: Build on Windows Machine

If you have access to a Windows machine:

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/Emmotte/agentxen.git
   cd agentxen
   ```

2. **Run build script**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File build.ps1
   ```

3. **Output**:
   ```
   dist/AgentXen-Windows-x64.zip
   ```

### Method 3: Cross-Compilation with Wine (Linux)

Build Windows executables from Linux using Wine:

**Setup (one-time):**
```bash
# Install Wine
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install wine64 wine32

# Install Python in Wine
wget https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
wine python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Install pip packages in Wine
wine python -m pip install --upgrade pip
wine pip install -r requirements.txt
wine pip install -r requirements-build.txt
```

**Build:**
```bash
wine pyinstaller agentxen.spec --clean --noconfirm
wine pyinstaller --noconfirm --clean \
  --name=AgentXen \
  --windowed \
  --onefile \
  --add-data="extension;extension" \
  --add-data="native-manifest.json;." \
  launcher.py
```

### Method 4: Docker with Windows Container

Use Docker Desktop with Windows containers (requires Windows 10/11):

```dockerfile
# Dockerfile.windows
FROM mcr.microsoft.com/windows/servercore:ltsc2022
SHELL ["powershell", "-Command"]

RUN Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -OutFile python.exe
RUN Start-Process python.exe -Wait -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1'

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -r requirements-build.txt

CMD ["powershell", "-File", "build.ps1"]
```

## 📦 Platform-Specific Builds

### Windows (.exe)
```powershell
# On Windows
build.ps1

# Output: dist/AgentXen-Windows-x64.zip
# Contains:
#   - AgentXen.exe (GUI launcher)
#   - agentxen-host.exe (native host)
#   - extension/ (browser extension)
```

### Linux (.tar.gz)
```bash
# On Linux
./build.sh

# Output: dist/AgentXen-Linux-x64.tar.gz
# Contains:
#   - AgentXen (GUI launcher)
#   - agentxen-host (native host)
#   - extension/ (browser extension)
```

### macOS (.tar.gz)
```bash
# On macOS
./build.sh

# Output: dist/AgentXen-macOS-x64.tar.gz
# Contains:
#   - AgentXen.app (GUI launcher)
#   - agentxen-host (native host)
#   - extension/ (browser extension)
```

## 🚀 Quick Start for Users

**Windows:**
1. Download `AgentXen-Windows-x64.zip`
2. Extract to a folder
3. Run `AgentXen.exe`
4. Follow installation wizard

**Linux:**
1. Download `AgentXen-Linux-x64.tar.gz`
2. Extract: `tar -xzf AgentXen-Linux-x64.tar.gz`
3. Run: `./AgentXen-Package/AgentXen`

**macOS:**
1. Download `AgentXen-macOS-x64.tar.gz`
2. Extract: `tar -xzf AgentXen-macOS-x64.tar.gz`
3. Run: `./AgentXen-Package/AgentXen`

## 🔍 Troubleshooting Builds

### PyInstaller Issues

**Missing modules:**
```bash
# Add to hiddenimports in agentxen.spec
hiddenimports=['missing_module']
```

**Large executable size:**
```bash
# Use UPX compression (already enabled)
# Or exclude unnecessary packages
excludes=['matplotlib', 'numpy']
```

**Runtime errors:**
```bash
# Check for missing data files
datas=[('path/to/file', 'destination')]
```

### Windows Build Errors

**"Python not found":**
- Install Python 3.11 from python.org
- Ensure Python is in PATH

**"PyInstaller failed":**
```powershell
# Clean and rebuild
Remove-Item -Recurse -Force build, dist
pip install --upgrade pyinstaller
```

### Wine Build Issues

**"Wine not installed":**
```bash
sudo apt install wine64 wine32
```

**"Python installation failed":**
```bash
# Use winetricks
sudo apt install winetricks
winetricks python311
```

## 📊 Build Sizes

Approximate sizes of built packages:

- **Windows**: ~150-200 MB (includes Python runtime + dependencies)
- **Linux**: ~120-150 MB
- **macOS**: ~130-160 MB

Sizes can be reduced by:
- Using `--onefile` mode (slower startup)
- Excluding unused modules
- Compressing with UPX (already enabled)
- Not including certain Playwright browsers

## 🔒 Code Signing (Optional)

### Windows
```powershell
# Sign with certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com AgentXen.exe
```

### macOS
```bash
# Sign with Apple Developer ID
codesign --force --sign "Developer ID Application" --timestamp AgentXen.app
```

### Linux
```bash
# Create checksum for verification
sha256sum AgentXen > AgentXen.sha256
```

## 📚 Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Wine HQ](https://www.winehq.org/)
- [Code Signing Guide](https://www.ssl.com/guide/code-signing-best-practices/)

## 🆘 Need Help?

If you can't build locally:
1. Use GitHub Actions (no local Windows needed)
2. Ask in GitHub Issues
3. Pre-built releases available on GitHub

---

**Recommended**: Use GitHub Actions for building Windows executables. It's free, reliable, and produces properly compiled binaries.
