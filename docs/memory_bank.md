# Memory Bank - Home Automation Button Project

## Overview

This memory bank will grow organically as features are implemented, capturing decisions, implementations, and learning insights throughout the development process.

## Current Status

- **Repository Setup**: Complete ✅
- **Project Restructuring**: Complete ✅
- **Phase 1 Development**: main.py ready for ESP32 deployment
- **Testing Infrastructure**: Professional testing framework established
- **Hardware**: Ordered (arriving 2-3 days)

## Quick Links

- [Project Specifications](../CLAUDE.md) - Complete project requirements and technical specifications
- [README](../README.md) - Project overview and quick start guide

## Development Notes

### Hardware Component Selection ✅
- **ESP32 Board**: DOIT ESP32 DevKit V1 selected for MicroPython compatibility
- **Components**: WayinTop starter kit + Gikfun 12mm tactile buttons
- **Budget**: $48 total, within $50 target
- **Details**: [Hardware Component Selection](hardware/component_selection.md)

### Development Environment Setup ✅
- **Primary Workflow**: VS Code + PyMakr extension for seamless ESP32 development
- **Backup Workflow**: Thonny IDE for complex hardware debugging
- **MicroPython Firmware**: v1.24.1 stable (ESP32_GENERIC) downloaded and ready
- **Tools**: esptool.py v4.9.0, virtual environment, VS Code workspace configured
- **Details**: [Development Environment Setup](software/development_environment_setup.md)

### LIFX API Integration and Testing ✅
- **API Token**: Validated with full read/write permissions for 5 lights
- **Toggle Functionality**: Confirmed working with 600-800ms response time
- **Light Discovery**: Kitchen, Living room, Bedroom lamp, moon, Flower Light
- **Details**: [LIFX API Integration](software/lifx_api_integration.md)

### WiFi Manager Decision ✅
- **Solution**: Use micropython-esp-wifi-manager v1.8.0 via PyPI (no custom code needed)
- **Integration**: 3 lines in main.py, library handles all WiFi complexity
- **Rationale**: Focus development effort on button logic, not WiFi edge cases
- **Details**: [WiFi Manager Decision](software/wifi_manager_plan.md)

### Phase 1 ESP32 Application ✅
- **Implementation**: Complete single-file MicroPython application (src/main.py)
- **Features**: Button interrupt handling, LIFX API integration, LED feedback, WiFi auto-reconnection
- **Architecture**: Event-driven with fail-fast error handling and sub-second response target
- **Hardware Support**: GPIO 4 button, GPIO 2/5/18 LEDs, automatic debouncing
- **Testing**: Logic validated via desktop testing with mocked hardware components

### Project Structure Modernization ✅  
- **Architecture**: Migrated to proper Python package structure with src/ organization
- **Testing Framework**: Professional pytest setup with unit/integration/hardware test categories
- **Dual Platform Support**: Separate test files for Desktop Python vs MicroPython execution
- **Development Quality**: pyproject.toml, black/flake8 configuration, comprehensive fixtures
- **Test Coverage**: Main controller logic, LIFX API, hardware mocking, error scenarios

### Development Workflow Guide ✅
- **Virtual Environment**: Always use existing venv/, never install packages globally
- **IDE Configuration**: VS Code + PyMakr primary, Thonny backup for ESP32 debugging
- **Platform Detection**: Conditional imports for desktop Python vs MicroPython compatibility
- **Tool Prerequisites**: esptool.py, pytest, requests verification before ESP32 work
- **Details**: [Development Workflow Guide](software/development_workflow_guide.md)

### Development Environment Completion ✅
- **Tool Installation**: pytest 8.4.1, mpremote 1.25.0, esptool 4.9.0 all verified working
- **Import Issue Resolution**: Fixed secrets.py conflict by renaming to project_secrets.py
- **Testing Validation**: Complete LIFX API test suite passes (5 lights discovered, toggle verified)
- **Cross-Platform Support**: Desktop Python and MicroPython import paths validated
- **Ready for Hardware**: Complete toolchain prepared for ESP32 deployment when components arrive

*Additional entries will be added as development progresses:*
- Hardware assembly and wiring implementation
- Performance optimization and timing validation  
- Multi-button scaling and configuration management

## Memory Bank Structure

As development progresses, this will expand to include:

```
docs/
├── memory_bank.md (this file)
├── hardware/      # Hardware decisions and component guides
├── software/      # Architecture decisions and code patterns
├── troubleshooting/ # Common issues and solutions
└── learning/      # Lessons learned and best practices
```

Each section will be created and populated as relevant content emerges during development.