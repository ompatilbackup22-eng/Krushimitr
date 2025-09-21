#!/usr/bin/env python3
"""
Script to run KrishiMitra app for mobile access
This script will show your IP address and run the app
"""

import socket
import subprocess
import sys
import os

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    print("🌱 KrishiMitra: Agriband - Mobile Access Setup")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    
    print(f"📱 To access from your mobile device:")
    print(f"   1. Make sure your mobile is connected to the same WiFi network")
    print(f"   2. Open your mobile browser")
    print(f"   3. Go to: http://{local_ip}:5000")
    print()
    print("🚀 Starting the application...")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the Flask app
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thank you for using KrishiMitra!")
    except Exception as e:
        print(f"❌ Error running the application: {e}")

if __name__ == "__main__":
    main()
