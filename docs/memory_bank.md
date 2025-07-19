# Memory Bank - Home Automation Button Project

## Overview

This memory bank will grow organically as features are implemented, capturing decisions, implementations, and learning insights throughout the development process.

## Current Status

- **Repository Setup**: Complete ✅
- **Phase 1 Development**: Ready to begin
- **Architecture**: Domain-based organization established

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

*Additional entries will be added as development progresses:*
- LIFX API integration and testing results
- Software architecture choices and implementation patterns
- Problem-solving approaches and debugging insights
- Performance optimizations and testing strategies

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