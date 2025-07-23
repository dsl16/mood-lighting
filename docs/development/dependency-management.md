# Dependency Management Learnings

## Overview

This document captures dependency management patterns and decisions from the ESP32 LIFX controller project, covering both the MicroPython and Arduino phases.

## MicroPython Dependency Strategy

### Virtual Environment Approach
```bash
# Project used isolated Python environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Key Dependencies
```python
# requirements.txt (MicroPython development)
requests>=2.25.0        # Desktop Python API testing
pytest>=7.0.0          # Testing framework
pytest-asyncio>=0.21.0 # Async test support
pytest-mock>=3.10.0    # Mocking capabilities
black>=23.0.0          # Code formatting
flake8>=6.0.0          # Linting
esptool>=4.5.0         # ESP32 firmware flashing
mpremote>=1.20.0       # MicroPython file transfer
```

### Conditional Import Pattern
```python
# Dual-platform compatibility
try:
    import urequests as requests  # MicroPython
    import ujson as json
    MICROPYTHON = True
except ImportError:
    import requests              # Desktop Python
    import json
    MICROPYTHON = False
```

### Benefits and Issues
**✅ Benefits:**
- Clean separation of development vs runtime dependencies
- Reproducible development environment
- Professional Python project structure

**❌ Issues:**
- Complex deployment to ESP32 (multiple files)
- MicroPython library limitations (SSL/HTTPS problems)
- Overhead of maintaining dual import paths

## Arduino Dependency Strategy

### Library Management
```cpp
// Arduino libraries (managed by Arduino IDE)
#include <WiFi.h>         // ESP32 built-in WiFi
#include <HTTPClient.h>   // ESP32 built-in HTTP client
#include <ArduinoJson.h>  // Installed via Library Manager
#include "secrets.h"      // Local configuration file
```

### Dependency Minimalism
- **Built-in Libraries**: WiFi and HTTPClient included with ESP32 core
- **Single External**: ArduinoJson for JSON parsing (widely used, stable)
- **No Package Manager**: Arduino IDE handles library installation
- **Local Configuration**: secrets.h for credentials (git-ignored)

### Benefits and Trade-offs
**✅ Benefits:**
- Minimal external dependencies
- Arduino IDE manages all library versioning
- Single-file deployment model
- No virtual environment complexity

**❌ Trade-offs:**
- Less sophisticated dependency tracking
- Library updates must be managed manually
- Limited to Arduino ecosystem libraries

## Dependency Lessons Learned

### 1. Platform-Specific Constraints Drive Strategy

**MicroPython Constraints:**
- Limited library ecosystem compared to desktop Python
- Memory constraints affect available libraries
- SSL/TLS implementation gaps in key libraries

**Arduino Constraints:**
- Library ecosystem focused on embedded applications  
- Manual library management through IDE
- Better hardware integration but less flexibility

### 2. Development vs Production Dependencies

**MicroPython Approach:**
```
Development: requests, pytest, black, flake8 (desktop Python)
Production: urequests, ujson, network (MicroPython built-ins)
```

**Arduino Approach:**
```
Development: Arduino IDE, Serial Monitor
Production: Same libraries (WiFi.h, HTTPClient.h, ArduinoJson.h)
```

**Insight**: Arduino's approach of using same libraries for development and production reduces complexity.

### 3. Security in Dependency Management

**MicroPython Approach:**
```python
# project_secrets.py (git-ignored)
WIFI_SSID = "network_name"
LIFX_TOKEN = "api_token"

# main.py
from project_secrets import WIFI_SSID, LIFX_TOKEN
```

**Arduino Approach:**
```cpp
// secrets.h (git-ignored)
const char* WIFI_SSID = "network_name";
const char* LIFX_TOKEN = "api_token";

// main.ino
#include "secrets.h"
```

**Common Pattern**: Both approaches used git-ignored configuration files with include/import mechanisms.

### 4. Deployment Complexity

**MicroPython Deployment:**
```bash
# Multiple files to deploy
mpremote cp src/main.py :
mpremote cp src/lighting/lifx_api.py :lighting/
mpremote cp src/network/wifi_manager.py :network/
mpremote cp project_secrets.py :
```

**Arduino Deployment:**
```
Arduino IDE Upload Button → Single .ino file + secrets.h
```

**Insight**: Arduino's single-file model significantly simplifies deployment.

## Recommendations for Future Projects

### For MicroPython Projects
1. **Use virtual environments** for development dependencies
2. **Plan for conditional imports** early in development
3. **Test library compatibility** with MicroPython before committing
4. **Consider deployment complexity** in architecture decisions
5. **Validate SSL/HTTPS libraries** thoroughly for production use

### For Arduino Projects  
1. **Minimize external dependencies** - prefer built-in libraries
2. **Use Arduino Library Manager** for version control
3. **Separate configuration files** for credentials (secrets.h pattern)
4. **Test library compatibility** across ESP32 board variations
5. **Document library versions** used for reproducibility

### For Platform Selection
```
Choose MicroPython when:
- Rapid prototyping and development speed is priority
- Complex data processing or algorithms required
- Team has strong Python expertise
- HTTP-only communication is sufficient

Choose Arduino when:
- Production reliability is critical
- HTTPS/SSL communication required
- Minimal dependencies preferred
- Single-file deployment is advantageous
- Hardware integration is primary focus
```

### Universal Best Practices
1. **Credential Separation**: Always use git-ignored configuration files
2. **Document Dependencies**: Maintain clear dependency lists and versions
3. **Test Early**: Validate critical libraries (especially networking) early
4. **Plan for Updates**: Consider library update and maintenance strategy
5. **Security First**: Audit dependencies for security vulnerabilities

## Development Environment Setup

### MicroPython Environment
```bash
# One-time setup
python -m venv venv
source venv/bin/activate
pip install esptool mpremote pytest requests

# Daily development
source venv/bin/activate
pytest tests/                    # Run tests
mpremote cp src/main.py :       # Deploy to ESP32
```

### Arduino Environment  
```
# One-time setup
1. Install Arduino IDE
2. Add ESP32 board support (espressif/arduino-esp32)
3. Install ArduinoJson library via Library Manager

# Daily development
1. Open .ino file in Arduino IDE
2. Click Upload button → Automatic compilation and deployment
```

**Insight**: Arduino's integrated development environment significantly reduces setup complexity compared to MicroPython's command-line tools.

## Conclusion

The dependency management evolution from MicroPython to Arduino reflects a broader trade-off between flexibility and simplicity:

- **MicroPython**: More flexible, professional Python tooling, but complex deployment
- **Arduino**: Simpler, integrated tooling, but less flexible dependency management

For embedded IoT projects requiring reliable HTTPS communication, Arduino's simpler dependency model combined with mature SSL libraries proved more effective than MicroPython's flexible but problematic approach.

The key insight is that **dependency strategy should be driven by production requirements rather than development preferences** - the most elegant development setup is worthless if the production deployment is unreliable.