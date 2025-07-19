# MicroPython Development Environment Setup

## Environment Overview

**Status**: ✅ Ready for ESP32 development  
**MicroPython Firmware**: v1.24.1 (stable, downloaded)  
**Development Tools**: Thonny IDE + esptool.py configured  
**Virtual Environment**: Isolated project dependencies  

## Quick Start Commands

### Activate Development Environment

#### Primary Workflow: VS Code + PyMakr
```bash
# Navigate to project directory
cd /Users/darrinlim/Documents/mood-lighting

# Open project in VS Code (will auto-activate virtual environment)
code .

# Install PyMakr extension if not already installed:
# 1. Open Extensions (⌘+Shift+X)  
# 2. Search "PyMakr"
# 3. Install "PyMakr" by Pycom
# 4. Restart VS Code
```

#### Backup Workflow: Thonny IDE
```bash
# For complex ESP32 debugging when needed
source venv/bin/activate
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

### Primary Workflow: VS Code + PyMakr

#### 1. Code Development
- **Editor**: VS Code with PyMakr extension  
- **Features**: Full VS Code functionality (IntelliSense, Git, extensions)
- **File Structure**: Domain-based organization in src/
- **Auto-completion**: MicroPython libraries and ESP32-specific modules

#### 2. ESP32 Connection & File Management
```bash
# PyMakr will automatically detect ESP32 when connected
# 1. Connect ESP32 via USB
# 2. Open PyMakr panel in VS Code
# 3. Click "Connect Device" 
# 4. Select ESP32 port (usually auto-detected)
```

#### 3. Code Deployment
- **Method**: PyMakr sync - uploads all src/ files to ESP32
- **Command**: Use PyMakr "Upload" button or Ctrl+Shift+P → "PyMakr: Upload"
- **Files synced**: All .py files in src/ directory
- **Config**: Automatic upload of config.json and secrets.py

#### 4. Development & Debugging  
- **REPL Access**: PyMakr provides integrated REPL in VS Code terminal
- **Serial Monitor**: Real-time ESP32 output in VS Code
- **File Management**: Download/upload individual files via PyMakr
- **Error Handling**: Immediate LED feedback per CLAUDE.md specs

### Backup Workflow: Thonny IDE

#### When to Use Thonny
- **Firmware flashing issues**: Better hardware-level debugging
- **Complex device management**: More detailed ESP32 control
- **PyMakr connection problems**: Alternative communication method
- **Hardware troubleshooting**: Step-by-step device diagnosis

#### Thonny Workflow
- **File Management**: Drag-and-drop upload to ESP32
- **REPL**: Built-in interactive shell
- **Debugging**: Step-through code execution on ESP32

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