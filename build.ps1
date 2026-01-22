# Windows Build Script for AgentXen
# Run with: powershell -ExecutionPolicy Bypass -File build.ps1

Write-Host "🚀 Building AgentXen Executable Package (Windows)" -ForegroundColor Cyan
Write-Host "===================================================`n"

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python 3 is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python found: $(python --version)" -ForegroundColor Green

# Create/activate venv
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📦 Installing build dependencies..." -ForegroundColor Yellow
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install -r requirements-build.txt -q

Write-Host "✅ Dependencies installed`n" -ForegroundColor Green

# Clean previous builds
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
Remove-Item -Path build, dist -Recurse -Force -ErrorAction SilentlyContinue

# Build native host
Write-Host "`n🔨 Building native host with PyInstaller..." -ForegroundColor Yellow
pyinstaller agentxen.spec --clean --noconfirm

Write-Host "✅ Native host built" -ForegroundColor Green

# Build launcher
Write-Host "`n🔨 Building launcher GUI..." -ForegroundColor Yellow
pyinstaller --noconfirm --clean `
    --name=AgentXen `
    --windowed `
    --onefile `
    --add-data="extension;extension" `
    --add-data="native-manifest.json;." `
    launcher.py

Write-Host "✅ Launcher built" -ForegroundColor Green

# Create distribution package
Write-Host "`n📦 Creating distribution package..." -ForegroundColor Yellow

$distDir = "dist\AgentXen-Package"
New-Item -Path $distDir -ItemType Directory -Force | Out-Null

# Copy executables
Copy-Item -Path "dist\agentxen-host" -Destination $distDir -Recurse -Force
Copy-Item -Path "dist\AgentXen.exe" -Destination $distDir -Force

# Copy extension
Copy-Item -Path "extension" -Destination $distDir -Recurse -Force

# Copy documentation
Copy-Item -Path "README.md", "ZEN_INTEGRATION.md", "SETUP.md", "DISTRIBUTION.md" -Destination $distDir

# Create install script for Windows
@"
@echo off
echo 🚀 Installing AgentXen...
set INSTALL_DIR=%USERPROFILE%\.agentxen
mkdir "%INSTALL_DIR%" 2>nul
xcopy /E /I /Y agentxen-host "%INSTALL_DIR%\agentxen-host"
xcopy /E /I /Y extension "%INSTALL_DIR%\extension"
echo ✅ Installed to %INSTALL_DIR%
echo Run: AgentXen.exe to launch
pause
"@ | Out-File -FilePath "$distDir\install.bat" -Encoding ASCII

# Create archive
Write-Host "`n📦 Creating archive..." -ForegroundColor Yellow
$archiveName = "AgentXen-Windows-x64.zip"
Compress-Archive -Path "$distDir\*" -DestinationPath "dist\$archiveName" -Force

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✅ Build Complete!" -ForegroundColor Green
Write-Host "================================`n"

Write-Host "Package created:"
Write-Host "  dist\$archiveName"

Write-Host "`nContents:"
Write-Host "  - AgentXen.exe (launcher GUI)"
Write-Host "  - agentxen-host/ (native messaging host)"
Write-Host "  - extension/ (browser extension)"
Write-Host "  - Documentation files"

$size = (Get-Item "dist\$archiveName").Length / 1MB
Write-Host "`nSize: $([math]::Round($size, 2)) MB`n"

Write-Host "To distribute:"
Write-Host "  1. Extract the archive"
Write-Host "  2. Run AgentXen.exe"
Write-Host "  3. Follow the setup wizard`n"
