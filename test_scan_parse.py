#!/usr/bin/env python3
"""Regression check: nmcli -t escapes colons inside BSSID. Run: python3 test_scan_parse.py"""
import importlib.util, subprocess, types

spec = importlib.util.spec_from_file_location('wr', 'wifi_radar_linux.py')
wr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wr)

FAKE = "omar:0E\\:AC\\:8A\\:E6\\:2D\\:26:51\n:AA\\:BB\\:CC\\:DD\\:EE\\:FF:73\nbad:row\n"
wr.subprocess = types.SimpleNamespace(
    run=lambda *a, **k: types.SimpleNamespace(returncode=0, stdout=FAKE),
    TimeoutExpired=subprocess.TimeoutExpired,
)

aps = wr.WiFiRadarLinux.scan_wifi(None)
assert set(aps) == {'0E:AC:8A:E6:2D:26', 'AA:BB:CC:DD:EE:FF'}, aps
assert aps['0E:AC:8A:E6:2D:26'] == {'ssid': 'omar', 'bssid': '0E:AC:8A:E6:2D:26', 'signal': 51}
assert aps['AA:BB:CC:DD:EE:FF']['ssid'] == '(hidden)'   # empty SSID
print('OK — 2 APs, BSSIDs intact, malformed row skipped')
