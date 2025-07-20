# Development Workflow Guide - Memory Bank Entry

## Overview

Essential workflow patterns and environment setup for mood-lighting project development. This guide ensures consistent development practices across all sessions.

## Virtual Environment Management

### **CRITICAL: Always Use Existing Virtual Environment**
```bash
# Check for existing venv first
ls -la venv/

# Activate existing venv (REQUIRED for all Python work)
source venv/bin/activate

# Verify correct environment
which python3  # Should show path with /venv/
pip list       # Should show project dependencies
```

**Never install packages globally** - this project has a configured virtual environment with all necessary dependencies.

### **Virtual Environment Contents**
- **esptool.py**: For ESP32 firmware flashing
- **requests**: For desktop LIFX API testing
- **pytest**: For running test suites
- **mpremote**: For MicroPython file management (when added)

## IDE Configuration & Usage

### **Primary Development Environment: VS Code + PyMakr**
```bash
# Open project in VS Code
code .

# Verify PyMakr extension is active
# Look for PyMakr panel in VS Code sidebar
```

**VS Code Workspace Features:**
- **Python Interpreter**: Set to virtual environment Python
- **PyMakr Integration**: ESP32 file upload/download via USB
- **Terminal Integration**: Auto-activates virtual environment
- **Code Formatting**: Black formatter configured

### **Backup Environment: Thonny IDE**
```bash
# Use Thonny for complex ESP32 debugging only
# Particularly useful for:
# - MicroPython REPL interaction
# - Real-time variable inspection
# - Step-by-step ESP32 debugging
```

## Platform Detection & Imports

### **Conditional Import Pattern**
The project uses conditional imports to support both desktop and ESP32 execution:

```python
# Standard pattern used throughout codebase
try:
    import urequests as requests  # MicroPython
    import ujson as json
    MICROPYTHON = True
except ImportError:
    import requests              # Desktop Python
    import json
    MICROPYTHON = False
```

**When to Use:**
- **Desktop Testing**: Uses `requests`, `json`, `unittest.mock`
- **ESP32 Deployment**: Uses `urequests`, `ujson`, `machine`, `network`

## Tool Prerequisites & Verification

### **Before ESP32 Work - Verify Tools**
```bash
# Activate virtual environment first
source venv/bin/activate

# Check essential tools
esptool.py version          # Should show v4.9.0+
python3 --version          # Should show Python 3.9+
pip show requests           # Should show installed version

# Check for MicroPython firmware
ls firmware/esp32-generic-v1.24.1.bin  # Should exist
```

### **Before Testing - Verify Test Setup**
```bash
# Run quick verification
pytest --version           # Should work without errors
pytest tests/ -v --dry-run # Should discover all tests

# Check imports work
python3 -c "from src.lighting.lifx_api import LIFXController"  # Should not error
```

## File Path Patterns

### **Import Paths for Different Contexts**
```python
# Desktop Python testing (from project root)
from src.lighting.lifx_api import LIFXController

# MicroPython on ESP32 (uploaded to device)
from lighting.lifx_api import LIFXController

# Test files (using sys.path)
sys.path.append('src')  # For desktop testing
from lighting.lifx_api import LIFXController
```

### **File Upload to ESP32**
```bash
# Main application files to upload:
# - src/main.py -> /main.py (ESP32 root)
# - src/lighting/ -> /lighting/ (ESP32 filesystem)
# - secrets.py -> /secrets.py (ESP32 root)
# - config files as needed
```

## Testing Workflow

### **Test Categories & When to Run**
```bash
# Unit tests (fast, no external dependencies)
pytest tests/test_main.py -v

# Integration tests (requires LIFX API)
pytest tests/integration/ -v -m integration

# Desktop Python tests
python3 tests/test_lighting/test_lifx_api.py

# MicroPython tests (run on ESP32)
# Upload test_lifx_api_micropython.py to ESP32 and execute
```

### **Pre-Deployment Testing**
```bash
# Always run before ESP32 deployment:
1. Activate venv: source venv/bin/activate
2. Run unit tests: pytest tests/test_main.py
3. Test LIFX API: python3 tests/test_lighting/test_lifx_api.py
4. Verify secrets.py exists and has valid credentials
```

## Common Development Commands

### **Quick Status Check**
```bash
# Project health check
source venv/bin/activate && \
python3 -c "from src.lighting.lifx_api import LIFXController; print('✅ Imports work')" && \
pytest tests/test_main.py -q && \
echo "✅ Project ready for development"
```

### **ESP32 Development Cycle**
```bash
# 1. Test logic on desktop first
python3 tests/test_lighting/test_lifx_api.py

# 2. Flash MicroPython firmware (once)
esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 firmware/esp32-generic-v1.24.1.bin

# 3. Upload application files
# (Use VS Code + PyMakr for file management)

# 4. Test on hardware
# (Use serial console for debugging)
```

## Key Principles

1. **Always activate virtual environment first**
2. **Test on desktop before ESP32 deployment**
3. **Use conditional imports for cross-platform compatibility** 
4. **Verify tools before hardware work**
5. **Keep secrets.py out of version control**

## Troubleshooting Quick Fixes

```bash
# Virtual environment not working
rm -rf venv/ && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Import errors
# Check if you're in project root and venv is activated

# ESP32 connection issues
# Try different USB cables, check /dev/ttyUSB* devices

# LIFX API failures  
# Verify secrets.py has valid LIFX_TOKEN
```

This workflow guide ensures consistent, productive development sessions regardless of session context or time gaps between development work.