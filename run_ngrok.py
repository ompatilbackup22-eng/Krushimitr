#!/usr/bin/env python3
"""
Script to run KrishiMitra app with ngrok for internet access
This allows access from anywhere, not just local network
"""

import subprocess
import sys
import time
import webbrowser
import requests
import json

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        subprocess.run(["ngrok", "version"], check=True, capture_output=True)
        return True
    except:
        return False

def install_ngrok_instructions():
    """Show instructions to install ngrok"""
    print("📦 ngrok is not installed. Here's how to install it:")
    print()
    print("1. Go to: https://ngrok.com/download")
    print("2. Download ngrok for Windows")
    print("3. Extract the .exe file to a folder")
    print("4. Add that folder to your PATH environment variable")
    print("5. Or run this script from the same folder as ngrok.exe")
    print()
    print("Alternative: Install via Chocolatey:")
    print("   choco install ngrok")
    print()
    print("Alternative: Install via Scoop:")
    print("   scoop install ngrok")

def get_ngrok_url():
    """Get the public URL from ngrok"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        if data['tunnels']:
            return data['tunnels'][0]['public_url']
    except:
        pass
    return None

def main():
    print("🌐 KrishiMitra: Agriband - Internet Access Setup")
    print("=" * 50)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        install_ngrok_instructions()
        return
    
    print("🚀 Starting Flask app...")
    
    # Start Flask app in background
    flask_process = subprocess.Popen([sys.executable, "app.py"])
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    print("🌐 Starting ngrok tunnel...")
    
    # Start ngrok
    ngrok_process = subprocess.Popen(["ngrok", "http", "5000"])
    
    # Wait for ngrok to start
    time.sleep(5)
    
    # Get the public URL
    public_url = get_ngrok_url()
    
    if public_url:
        print("✅ Success! Your app is now accessible from anywhere!")
        print(f"📱 Mobile URL: {public_url}")
        print(f"💻 Computer URL: {public_url}")
        print()
        print("🔗 Share this URL with anyone to access your app")
        print("⚠️  Note: This URL will change each time you restart ngrok")
        print()
        print("Press Ctrl+C to stop both Flask and ngrok")
        
        # Open in browser
        try:
            webbrowser.open(public_url)
        except:
            pass
    else:
        print("❌ Could not get ngrok URL. Please check ngrok status.")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        flask_process.terminate()
        ngrok_process.terminate()
        print("👋 All services stopped. Thank you for using KrishiMitra!")

if __name__ == "__main__":
    main()
