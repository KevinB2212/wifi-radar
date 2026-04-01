# 📡 WiFi Radar - Motion Detection

**Visual motion detection using WiFi signal analysis**

![WiFi Radar Demo](https://img.shields.io/badge/status-demo-yellow)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![macOS](https://img.shields.io/badge/platform-macOS-lightgrey)

---

## 🌐 [Live Demo](https://kevinb2212.github.io/wifi-radar/)

**Note:** The web version is a simulated demo. The real app scans actual WiFi networks and requires Python + macOS.

---

## 🎯 What Is This?

WiFi Radar detects motion by monitoring signal strength fluctuations across multiple WiFi access points. When you move around, your body blocks/reflects WiFi signals, causing detectable changes that the radar picks up.

### How It Works

1. **Baseline Phase** (40 seconds) - Records normal signal patterns
2. **Monitoring Phase** - Continuously scans WiFi networks every 2 seconds
3. **Detection** - Flags motion when multiple APs show unusual fluctuations
4. **Visualization** - Real-time radar display with sweeping animation

---

## 🖥️ The Real Version (Python)

### Requirements

- **macOS** (uses `airport` command-line utility)
- **Python 3.7+**
- **Tkinter** (built into Python)

### Quick Start

```bash
# Clone this repo
git clone https://github.com/KevinB2212/wifi-radar.git
cd wifi-radar

# Run the radar UI
python3 wifi_radar_ui.py

# Or use the launcher (auto-installs dependencies)
bash launch_radar.sh
```

### Features

✅ **Visual Radar Display** - Circular radar with sweeping line animation  
✅ **Real-time Detection** - Live WiFi scanning and motion alerts  
✅ **Activity Log** - Timestamped event history  
✅ **Statistics Dashboard** - Scan count, AP count, alert tracking  
✅ **Smooth Animation** - 20 FPS with fade trail effects  

---

## 📊 What You'll See

### Radar Interface

```
     ╱────────╲
   ╱  -40dBm  ╲
  │     •     │  🟢 Normal AP
  │   • •🔴  │  🔴 Motion detected
  │  •  •  • │
   ╲    •   ╱
     ╲──────╱
```

- **Green dots** = WiFi access points (normal)
- **Red pulsing dots** = APs detecting motion
- **Rotating sweep line** = Radar animation
- **Concentric circles** = Signal strength zones

### When Motion Is Detected

1. Status banner flashes **"⚠️ MOTION DETECTED"**
2. Affected APs turn red and pulse
3. Activity log updates with timestamp
4. Alert counter increments

---

## 🛠️ Technical Details

### Python Version (Desktop App)

| Component | Technology |
|-----------|-----------|
| **WiFi Scanning** | macOS `airport` command |
| **GUI Framework** | Tkinter |
| **Animation** | Custom canvas rendering (20 FPS) |
| **Threading** | Background scanner + foreground UI |
| **Memory Usage** | ~35 MB |
| **CPU Usage** | 5-10% when active |

### Web Version (Demo)

| Component | Technology |
|-----------|-----------|
| **Frontend** | Vanilla JavaScript + HTML5 Canvas |
| **Animation** | RequestAnimationFrame |
| **Simulation** | Random motion events + fake AP data |
| **Hosting** | GitHub Pages |

---

## 📁 Files

```
wifi-radar/
├── wifi_radar.py           # Terminal version (text-based)
├── wifi_radar_ui.py        # GUI version (radar display) ⭐
├── launch_radar.sh         # Quick launcher script
├── setup.sh                # Dependency installer
├── wifi_radar_README.md    # Full documentation
└── DEMO.md                 # UI walkthrough
```

---

## 🚀 Usage

### Terminal Version

```bash
python3 wifi_radar.py
```

Simple text-based output:

```
[12:34:56] Scan #42: 12 APs detected
[12:35:02] ⚠️  MOTION DETECTED - 3 APs affected
[12:35:08] Scan #43: 12 APs detected
```

### Radar UI Version

```bash
python3 wifi_radar_ui.py
```

Full graphical interface with:
- Animated radar display
- Real-time statistics
- Visual motion alerts
- Activity log panel

---

## 🎓 How Motion Detection Works

### Signal Analysis

1. **Multiple APs Required** - Uses 3+ access points for triangulation
2. **Deviation Threshold** - Detects fluctuations >5 dB from baseline
3. **Time Window** - Requires sustained changes over multiple scans
4. **False Positive Reduction** - Ignores single-AP anomalies

### Limitations

- **macOS Only** - Relies on `airport` utility
- **Indoor Use** - Works best with multiple WiFi networks
- **Not Perfect** - Can miss slow/small movements
- **Baseline Drift** - Needs recalibration over time

---

## 🔮 Future Ideas

- [ ] Linux support (via `iwlist` or `nmcli`)
- [ ] Windows support (via `netsh`)
- [ ] Heatmap visualization
- [ ] Multi-room tracking
- [ ] Alert notifications (email/SMS)
- [ ] Historical data export

---

## 🤝 Contributing

This is a personal project, but feel free to fork it and experiment! Pull requests welcome.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👨‍💻 Author

**Kevin Brennan**  
CS Student @ DCU | Product Support Engineer @ Telnyx

- GitHub: [@KevinB2212](https://github.com/KevinB2212)
- Portfolio: [KevinB2212.github.io](https://kevinb2212.github.io)

---

## 🙏 Acknowledgments

Inspired by the concept of passive WiFi sensing research:
- [WiSee (University of Washington)](https://wisee.cs.washington.edu/)
- [WiFi CSI-based sensing papers](https://scholar.google.com/scholar?q=wifi+csi+motion+detection)

This project is a simplified demonstration using consumer hardware.
