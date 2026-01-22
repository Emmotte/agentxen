#!/usr/bin/env python3
"""
AgentXen Launcher - Main entry point for packaged application
Manages Ollama and browser extension installation
"""

import os
import sys
import json
import shutil
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import webbrowser

class AgentXenLauncher:
    """GUI launcher for AgentXen"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AgentXen Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Paths
        if getattr(sys, 'frozen', False):
            self.app_dir = Path(sys._MEIPASS)
            self.install_dir = Path(os.path.expanduser("~/.agentxen"))
        else:
            self.app_dir = Path(__file__).parent
            self.install_dir = self.app_dir
        
        self.setup_ui()
        self.check_installation()
    
    def setup_ui(self):
        """Create the UI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(self.root, bg="#0084ff", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header, 
            text="🤖 AgentXen", 
            font=("Arial", 24, "bold"),
            bg="#0084ff",
            fg="white"
        )
        title.pack(pady=20)
        
        # Main content
        content = tk.Frame(self.root, padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_label = tk.Label(
            content,
            text="Checking installation...",
            font=("Arial", 12),
            fg="#666"
        )
        self.status_label.pack(pady=10)
        
        # Progress
        self.progress = ttk.Progressbar(
            content,
            length=400,
            mode='indeterminate'
        )
        self.progress.pack(pady=10)
        
        # Info text
        info_frame = tk.Frame(content)
        info_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(
            info_frame,
            height=10,
            font=("Courier", 9),
            bg="#f5f5f5",
            wrap=tk.WORD
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(content)
        button_frame.pack(pady=20)
        
        self.install_btn = tk.Button(
            button_frame,
            text="Install",
            command=self.install,
            font=("Arial", 12, "bold"),
            bg="#0084ff",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        self.launch_btn = tk.Button(
            button_frame,
            text="Open Browser Extension",
            command=self.open_extension,
            font=("Arial", 12),
            padx=20,
            pady=10,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.launch_btn.pack(side=tk.LEFT, padx=5)
        
        self.help_btn = tk.Button(
            button_frame,
            text="Help",
            command=self.show_help,
            font=("Arial", 12),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.help_btn.pack(side=tk.LEFT, padx=5)
    
    def log(self, message):
        """Add message to log"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.root.update()
    
    def check_installation(self):
        """Check if components are installed"""
        self.log("Checking installation status...")
        
        # Check Ollama
        ollama_installed = shutil.which('ollama') is not None
        self.log(f"✅ Ollama: {'Installed' if ollama_installed else '❌ Not installed'}")
        
        # Check native manifest
        system = platform.system()
        if system == "Linux" or system == "Darwin":
            manifest_dir = Path.home() / ".mozilla" / "native-messaging-hosts"
        elif system == "Windows":
            manifest_dir = Path.home() / "AppData" / "Roaming" / "Mozilla" / "NativeMessagingHosts"
        else:
            manifest_dir = None
        
        manifest_exists = manifest_dir and (manifest_dir / "agentxen.json").exists()
        self.log(f"{'✅' if manifest_exists else '❌'} Native messaging: {'Configured' if manifest_exists else 'Not configured'}")
        
        # Check model
        model_exists = False
        if ollama_installed:
            try:
                result = subprocess.run(
                    ['ollama', 'list'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                model_exists = 'gemma:1b' in result.stdout
            except:
                pass
        
        self.log(f"{'✅' if model_exists else '❌'} Gemma 1B model: {'Downloaded' if model_exists else 'Not downloaded'}")
        
        self.progress.stop()
        
        if ollama_installed and manifest_exists and model_exists:
            self.status_label.config(text="✅ Ready to use!", fg="#4caf50")
            self.install_btn.config(text="Reinstall")
            self.launch_btn.config(state=tk.NORMAL)
        elif ollama_installed and manifest_exists:
            self.status_label.config(text="⚠️ Model needs to be downloaded", fg="#ff9800")
            self.install_btn.config(text="Download Model")
        else:
            self.status_label.config(text="❌ Installation required", fg="#f44336")
            self.install_btn.config(text="Install")
    
    def install(self):
        """Run installation"""
        self.install_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.log("\n📦 Starting installation...")
        
        try:
            # Check Ollama
            if not shutil.which('ollama'):
                self.log("\n❌ Ollama not found!")
                self.log("Please install Ollama first:")
                self.log("  Linux: curl -fsSL https://ollama.com/install.sh | sh")
                self.log("  macOS: brew install ollama")
                self.log("  Windows: Download from https://ollama.com/download")
                messagebox.showerror(
                    "Ollama Required",
                    "Please install Ollama first.\nVisit: https://ollama.com"
                )
                self.progress.stop()
                self.install_btn.config(state=tk.NORMAL)
                return
            
            self.log("✅ Ollama found")
            
            # Pull model
            self.log("\n🤖 Downloading Gemma 1B model (this may take a few minutes)...")
            result = subprocess.run(
                ['ollama', 'pull', 'gemma:1b'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("✅ Model downloaded")
            else:
                self.log(f"⚠️ Model download issue: {result.stderr}")
            
            # Install native manifest
            self.log("\n📝 Installing native messaging manifest...")
            self.install_native_manifest()
            
            # Install extension files
            self.log("\n📦 Installing extension files...")
            extension_dest = self.install_dir / "extension"
            extension_dest.mkdir(parents=True, exist_ok=True)
            
            extension_src = self.app_dir / "extension"
            if extension_src.exists():
                shutil.copytree(extension_src, extension_dest, dirs_exist_ok=True)
                self.log("✅ Extension files copied")
            
            self.log("\n✅ Installation complete!")
            self.status_label.config(text="✅ Installation successful!", fg="#4caf50")
            self.launch_btn.config(state=tk.NORMAL)
            
            messagebox.showinfo(
                "Success",
                "AgentXen installed successfully!\n\nNext steps:\n"
                "1. Click 'Open Browser Extension'\n"
                "2. Load the extension in your browser\n"
                "3. Start using AgentXen!"
            )
            
        except Exception as e:
            self.log(f"\n❌ Error: {e}")
            messagebox.showerror("Installation Error", str(e))
        finally:
            self.progress.stop()
            self.install_btn.config(state=tk.NORMAL)
    
    def install_native_manifest(self):
        """Install native messaging manifest"""
        system = platform.system()
        
        if system == "Linux" or system == "Darwin":
            manifest_dir = Path.home() / ".mozilla" / "native-messaging-hosts"
        elif system == "Windows":
            manifest_dir = Path.home() / "AppData" / "Roaming" / "Mozilla" / "NativeMessagingHosts"
        else:
            raise Exception(f"Unsupported platform: {system}")
        
        manifest_dir.mkdir(parents=True, exist_ok=True)
        
        # Get host executable path
        if getattr(sys, 'frozen', False):
            # Packaged
            host_path = Path(sys.executable).parent / "agentxen-host"
            if system == "Windows":
                host_path = host_path.with_suffix(".exe")
        else:
            # Development
            host_path = self.app_dir / "native_host.py"
        
        manifest = {
            "name": "agentxen",
            "description": "AgentXen Native Messaging Host",
            "path": str(host_path),
            "type": "stdio",
            "allowed_extensions": ["agentxen@zen-browser.local"]
        }
        
        manifest_file = manifest_dir / "agentxen.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        self.log(f"✅ Manifest installed: {manifest_file}")
    
    def open_extension(self):
        """Open extension directory"""
        extension_dir = self.install_dir / "extension"
        
        if not extension_dir.exists():
            extension_dir = self.app_dir / "extension"
        
        if extension_dir.exists():
            # Open file manager
            system = platform.system()
            if system == "Windows":
                os.startfile(extension_dir)
            elif system == "Darwin":
                subprocess.run(['open', extension_dir])
            else:
                subprocess.run(['xdg-open', extension_dir])
            
            # Open browser instructions
            webbrowser.open('about:debugging#/runtime/this-firefox')
            
            messagebox.showinfo(
                "Load Extension",
                f"Extension files: {extension_dir}\n\n"
                "In your browser:\n"
                "1. Go to: about:debugging#/runtime/this-firefox\n"
                "2. Click 'Load Temporary Add-on'\n"
                "3. Select: manifest.json from the extension folder\n"
                "4. Open sidebar with Alt+Shift+A"
            )
        else:
            messagebox.showerror("Error", "Extension files not found!")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
AgentXen - AI-Powered Browser Agent

INSTALLATION:
1. Install Ollama (https://ollama.com)
2. Click 'Install' button
3. Load extension in Zen Browser/Firefox

USAGE:
1. Load extension in browser
2. Open sidebar (Alt+Shift+A)
3. Type natural language commands

COMMANDS:
- Go to google.com
- Search for AI news
- Take a screenshot
- Click the search button
- Extract text from this page

TROUBLESHOOTING:
- Check /tmp/agentxen-native.log (Linux/Mac)
- Ensure Ollama is running: ollama serve
- Browser console: F12 → Console

DOCUMENTATION:
See README.md and ZEN_INTEGRATION.md
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("AgentXen Help")
        help_window.geometry("500x600")
        
        text = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(1.0, help_text)
        text.config(state=tk.DISABLED)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == '__main__':
    app = AgentXenLauncher()
    app.run()
