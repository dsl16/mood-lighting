# Mood Lighting - ESP32 Smart Button System

A physical button system for controlling LIFX smart lights using ESP32 microcontrollers and MicroPython.

## Project Overview

This project implements independent, WiFi-enabled buttons that trigger LIFX light controls through direct API calls. Each button operates autonomously with sub-second response times and fail-fast error handling.

**Current Status**: Repository setup complete, ready for Phase 1 development

## Quick Start

1. **Hardware Setup**: ESP32 development board + tactile button + LED indicator
2. **Credentials**: Copy `secrets.py.example` to `secrets.py` and add your WiFi/LIFX credentials
3. **Configuration**: Edit `src/config/config.json` for button-to-light mappings
4. **Deploy**: Flash MicroPython firmware to ESP32 and upload code

## Project Structure

```
src/
├── network/          # WiFi management and connectivity
├── lighting/         # LIFX API integration and light control
├── hardware/         # Button input and LED feedback handling
├── config/           # Configuration management and JSON parsing
└── main.py           # Application orchestration
```

## Development

- **Branch Strategy**: Feature development on `dev` branch, stable releases on `main`
- **Documentation**: See [CLAUDE.md](./CLAUDE.md) for comprehensive project specifications
- **Memory Bank**: Progressive documentation in `docs/` as features are implemented

## Architecture

- **Event-Driven**: Independent button operation with async light control
- **Fail-Fast**: Sub-second error detection with LED feedback
- **Stateless**: Query-then-set approach for reliable light state management
- **Scalable**: Domain-based code organization supports multiple buttons

## Security

- Credentials managed via `secrets.py` (git-ignored)
- API tokens never committed to version control
- Clear separation of code and configuration

For detailed specifications, implementation phases, and technical decisions, see [CLAUDE.md](./CLAUDE.md).