# WiFi Manager Implementation Plan - Memory Bank Entry

## WiFi Manager Decision

**Date**: July 19, 2025  
**Decision**: Use official PyPI package - no custom implementation needed  
**Package**: `micropython-esp-wifi-manager` v1.8.0 by brainelectronics  
**Result**: WiFi connectivity handled by proven library, focus on button logic  

## Library Selection Rationale

### Why PyPI Package Over Custom Implementation

**Decision**: Use `micropython-esp-wifi-manager` from PyPI  
**Alternative Considered**: Custom implementation using MicroPython built-ins  

**Benefits of PyPI Package**:
- **✅ Professional grade**: Mature, tested codebase with edge case handling
- **✅ Standard approach**: Follows CLAUDE.md "well supported libraries" principle  
- **✅ Auto-reconnection**: Built-in 5-second timeout + fallback to AP mode
- **✅ Web interface**: Configuration at 192.168.4.1 when needed
- **✅ Encrypted storage**: Network credentials stored securely
- **✅ Zero dependencies**: Uses only MicroPython built-ins
- **✅ Maintained**: Active development and bug fixes
- **✅ Documentation**: Comprehensive usage examples

**Why Not Custom Implementation**:
- **⚠️ Reinventing wheel**: WiFi connection edge cases already solved
- **⚠️ Development time**: Focus should be on button→light logic
- **⚠️ Testing burden**: Need to handle reconnection, timeouts, AP fallback
- **⚠️ Maintenance**: We own all bugs and edge cases

## Package Details

### micropython-esp-wifi-manager Features

**Core Functionality**:
- **Auto-reconnection**: Tries to connect to saved networks on boot
- **Fallback AP mode**: Creates access point at 192.168.4.1 if no connection
- **Web configuration**: Simple interface to add/remove networks
- **Encrypted credentials**: JSON file with secure network storage
- **Timeout handling**: 5-second per-network connection timeout
- **Multi-network support**: Tries multiple saved networks in sequence

**Technical Specifications**:
- **Platform**: ESP32 + ESP8266 compatible
- **MicroPython**: Works with v1.19.1+ (our v1.24.1 is compatible)
- **Dependencies**: None (uses built-in network, picoweb modules)
- **Memory footprint**: Minimal impact on ESP32 resources
- **File structure**: Installs to `/lib` on ESP32 via mip/upip

### Installation Process

**Step 1: Flash MicroPython** (already prepared)
```bash
esptool.py --port /dev/tty.usbserial-* write_flash 0x1000 firmware/esp32-generic-v1.24.1.bin
```

**Step 2: Install WiFi Manager** (via ESP32 REPL)
```python
import upip
upip.install('micropython-esp-wifi-manager')
```

**Step 3: Basic Integration** (in our code)
```python
from wifi_manager import WiFiManager

# Initialize and connect
wm = WiFiManager()
wm.connect()  # Auto-connects to saved networks or creates AP
```

## Integration with Button Project

### Code Architecture Impact

**Original Plan** (custom implementation):
```
src/network/wifi_manager.py  # Custom implementation
├── connect()
├── reconnect()
├── check_connection()
└── handle_failure()
```

**Updated Plan** (PyPI package):
```
# No src/network/wifi_manager.py needed!
# Just use the installed library in main.py:

from wifi_manager import WiFiManager
wm = WiFiManager()
wm.connect()
```

### Simplified Implementation

**WiFi Functionality Handled by Library**:
- ✅ WiFi connection logic
- ✅ Auto-reconnection handling  
- ✅ Network failure detection
- ✅ Timeout management
- ✅ Credential storage
- ✅ AP fallback mode

**Our Implementation Focus**:
- ✅ Button input handling
- ✅ LIFX API integration
- ✅ LED feedback system
- ✅ Configuration management
- ✅ Main application logic

**Integration**: Just 3 lines in main.py:
```python
from wifi_manager import WiFiManager
wm = WiFiManager()
wm.connect()  # Everything else handled automatically
```

## Setup Workflow (When Hardware Arrives)

### Initial ESP32 Setup
1. **Flash MicroPython firmware** (2-3 minutes)
2. **Connect via REPL** (PyMakr or Thonny)
3. **Install WiFi manager**: `upip.install('micropython-esp-wifi-manager')`
4. **Test installation**: Import and verify library works

### Network Configuration  
1. **Boot ESP32** with WiFi manager installed
2. **Connect to AP**: Look for WiFi network (default: "WifiManager")
3. **Configure via web**: Go to 192.168.4.1, add home WiFi credentials
4. **Verify connection**: ESP32 should connect to home network automatically
5. **Test persistent**: Reboot ESP32, should auto-connect to saved network

### Development Integration
1. **Update main.py**: Add WiFi manager initialization
2. **Test connectivity**: Verify internet access for LIFX API calls
3. **Add error handling**: LED feedback if WiFi connection fails
4. **Configure button logic**: Implement button → LIFX API workflow

## Performance Considerations

### Startup Time
- **WiFi connection**: ~5 seconds maximum per saved network
- **Fallback to AP**: If no networks available, immediate AP creation
- **Boot to ready**: Expected 5-15 seconds total (acceptable for button device)

### Memory Usage
- **Library footprint**: Minimal (picoweb + connection logic)
- **Runtime overhead**: Only during connection phase
- **Steady state**: No background processes, minimal memory impact

### Error Recovery
- **Network drops**: Automatic reconnection attempts
- **Power cycles**: Auto-connect on boot to last working network
- **Configuration errors**: Web interface available for reconfiguration

## Documentation Updates Required

### Files to Update
- ✅ **README_DEVELOPMENT.md**: Add WiFi manager installation steps
- ⏳ **Memory bank**: Document library selection and integration approach
- ⏳ **Main implementation**: Update src/main.py to use WiFi manager
- ⏳ **Testing procedures**: Add network connectivity verification steps

### Future Considerations

**Phase 1**: Use WiFi manager as-is for reliable connectivity  
**Phase 2**: Potential customization if specific button requirements emerge  
**Phase 3**: Consider local network optimizations for sub-second response  

## Next Implementation Steps

### Immediate (No Hardware Required)
1. ✅ **Update documentation** with WiFi manager approach
2. ✅ **Update todo list** to remove custom WiFi implementation  
3. ⏳ **Design main.py structure** using WiFi manager library

### When Hardware Arrives
1. **Install and test** WiFi manager library
2. **Configure home network** via web interface
3. **Integrate with LIFX API** module
4. **Test complete connectivity** for button implementation

This approach significantly simplifies our implementation while providing a more robust and professionally tested WiFi management solution, allowing us to focus on the core button functionality that makes this project unique.