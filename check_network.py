#!/usr/bin/env python3
"""
Network checker for KrishiMitra mobile access
"""

import socket
import subprocess
import platform

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_network_info():
    """Get network information"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            return result.stdout
        else:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            return result.stdout
    except:
        return "Could not get network info"

def main():
    print("🔍 KrishiMitra Network Checker")
    print("=" * 40)
    
    local_ip = get_local_ip()
    
    print(f"💻 Your computer's IP: {local_ip}")
    print()
    
    if local_ip == "127.0.0.1":
        print("❌ You're not connected to a network!")
        print("   Please connect to WiFi or Ethernet")
    else:
        print("✅ You're connected to a network")
        print(f"📱 Mobile access URL: http://{local_ip}:5000")
        print()
        print("📋 Instructions for mobile access:")
        print("   1. Connect your mobile to the SAME WiFi network")
        print("   2. Open mobile browser")
        print(f"   3. Go to: http://{local_ip}:5000")
        print()
        print("🔧 If mobile can't connect:")
        print("   - Check Windows Firewall settings")
        print("   - Make sure both devices are on same network")
        print("   - Try restarting your router")
    
    print()
    print("🌐 Network Details:")
    print("-" * 20)
    network_info = get_network_info()
    print(network_info[:500] + "..." if len(network_info) > 500 else network_info)

if __name__ == "__main__":
    main()
