# Development Environment Setup - Memory Bank Entry

## Setup Overview

**Date**: July 19, 2025  
**Phase**: Phase 1 - Development Environment Preparation  
**Status**: ✅ Complete and ready for hardware arrival  
**Tools Verified**: esptool.py, Thonny IDE, MicroPython firmware  

## Key Decisions and Rationale

### Python Virtual Environment Strategy

**Decision**: Use Python venv for project isolation  
**Implementation**: `python3 -m venv venv` in project root  
**Rationale**:
- Isolates project dependencies from system Python
- Prevents conflicts with other projects
- Easy to reproduce on different machines
- Standard Python practice for project development

**Benefits**:
- Clean dependency management
- No interference with system tools
- Easy environment recreation
- Professional development workflow

### MicroPython Firmware Selection

**Decision**: ESP32_GENERIC v1.24.1 (stable release)  
**Downloaded**: `firmware/esp32-generic-v1.24.1.bin` (1.6MB)  
**Release Date**: 2024-11-29 (latest stable)  

**Why This Firmware**:
- **ESP32_GENERIC**: Perfect match for DOIT ESP32 DevKit V1 hardware
- **Stable release**: Avoids nightly build bugs, production-ready
- **v1.24.1**: Latest stable with all required built-in libraries
- **Size optimization**: Includes urequests, ujson, asyncio, network modules

**Alternatives Considered**:
- ESP32_GENERIC_SPIRAM: Our board has standard SRAM, not SPIRAM
- ESP32_GENERIC_OTA: Larger size, OTA not needed for Phase 1
- Nightly builds: Too unstable for prototype development

### Development IDE Choice

**Decision**: Thonny IDE v4.1.7  
**Rationale**:
- **MicroPython-focused**: Built specifically for MicroPython development
- **Beginner-friendly**: Simple interface, excellent for learning
- **ESP32 integration**: Direct serial connection and file management
- **Real-time REPL**: Interactive Python shell on ESP32
- **File management**: Easy upload/download between computer and ESP32

**Development Workflow**:
```
Code in Thonny → Upload to ESP32 → Test via REPL → Iterate
```

**Alternative IDEs Considered**:
- VS Code: More complex setup, requires extensions
- PyCharm: Heavyweight, no direct MicroPython support
- Terminal + editor: Less integrated, harder debugging

### Flashing Tool Selection

**Decision**: esptool.py v4.9.0  
**Installation**: Via pip in virtual environment  
**Rationale**:
- **Official Espressif tool**: Standard for ESP32 development
- **Active maintenance**: Latest version with bug fixes
- **Cross-platform**: Works on macOS, Linux, Windows
- **Command-line interface**: Scriptable and reliable

**Capabilities**:
- Firmware flashing and erasing
- ESP32 chip identification
- Flash memory management
- Serial communication setup

## Technical Implementation Details

### Directory Structure Created
```
mood-lighting/
├── venv/                    # Virtual environment (git-ignored)
├── firmware/                # MicroPython firmware files
│   └── esp32-generic-v1.24.1.bin
├── README_DEVELOPMENT.md    # Development setup guide
└── docs/software/           # Software documentation
    └── development_environment_setup.md
```

### Virtual Environment Contents
- **Python**: 3.9.6 (system Python in isolated environment)
- **esptool**: v4.9.0 (ESP32 flashing and communication)
- **Thonny**: v4.1.7 (MicroPython IDE)
- **Dependencies**: pyserial, cryptography, etc. (auto-installed)

### Firmware Flash Process (Ready for Hardware)
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Erase existing firmware
esptool.py --port /dev/tty.usbserial-* erase_flash

# 3. Flash MicroPython
esptool.py --port /dev/tty.usbserial-* --baud 460800 write_flash -z 0x1000 firmware/esp32-generic-v1.24.1.bin
```

## Development Workflow Design

### Code Development Cycle
1. **Edit**: Write Python code in Thonny
2. **Upload**: Transfer files to ESP32 flash memory
3. **Test**: Run code via REPL, monitor serial output
4. **Debug**: Use print statements and LED feedback
5. **Iterate**: Modify and re-upload quickly

### File Organization Strategy
- **main.py**: Auto-runs on ESP32 boot
- **src/ modules**: Domain-based organization
- **config.json**: Configuration file on ESP32
- **secrets.py**: Credentials (not uploaded to git)

### Testing Approach
- **Hardware validation**: LED blink, WiFi connection tests
- **API integration**: HTTP requests to LIFX API
- **Component testing**: Individual module verification
- **Integration testing**: Complete button→light workflow

## Hardware Connection Preparation

### ESP32 Connection Process (When Hardware Arrives)
1. **Physical**: Connect ESP32 to computer via USB data cable
2. **Driver**: macOS auto-detects CP2102 USB-to-UART converter
3. **Port**: Device appears as `/dev/tty.usbserial-*` or `/dev/tty.SLAB_USBtoUART`
4. **Verification**: `esptool.py chip_id` confirms communication

### Development Hardware Requirements
- **USB Cable**: Data cable (not power-only) for ESP32 connection
- **Computer Port**: USB-A or USB-C with appropriate adapter
- **Power**: ESP32 powered via USB during development
- **Serial Console**: 115200 baud rate for debugging output

## Error Recovery Strategy

### Firmware Recovery Process
**Situation**: Wrong firmware flashed or ESP32 not responding  
**Solution**: Complete recovery always possible  
**Steps**:
```bash
# 1. Full erase (removes any firmware)
esptool.py --port /dev/tty.usbserial-* erase_flash

# 2. Re-flash correct firmware
esptool.py --port /dev/tty.usbserial-* write_flash 0x1000 firmware/esp32-generic-v1.24.1.bin
```

**Recovery Guarantee**: ESP32 bootloader in ROM cannot be corrupted, making recovery always possible as long as USB connection works.

## Performance Considerations

### MicroPython vs Arduino
**Decision**: MicroPython for rapid prototyping  
**Trade-offs**:
- **Advantages**: Faster development, easier debugging, Python ecosystem
- **Disadvantages**: Slightly slower execution, more memory usage
- **Project fit**: Perfect for Phase 1 prototype, can optimize later if needed

### Memory Management
- **Firmware size**: 1.6MB leaves ~2.4MB for code and data
- **RAM usage**: 520KB total, ~100-200KB available for application
- **Flash storage**: Sufficient for all Phase 1 code and configuration

## Documentation and Knowledge Transfer

### Development Guide Created
- **README_DEVELOPMENT.md**: Complete setup and usage instructions
- **Troubleshooting**: Common issues and solutions documented
- **Commands**: Copy-paste ready for immediate use
- **Verification**: Step-by-step testing procedures

### Memory Bank Integration
- **Decision context**: Why each tool was chosen
- **Alternative analysis**: What was considered and rejected
- **Future considerations**: Migration paths and optimization opportunities

## Next Steps Ready

### Immediate Next Steps (Hardware Arrival)
1. **Flash firmware**: 2-3 minute process using prepared tools
2. **Verify hardware**: Test built-in LED and WiFi connectivity
3. **LIFX API testing**: Validate API integration from ESP32
4. **Begin coding**: Start with WiFi manager implementation

### Development Readiness
- **Tools**: All development tools installed and tested
- **Documentation**: Complete setup guide for reproducibility
- **Firmware**: Latest stable version downloaded and verified
- **Workflow**: Clear development and debugging process established

This development environment setup provides a solid foundation for rapid Phase 1 prototype development while maintaining professional development practices and easy scalability to Phase 2 multi-button system.