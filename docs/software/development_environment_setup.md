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

**Primary Decision**: VS Code + PyMakr Extension  
**Backup Decision**: Thonny IDE v4.1.7  

**Why VS Code + PyMakr as Primary**:
- **Developer preference**: User already comfortable with VS Code/Cursor
- **Full IDE features**: IntelliSense, Git integration, extensions, code formatting
- **PyMakr extension**: Mature ESP32 support, automatic device detection
- **Professional workflow**: Maintains existing development muscle memory
- **File management**: Seamless sync between VS Code and ESP32

**Why Thonny as Backup**:
- **MicroPython-focused**: Built specifically for MicroPython development
- **Hardware debugging**: Superior for complex ESP32 troubleshooting
- **Zero configuration**: Works immediately without setup
- **Recovery tool**: When PyMakr has connection issues

**Primary Development Workflow**:
```
Write code in VS Code → PyMakr sync to ESP32 → Test via integrated REPL → Iterate
```

**Backup Workflow**:
```
Complex debugging in Thonny → File management → Hardware troubleshooting
```

**Alternative IDEs Considered**:
- MicroPico extension: Experimental ESP32 support, primarily for Raspberry Pi Pico
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
├── .vscode/                 # VS Code workspace configuration
│   ├── settings.json        # Python environment, PyMakr settings
│   └── extensions.json      # Recommended extensions
├── venv/                    # Virtual environment (git-ignored)
├── firmware/                # MicroPython firmware files
│   └── esp32-generic-v1.24.1.bin
├── pymakr.conf              # PyMakr project configuration
├── README_DEVELOPMENT.md    # Development setup guide
└── docs/software/           # Software documentation
    └── development_environment_setup.md
```

### Virtual Environment Contents
- **Python**: 3.9.6 (system Python in isolated environment)
- **esptool**: v4.9.0 (ESP32 flashing and communication)
- **Thonny**: v4.1.7 (backup MicroPython IDE)
- **Dependencies**: pyserial, cryptography, etc. (auto-installed)

### VS Code Configuration Details

**Workspace Settings** (`.vscode/settings.json`):
- **Python interpreter**: Auto-points to project virtual environment
- **PyMakr settings**: ESP32 auto-detection, 115200 baud rate, safe upload
- **File sync**: Only src/ directory uploaded to ESP32
- **Code quality**: Black formatting, pylint linting enabled
- **File exclusions**: Hide venv, firmware, git files from explorer

**Extension Recommendations** (`.vscode/extensions.json`):
- **PyMakr**: ESP32 communication and file management
- **Python support**: IntelliSense, debugging, formatting
- **Auto-install**: VS Code prompts to install recommended extensions

**PyMakr Project Config** (`pymakr.conf`):
- **Device connection**: Auto-detect ESP32 on /dev/tty.usbserial-*
- **File synchronization**: Upload .py, .json, .txt files from src/
- **Ignore patterns**: Exclude development files (.git, venv, docs, etc.)
- **Safety features**: Safe boot on upload, chunked file transfer

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

### Primary Code Development Cycle (VS Code + PyMakr)
1. **Edit**: Write Python code in VS Code with full IDE features
2. **Sync**: PyMakr uploads all src/ files to ESP32 automatically  
3. **Test**: Run code via integrated REPL in VS Code terminal
4. **Debug**: Monitor serial output and use LED feedback
5. **Iterate**: Seamless edit-sync-test cycle

### Backup Development Cycle (Thonny)
1. **Debug**: Complex hardware issues or PyMakr connection problems
2. **Upload**: Drag-and-drop individual files to ESP32
3. **Test**: Built-in REPL and detailed device management
4. **Recover**: Hardware troubleshooting and firmware issues

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
- **README_DEVELOPMENT.md**: Complete setup and usage instructions for both VS Code and Thonny workflows
- **VS Code configuration**: Workspace settings, extensions, and PyMakr setup documented
- **Troubleshooting**: Common issues and solutions for both development environments
- **Commands**: Copy-paste ready for immediate use
- **Verification**: Step-by-step testing procedures for both workflows

### Memory Bank Integration
- **Decision context**: Why VS Code + PyMakr was chosen as primary, Thonny as backup
- **Alternative analysis**: MicroPico vs PyMakr comparison, other IDE options considered  
- **Configuration rationale**: Detailed explanation of VS Code workspace settings
- **Future considerations**: Migration paths and optimization opportunities

## Next Steps Ready

### Immediate Next Steps (Hardware Arrival)
1. **Flash firmware**: 2-3 minute process using prepared tools
2. **Verify hardware**: Test built-in LED and WiFi connectivity
3. **LIFX API testing**: Validate API integration from ESP32
4. **Begin coding**: Start with WiFi manager implementation

### Development Readiness
- **Primary tools**: VS Code + PyMakr extension configured and ready
- **Backup tools**: Thonny IDE available for complex debugging
- **Documentation**: Complete setup guide for both workflows
- **Firmware**: Latest stable version downloaded and verified
- **Configuration**: VS Code workspace optimized for MicroPython ESP32 development
- **Prerequisites**: Node.js requirement documented for PyMakr installation

This development environment setup provides a solid foundation for rapid Phase 1 prototype development while maintaining professional development practices, user workflow preferences, and easy scalability to Phase 2 multi-button system.