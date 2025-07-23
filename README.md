# Mood Lighting - ESP32 Smart Button System

A single-button smart home controller that transforms all your LIFX lights into a warm, cozy "sunset scene" with just one press. Built with ESP32 and Arduino for reliable, self-contained operation.

## Project Overview

This project implements a physical WiFi-enabled button that triggers a beautiful sunset lighting scene across all LIFX lights in your home. The button is completely autonomous - just press it and watch your entire house transform to a warm orange glow (#f08d24).

**Current Status**: ✅ **Production Ready** - Working hardware with reliable Arduino implementation

## Quick Start

### Hardware Requirements
- ESP32 development board (DevKit V1 recommended)
- Tactile push button with pull-up resistor
- Red and green LEDs for status feedback
- Breadboard and jumper wires

### Software Setup
1. **Install Arduino IDE** with ESP32 support
2. **Clone Repository**: `git clone [repository-url]`
3. **Configure Credentials**: 
   - Copy `arduino/esp32_lifx_button/secrets.h.example` to `secrets.h`
   - Add your WiFi network name and password
   - Add your LIFX API token
4. **Flash to ESP32**: Open `.ino` file in Arduino IDE and upload

### Wiring Guide
See [docs/hardware/wiring_diagram.md](./docs/hardware/wiring_diagram.md) for complete wiring instructions.

## Features

- 🌅 **Sunset Scene**: Transform all lights to warm orange (#f08d24) with 2-second fade
- 🔘 **One Button**: Simple, reliable single-press operation
- 🔄 **Auto-Reconnect**: Handles WiFi outages gracefully
- 💡 **LED Feedback**: Visual status indicators (red=error, green=success, blue=ready)
- 🔒 **Secure**: Credentials stored separately from code
- ⚡ **Fast Response**: Sub-second button response time
- 🏠 **Self-Contained**: No central server or cloud dependencies (except LIFX API)

## Project Structure

```
arduino/
└── esp32_lifx_button/
    ├── esp32_lifx_button.ino    # Main Arduino code
    ├── secrets.h                # WiFi and LIFX credentials (git-ignored)
    ├── secrets.h.example        # Template for credentials
    └── README.md                # Arduino-specific setup guide

docs/
├── development/                 # Development learnings and patterns
├── platform-comparison/        # MicroPython vs Arduino analysis
├── architecture/               # Design decisions and patterns
└── hardware/                   # Wiring diagrams and component guides
```

## Development Journey

This project began with MicroPython but switched to Arduino for production reliability. The documentation preserves all learnings from both approaches:

- **MicroPython Phase**: Excellent for prototyping, but hit SSL/HTTPS limitations
- **Arduino Phase**: Production-ready solution with reliable HTTPS support
- **Architecture Evolution**: From modular Python design to focused Arduino implementation

See [docs/platform-comparison/micropython-vs-arduino.md](./docs/platform-comparison/micropython-vs-arduino.md) for detailed analysis.

## Technical Architecture

- **Event-Driven**: Hardware interrupt button handling for responsive UI
- **Fail-Fast**: Immediate error detection with LED feedback
- **Stateless**: No local state caching - always queries current light state
- **Self-Healing**: Automatic WiFi reconnection and error recovery

## Security

- **Credentials Separation**: `secrets.h` file is git-ignored
- **API Security**: Uses LIFX Cloud API with proper token authentication
- **No Hardcoded Secrets**: All sensitive data in separate configuration

## Getting Help

- **Hardware Setup**: See [docs/hardware/](./docs/hardware/)
- **Troubleshooting**: Check Serial Monitor at 115200 baud for debug output
- **Project Specifications**: [CLAUDE.md](./CLAUDE.md) contains comprehensive technical details
- **Development Insights**: [docs/development/](./docs/development/) for testing patterns and project structure learnings

## What's Next

The current implementation provides a solid foundation for expansion:
- **Multiple Buttons**: Architecture supports multiple independent buttons
- **Custom Scenes**: Easy to modify for different colors/brightness
- **Local Protocol**: Could be upgraded to LIFX local UDP for faster response
- **Web Interface**: Potential for web-based configuration

---

**Ready to build?** Start with the [Arduino setup guide](./arduino/esp32_lifx_button/README.md) and transform your home lighting with a single button press! 🌅