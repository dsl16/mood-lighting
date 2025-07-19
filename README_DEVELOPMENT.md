# MicroPython Development Environment Setup

## Environment Overview

**Status**: ✅ Ready for ESP32 development  
**MicroPython Firmware**: v1.24.1 (stable, downloaded)  
**Development Tools**: Thonny IDE + esptool.py configured  
**Virtual Environment**: Isolated project dependencies  

## Quick Start Commands

### Activate Development Environment
```bash
# Navigate to project directory
cd /Users/darrinlim/Documents/mood-lighting

# Activate virtual environment
source venv/bin/activate

# Launch Thonny IDE for MicroPython development
thonny
```

### Flash MicroPython Firmware (When Hardware Arrives)
```bash
# Connect ESP32 via USB, then run:
source venv/bin/activate

# 1. Erase existing firmware
esptool.py --port /dev/tty.usbserial-* erase_flash

# 2. Flash MicroPython firmware
esptool.py --port /dev/tty.usbserial-* --baud 460800 write_flash -z 0x1000 firmware/esp32-generic-v1.24.1.bin

# Note: Replace /dev/tty.usbserial-* with actual port (will be shown when ESP32 connects)
```

### Connect to ESP32 Serial Console
```bash
# Option 1: Using Thonny (Recommended)
# 1. Open Thonny
# 2. Tools → Options → Interpreter
# 3. Select "MicroPython (ESP32)"
# 4. Select correct port

# Option 2: Using screen command
screen /dev/tty.usbserial-* 115200
```

## Development Workflow

### 1. Code Development
- **Editor**: Thonny IDE with MicroPython support
- **File Structure**: Domain-based organization in src/
- **Testing**: Serial console + REPL for immediate feedback

### 2. Code Deployment
- **Method**: Thonny file upload to ESP32 flash memory
- **Files**: main.py (auto-runs on boot) + modules in src/
- **Config**: Upload config.json and secrets.py to ESP32

### 3. Debugging
- **Serial Monitor**: Real-time output via USB connection
- **REPL**: Interactive Python shell on ESP32
- **Error Handling**: Immediate LED feedback per CLAUDE.md specs

## Installed Tools

### Core Development Tools
- **Python**: 3.9.6 (system Python)
- **Virtual Environment**: `venv/` (project-isolated)
- **esptool.py**: v4.9.0 (ESP32 flashing and communication)
- **Thonny**: v4.1.7 (MicroPython-focused IDE)

### MicroPython Firmware
- **Version**: v1.24.1 (2024-11-29 stable release)
- **Target**: ESP32_GENERIC (for our DOIT ESP32 DevKit V1)
- **File**: `firmware/esp32-generic-v1.24.1.bin` (1.6MB)
- **Features**: WiFi, Bluetooth, urequests, ujson, asyncio built-in

## Hardware Connection Guide

### ESP32 DevKit V1 Connection
1. **Connect**: ESP32 to computer via USB cable (data cable, not power-only)
2. **Drivers**: macOS should auto-detect CP2102 USB-to-UART (no manual drivers needed)
3. **Port Detection**: Check `/dev/tty.usbserial-*` or `/dev/tty.SLAB_USBtoUART`
4. **Verification**: `ls /dev/tty.*` should show ESP32 device when connected

### First Connection Test
```bash
# Check if ESP32 is detected
ls /dev/tty.*

# Test communication with ESP32 (before MicroPython flash)
esptool.py --port /dev/tty.usbserial-* chip_id
```

## Troubleshooting

### Common Issues
- **Port not found**: Try different USB cable (needs data lines)
- **Permission denied**: Run `sudo chmod 666 /dev/tty.usbserial-*`
- **Flash fails**: Hold BOOT button during flashing, release after start
- **No response**: Press EN (reset) button after successful flash

### Recovery Process
If firmware flash goes wrong (very unlikely):
```bash
# Full recovery - erases everything and starts fresh
esptool.py --port /dev/tty.usbserial-* erase_flash
esptool.py --port /dev/tty.usbserial-* write_flash 0x1000 firmware/esp32-generic-v1.24.1.bin
```

## Development Environment Verification

Once ESP32 hardware arrives, verify setup:

### 1. Hardware Test
```python
# In Thonny MicroPython REPL:
import machine
led = machine.Pin(2, machine.Pin.OUT)
led.on()   # Built-in LED should turn on
led.off()  # Built-in LED should turn off
```

### 2. WiFi Test
```python
# In Thonny MicroPython REPL:
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()  # Should show available WiFi networks
```

### 3. HTTP Test (for LIFX API validation)
```python
# In Thonny MicroPython REPL (after WiFi connection):
import urequests
response = urequests.get('http://httpbin.org/get')
print(response.text)  # Should show successful HTTP response
```

## Next Steps

1. **Hardware Arrival**: Flash firmware and test basic functionality
2. **WiFi Configuration**: Connect ESP32 to home network
3. **LIFX API Testing**: Validate API calls from ESP32
4. **Button Integration**: Wire button and test input handling
5. **LED Feedback**: Connect status LEDs and test feedback system

All tools are ready for immediate development when ESP32 hardware arrives!