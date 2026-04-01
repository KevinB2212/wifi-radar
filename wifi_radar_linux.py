#!/usr/bin/env python3
"""
WiFi Radar - Linux Version
Motion detection via WiFi signal analysis
"""

import subprocess
import time
import re
from collections import defaultdict
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import threading
import math

class WiFiRadarLinux:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WiFi Radar - Motion Detection")
        self.root.geometry("900x1000")
        self.root.configure(bg='#1a1a2e')
        
        # State
        self.monitoring = False
        self.baseline = {}
        self.scan_count = 0
        self.alert_count = 0
        self.baseline_scans = 20  # 40 seconds at 2s intervals
        self.scan_history = defaultdict(list)
        self.alert_aps = set()
        
        # UI Setup
        self.setup_ui()
        
        # Animation
        self.angle = 0
        self.animate()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#1a1a2e')
        header.pack(pady=20)
        
        title = tk.Label(header, text="📡 WiFi Radar", font=('Arial', 32, 'bold'),
                        fg='#00ff88', bg='#1a1a2e')
        title.pack()
        
        subtitle = tk.Label(header, text="Motion Detection (Linux)", font=('Arial', 12),
                           fg='#888', bg='#1a1a2e')
        subtitle.pack()
        
        # Radar Canvas
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='#0a0a1a',
                               highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="READY", font=('Arial', 16, 'bold'),
                                    fg='#00ff88', bg='#1a1a2e')
        self.status_label.pack(pady=10)
        
        # Controls
        controls = tk.Frame(self.root, bg='#1a1a2e')
        controls.pack(pady=10)
        
        self.start_btn = tk.Button(controls, text="START MONITORING",
                                   command=self.start_monitoring,
                                   font=('Arial', 12, 'bold'),
                                   bg='#00ff88', fg='#1a1a2e',
                                   padx=30, pady=10, cursor='hand2')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(controls, text="STOP MONITORING",
                                 command=self.stop_monitoring,
                                 font=('Arial', 12, 'bold'),
                                 bg='#ff4444', fg='white',
                                 padx=30, pady=10, cursor='hand2',
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats
        stats = tk.Frame(self.root, bg='#16213e')
        stats.pack(pady=10, padx=20, fill=tk.X)
        
        stats_inner = tk.Frame(stats, bg='#16213e')
        stats_inner.pack(pady=10)
        
        self.scan_label = self.create_stat(stats_inner, "Scans", "0")
        self.scan_label.pack(side=tk.LEFT, padx=20)
        
        self.ap_label = self.create_stat(stats_inner, "Access Points", "0")
        self.ap_label.pack(side=tk.LEFT, padx=20)
        
        self.alert_label = self.create_stat(stats_inner, "Alerts", "0")
        self.alert_label.pack(side=tk.LEFT, padx=20)
        
        # Activity Log
        log_frame = tk.Frame(self.root, bg='#16213e')
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        log_title = tk.Label(log_frame, text="Activity Log", font=('Arial', 14, 'bold'),
                            fg='#00ff88', bg='#16213e')
        log_title.pack(pady=5)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, bg='#0a0a1a', fg='#00ff88',
                               font=('Courier', 10), yscrollcommand=log_scroll.set)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
    def create_stat(self, parent, label, value):
        frame = tk.Frame(parent, bg='#16213e')
        
        lbl = tk.Label(frame, text=label, font=('Arial', 10),
                      fg='#888', bg='#16213e')
        lbl.pack()
        
        val = tk.Label(frame, text=value, font=('Arial', 20, 'bold'),
                      fg='#00ff88', bg='#16213e')
        val.pack()
        
        frame.value_label = val
        return frame
        
    def log(self, message, level='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        prefix = '⚠️' if level == 'warning' else 'ℹ️'
        
        self.log_text.insert('1.0', f'[{timestamp}] {prefix} {message}\n')
        self.log_text.see('1.0')
        
    def scan_wifi(self):
        """Scan WiFi networks using nmcli or iwlist"""
        aps = {}
        
        # Try nmcli first (NetworkManager)
        try:
            result = subprocess.run(['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL', 'dev', 'wifi'],
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            ssid = parts[0] or '(hidden)'
                            bssid = parts[1]
                            signal = int(parts[2])
                            aps[bssid] = {
                                'ssid': ssid,
                                'bssid': bssid,
                                'signal': signal
                            }
                return aps
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        # Fallback to iwlist
        try:
            result = subprocess.run(['sudo', 'iwlist', 'scanning'],
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                current_ap = {}
                for line in result.stdout.split('\n'):
                    if 'Address:' in line:
                        if current_ap:
                            aps[current_ap['bssid']] = current_ap
                        bssid = line.split('Address: ')[1].strip()
                        current_ap = {'bssid': bssid, 'ssid': '(hidden)', 'signal': -100}
                    elif 'ESSID:' in line:
                        ssid = line.split('ESSID:')[1].strip('"')
                        current_ap['ssid'] = ssid or '(hidden)'
                    elif 'Signal level=' in line:
                        signal = int(re.search(r'-?\d+', line.split('Signal level=')[1]).group())
                        current_ap['signal'] = signal
                
                if current_ap:
                    aps[current_ap['bssid']] = current_ap
                    
                return aps
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        return {}
        
    def start_monitoring(self):
        if self.monitoring:
            return
            
        self.monitoring = True
        self.baseline = {}
        self.scan_count = 0
        self.alert_count = 0
        self.scan_history.clear()
        self.alert_aps.clear()
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.status_label.config(text="WARMING UP...", fg='#ffc107')
        self.log("Started monitoring. Building baseline...")
        
        # Start scanning thread
        self.scan_thread = threading.Thread(target=self.scan_loop, daemon=True)
        self.scan_thread.start()
        
    def stop_monitoring(self):
        self.monitoring = False
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.status_label.config(text="STOPPED", fg='#888')
        self.log("Monitoring stopped.")
        self.alert_aps.clear()
        
    def scan_loop(self):
        while self.monitoring:
            aps = self.scan_wifi()
            
            if not aps:
                self.log("Failed to scan WiFi. Check permissions (may need sudo).", 'warning')
                time.sleep(2)
                continue
                
            self.scan_count += 1
            
            # Update stats
            self.root.after(0, self.update_stats, len(aps))
            
            # Build baseline
            if self.scan_count <= self.baseline_scans:
                for bssid, ap in aps.items():
                    if bssid not in self.scan_history:
                        self.scan_history[bssid] = []
                    self.scan_history[bssid].append(ap['signal'])
                    
                progress = int((self.scan_count / self.baseline_scans) * 100)
                self.root.after(0, lambda p=progress: 
                              self.status_label.config(text=f"WARMING UP... {p}%"))
                
                if self.scan_count == self.baseline_scans:
                    # Calculate baseline
                    for bssid, signals in self.scan_history.items():
                        avg = sum(signals) / len(signals)
                        self.baseline[bssid] = avg
                    
                    self.root.after(0, lambda: 
                                  self.status_label.config(text="MONITORING", fg='#00ff88'))
                    self.log(f"Baseline established. Tracking {len(self.baseline)} APs.")
                    
            else:
                # Detect motion
                motion_detected = False
                affected_aps = []
                
                for bssid, ap in aps.items():
                    if bssid in self.baseline:
                        deviation = abs(ap['signal'] - self.baseline[bssid])
                        
                        if deviation > 5:  # 5 dBm threshold
                            motion_detected = True
                            affected_aps.append(ap['ssid'])
                            self.alert_aps.add(bssid)
                        elif bssid in self.alert_aps:
                            # Decay alert
                            self.alert_aps.discard(bssid)
                
                if motion_detected and len(affected_aps) >= 2:
                    self.alert_count += 1
                    self.root.after(0, lambda: 
                                  self.status_label.config(text="⚠️ MOTION DETECTED", fg='#ff4444'))
                    self.log(f"Motion detected! Affected: {', '.join(set(affected_aps))}", 'warning')
                    
                    # Reset status after 2 seconds
                    self.root.after(2000, lambda: 
                                  self.status_label.config(text="MONITORING", fg='#00ff88') 
                                  if self.monitoring else None)
            
            time.sleep(2)
            
    def update_stats(self, ap_count):
        self.scan_label.value_label.config(text=str(self.scan_count))
        self.ap_label.value_label.config(text=str(ap_count))
        self.alert_label.value_label.config(text=str(self.alert_count))
        
    def animate(self):
        self.draw_radar()
        self.angle += 0.02
        self.root.after(50, self.animate)  # 20 FPS
        
    def draw_radar(self):
        self.canvas.delete('all')
        
        cx, cy = 250, 250
        radius = 200
        
        # Background circles
        for i in range(1, 5):
            r = (radius / 4) * i
            alpha = int(25 + (i * 10))
            color = f'#{alpha:02x}ff{alpha:02x}'
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=1)
            
        # Crosshair
        self.canvas.create_line(cx-radius, cy, cx+radius, cy, fill='#006644', width=1)
        self.canvas.create_line(cx, cy-radius, cx, cy+radius, fill='#006644', width=1)
        
        # Sweep line
        if self.monitoring:
            x = cx + radius * math.cos(self.angle)
            y = cy + radius * math.sin(self.angle)
            self.canvas.create_line(cx, cy, x, y, fill='#00ff88', width=2)
            
        # Zone labels
        labels = ['-30dBm', '-45dBm', '-60dBm', '-75dBm']
        for i, label in enumerate(labels):
            r = (radius / 4) * (i + 1)
            self.canvas.create_text(cx, cy - r - 10, text=label, fill='#00aa66', font=('Courier', 10))
            
        # Access points
        for i, bssid in enumerate(self.scan_history.keys()):
            angle = (2 * math.pi / max(len(self.scan_history), 1)) * i
            distance = 0.5 + (hash(bssid) % 50) / 100  # Pseudo-random distance
            
            x = cx + radius * distance * math.cos(angle)
            y = cy + radius * distance * math.sin(angle)
            
            color = '#ff4444' if bssid in self.alert_aps else '#00ff88'
            size = 8 if bssid in self.alert_aps else 6
            
            self.canvas.create_oval(x-size, y-size, x+size, y+size, fill=color, outline='')
            
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    print("WiFi Radar - Linux Version")
    print("===========================")
    print()
    print("Requirements:")
    print("  - NetworkManager (nmcli) OR wireless-tools (iwlist)")
    print("  - Python 3.7+")
    print("  - tkinter (python3-tk)")
    print()
    print("If using iwlist, you may need to run with sudo:")
    print("  sudo python3 wifi_radar_linux.py")
    print()
    
    radar = WiFiRadarLinux()
    radar.run()
