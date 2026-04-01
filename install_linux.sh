#!/bin/bash
# WiFi Radar - Linux Installation Script

set -e

echo "📡 WiFi Radar - Linux Setup"
echo "==========================="
echo

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "❌ Could not detect Linux distribution"
    exit 1
fi

echo "Detected distribution: $DISTRO"
echo

# Install dependencies based on distro
case $DISTRO in
    ubuntu|debian|pop|linuxmint)
        echo "📦 Installing dependencies (Ubuntu/Debian)..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-tk network-manager
        ;;
    
    fedora|rhel|centos)
        echo "📦 Installing dependencies (Fedora/RHEL)..."
        sudo dnf install -y python3 python3-tkinter NetworkManager
        ;;
    
    arch|manjaro)
        echo "📦 Installing dependencies (Arch)..."
        sudo pacman -Sy --noconfirm python python-tkinter networkmanager
        ;;
    
    opensuse*)
        echo "📦 Installing dependencies (openSUSE)..."
        sudo zypper install -y python3 python3-tk NetworkManager
        ;;
    
    *)
        echo "⚠️  Unsupported distribution: $DISTRO"
        echo "Please install manually:"
        echo "  - Python 3.7+"
        echo "  - python3-tk (tkinter)"
        echo "  - NetworkManager (nmcli) OR wireless-tools (iwlist)"
        exit 1
        ;;
esac

echo
echo "✅ Dependencies installed!"
echo

# Check if NetworkManager is running
if systemctl is-active --quiet NetworkManager; then
    echo "✅ NetworkManager is running"
    WIFI_METHOD="nmcli"
else
    echo "⚠️  NetworkManager not running. Will try iwlist (requires sudo)."
    WIFI_METHOD="iwlist"
    
    # Check if iwlist is available
    if ! command -v iwlist &> /dev/null; then
        echo "❌ iwlist not found. Installing wireless-tools..."
        case $DISTRO in
            ubuntu|debian|pop|linuxmint)
                sudo apt-get install -y wireless-tools
                ;;
            fedora|rhel|centos)
                sudo dnf install -y wireless-tools
                ;;
            arch|manjaro)
                sudo pacman -S --noconfirm wireless_tools
                ;;
            opensuse*)
                sudo zypper install -y wireless-tools
                ;;
        esac
    fi
fi

echo

# Make script executable
chmod +x wifi_radar_linux.py

echo "🚀 Installation complete!"
echo
echo "To run WiFi Radar:"
if [ "$WIFI_METHOD" = "iwlist" ]; then
    echo "  sudo python3 wifi_radar_linux.py"
    echo
    echo "⚠️  Note: iwlist requires root permissions"
else
    echo "  python3 wifi_radar_linux.py"
fi
echo
echo "🎯 Quick test:"
if [ "$WIFI_METHOD" = "iwlist" ]; then
    echo "  sudo iwlist scanning | head -20"
else
    echo "  nmcli dev wifi"
fi
echo
