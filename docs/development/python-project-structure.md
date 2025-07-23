# Python Project Structure Learnings

## Overview

This document captures the Python project structure patterns we developed during the MicroPython phase of the ESP32 LIFX controller project. While we ultimately switched to Arduino for technical reasons, the architectural patterns here are valuable for future Python/MicroPython projects.

## Project Layout

### Chosen Structure: `src/` Layout
```
src/
├── __init__.py
├── main.py                    # Application orchestration
├── config/
│   └── __init__.py
├── hardware/                  # GPIO and button handling
│   └── __init__.py
├── lighting/                  # LIFX API integration
│   ├── __init__.py
│   └── lifx_api.py
└── network/                   # WiFi management
    └── __init__.py
```

### Benefits of This Structure

1. **Clear Separation of Concerns**
   - `hardware/`: GPIO pins, button debouncing, LED control
   - `lighting/`: LIFX API calls, state management
   - `network/`: WiFi connection, reconnection logic
   - `config/`: Configuration file management

2. **Testability**
   - Each module can be tested independently
   - Clean interfaces between modules
   - Easy to mock network and hardware components

3. **Scalability**
   - Easy to add new light protocols
   - Simple to extend hardware support
   - Clear place for new features

### Alternative Structures Considered

#### Single File Approach
```
main.py  # Everything in one file
```
- **Pros**: Simple for prototypes, easy deployment to ESP32
- **Cons**: Hard to test, difficult to maintain, poor separation

#### Domain-Driven Structure  
```
src/
├── lights/
├── buttons/
└── network/
```
- **Pros**: Business logic focused
- **Cons**: Too complex for embedded project scope

## Key Design Patterns

### 1. Configuration Management
```python
# Clean separation of config from code
from project_secrets import WIFI_SSID, WIFI_PASSWORD, LIFX_TOKEN
```

### 2. Module Organization
```python
# Each module has clear responsibility
# lighting/lifx_api.py - handles all LIFX communication
# hardware/button.py - handles physical button input
# network/wifi.py - handles connectivity
```

### 3. Error Handling Patterns
```python
# Fail-fast with clear error messages
try:
    response = self.make_api_request('GET', url)
except Exception as e:
    print(f"❌ API request failed: {e}")
    raise
```

## Module Interface Design

### Clean Abstractions
```python
# lighting/lifx_api.py
class LIFXController:
    async def toggle_light(self, light_name):
        """Toggle light state using stateless approach"""
        current_state = await self.get_light_state(light_name)
        new_state = 'off' if current_state['power'] == 'on' else 'on'
        return await self.set_light_state(light_name, new_state)
```

### Async/Await Pattern
```python
# Non-blocking operations for responsive UI
async def handle_button_press(self):
    try:
        await self.toggle_light(DEFAULT_LIGHT)
        self.blink_success_led()
    except Exception as e:
        self.show_error_led()
```

## Lessons Learned

### What Worked Well
- **Domain separation**: Clear boundaries between hardware, network, and lighting
- **Async patterns**: Non-blocking operations for sub-second response
- **Configuration separation**: Clean secrets management
- **Error handling**: Fail-fast with LED feedback

### What Could Improve
- **Type hints**: Would benefit from proper typing for better IDE support
- **Interface definitions**: Could use ABC for clearer contracts
- **Dependency injection**: Hardcoded dependencies made testing harder

### MicroPython Considerations
- **Import limitations**: Some Python patterns don't work on MicroPython
- **Memory constraints**: Had to be careful with object creation
- **Library differences**: `ujson` vs `json`, `urequests` vs `requests`

## Reusable Patterns

### 1. Embedded Project Structure
```
src/
├── hardware/     # Physical interface layer
├── network/      # Communication layer  
├── services/     # Business logic layer
└── config/       # Configuration management
```

### 2. Error Handling Strategy
- Immediate LED feedback for user awareness
- Detailed serial logging for debugging
- Graceful degradation (WiFi reconnection)

### 3. Configuration Pattern
- Separate secrets file (git-ignored)
- Environment-specific settings
- Runtime configuration loading

## Migration to Arduino

When we switched to Arduino, we preserved these architectural insights:
- **Single responsibility**: Each Arduino function has clear purpose
- **Error handling**: Same fail-fast approach with LED feedback
- **Configuration**: Same secrets separation pattern
- **Async concepts**: Non-blocking operations in Arduino loop()

This Python structure served as an excellent design foundation even when switching platforms.