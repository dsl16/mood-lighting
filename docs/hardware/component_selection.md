# Hardware Component Selection - Memory Bank Entry

## Component Selection Overview

**Date**: July 19, 2025  
**Phase**: Phase 1 - Single Button Prototype  
**Budget**: $48 total (within $50 target)  
**Delivery**: 2-3 days via Amazon Prime  

## Primary Hardware Decisions

### ESP32 Development Board: DOIT ESP32 DevKit V1

**Selected**: [DIYmall ESP32-WROOM-32 Development Board - 2 Pack](https://www.amazon.com/ESP32-WROOM-32-Development-ESP-32S-Bluetooth-forArduino/dp/B08PCPJ12M)

**Why This Board**:
- Most recommended ESP32 for beginners and MicroPython development
- Built-in USB-to-UART (CP2102) for easy programming via USB cable
- 36 pins broken out in breadboard-friendly layout
- Built-in RESET (EN) and BOOT buttons for development convenience
- Voltage regulator included (3.3V from 5V USB)
- Proven compatibility with MicroPython firmware
- Strong community support and documentation

**Technical Specifications**:
- **MCU**: ESP32-WROOM-32 (dual-core, 240MHz, 512KB RAM)
- **Connectivity**: WiFi 802.11 b/g/n + Bluetooth 4.2 (BR/EDR + BLE)
- **Pins**: 36 GPIO pins (18 per side)
- **Programming**: CP2102 USB-to-UART converter
- **Power**: 3.3V/5V via USB or external power
- **Size**: Breadboard-friendly form factor

**Alternatives Considered**:
- ESP32-DevKitC V4 (official Espressif): More expensive (~$15-20 vs ~$10-12)
- ESP32-S3 variants: Newer but less community support for MicroPython
- NodeMCU-32S: Similar features but less common pinout

**Quantity**: 2 boards ($20 total)
- 1 for prototype development
- 1 for backup/expansion to multi-button system

### Electronics Components: WayinTop Starter Kit

**Selected**: [WayinTop Electronics Component Fun Kit](https://www.amazon.com/WayinTop-Electronics-Electronic-Breadboard-Resistance/dp/B07Z1BK7NG)

**Why This Kit**:
- Specifically mentions ESP32/ESP8266 compatibility
- Well-organized storage box for component management
- Includes comprehensive project guide and tutorials
- Quality components with good customer reviews
- Breadboard + power supply module included

**Kit Contents**:
- 830-point solderless breadboard
- Breadboard power supply module (3.3V/5V)
- Jumper wires (male-male, male-female, female-female)
- LEDs (multiple colors: red, green, blue, yellow, white)
- Resistors (common values: 220Ω, 1kΩ, 10kΩ, etc.)
- Capacitors, transistors, sensors
- Organized storage compartments

**Price**: ~$18

### Large Tactile Push Buttons

**Selected**: [Gikfun 12x12mm Tactile Push Buttons - 25 Pack](https://www.amazon.com/Gikfun-12x12x7-3-Tactile-Momentary-Arduino/dp/B01E38OS7K)

**Why These Buttons**:
- **Size**: 12mm x 12mm - large enough for satisfying tactile feedback
- **Feel**: Solid "click" response as specified in CLAUDE.md requirements
- **Compatibility**: 4-pin DIP design fits standard breadboards
- **Quantity**: 25 buttons provides plenty for expansion (need only 7 max)
- **Quality**: Good customer reviews for durability and tactile response
- **Caps**: Includes button caps for improved user experience

**Technical Specifications**:
- **Size**: 12mm x 12mm x 7.3mm
- **Type**: Momentary SPST (normally open)
- **Mounting**: 4-pin DIP, breadboard compatible
- **Actuation Force**: Medium (satisfying click without being too hard)
- **Electrical**: Rated for low-voltage DC circuits

**Price**: ~$10

## Pin Assignment Plan

```
ESP32 DevKit V1 Pin Assignments:
├── Hardware Input
│   ├── Button Input: GPIO 4 (external tactile button)
│   └── Built-in Button: GPIO 0 (BOOT button for testing)
├── Status/Feedback LEDs  
│   ├── System Status: GPIO 2 (built-in LED)
│   ├── Error Indicator: GPIO 5 (external red LED)
│   └── Success Indicator: GPIO 18 (external green LED)
├── Power & Ground
│   ├── 3.3V: Pin labeled "3V3"
│   └── Ground: Pin labeled "GND"
└── Future Expansion
    ├── Additional Buttons: GPIO 12, 13, 14, 15
    └── Additional LEDs: GPIO 19, 21, 22, 23
```

**Pin Selection Rationale**:
- **GPIO 4**: No special functions, perfect for button input with pull-up
- **GPIO 2**: Built-in LED, ideal for system status indication
- **GPIO 5**: General purpose, good for external LED control
- **GPIO 18**: General purpose, no conflicts with SPI/I2C
- **Future pins**: Selected to avoid boot-critical pins and special functions

## Wiring Approach

### Button Wiring (with Hardware Debouncing)
```
Button Circuit:
GPIO 4 ──┐
         │
         ├── 10kΩ Resistor ── 3.3V (pull-up)
         │
         ├── Tactile Button ── GND
         │
         └── 100nF Capacitor ── GND (debouncing)
```

### LED Wiring
```
LED Circuit (for each LED):
GPIO Pin ── 220Ω Resistor ── LED Anode ── LED Cathode ── GND
```

## Budget Breakdown

| Component | Quantity | Unit Price | Total | Notes |
|-----------|----------|------------|-------|--------|
| ESP32 DevKit V1 | 2 boards | $10 | $20 | DIYmall 2-pack |
| Electronics Kit | 1 kit | $18 | $18 | WayinTop comprehensive kit |
| 12mm Tactile Buttons | 25 buttons | $0.40 | $10 | Gikfun quality buttons |
| **Total** | | | **$48** | **$2 under budget** |

## Development Workflow

### Phase 1: Single Button Prototype
1. **Breadboard Setup**: ESP32 + 1 button + 2 LEDs on breadboard
2. **Programming**: USB cable connection for MicroPython development
3. **Testing**: Serial monitor for debugging and development feedback
4. **Iteration**: Easy component swapping on breadboard for experimentation

### Phase 2: Multi-Button Expansion
1. **Scaling**: Add 2-6 additional buttons using same wiring pattern
2. **Enclosure**: 3D print custom enclosures (3D printer available)
3. **Professional Feel**: Move from breadboard to custom PCB if desired

## Procurement Status

- **Status**: ✅ **ORDERED** (July 19, 2025)
- **Delivery**: 2-3 days via Amazon Prime
- **Budget**: $48 total (within $50 target)
- **Timeline**: Hardware arriving while software development continues

## Next Steps

1. ~~**Order Components**: Use provided Amazon links~~ ✅ **COMPLETED**
2. **Development Environment**: Set up MicroPython tools while waiting for delivery
3. ~~**API Testing**: Validate LIFX integration from computer first~~ ✅ **COMPLETED**
4. **Write main.py**: Core ESP32 application logic
5. **Physical Setup**: Breadboard wiring when components arrive (2-3 days)

## Key Decision Rationale

**Why DOIT ESP32 DevKit V1 over alternatives**:
- Proven MicroPython compatibility (critical requirement)
- Strong community support for troubleshooting
- Built-in programming interface (no external programmer needed)
- Breadboard-friendly layout for prototype development
- Cost-effective for buying multiple units

**Why large 12mm buttons**:
- Satisfying tactile feedback as specified in CLAUDE.md
- Easy to press for family members of all ages
- Professional feel for finished product
- Sufficient size for clear labeling if needed

**Why comprehensive starter kit over individual components**:
- Better value than buying components separately
- Organized storage for long-term project management
- Includes power supply module and breadboard
- Extra components available for experimentation and future features

This hardware selection provides everything needed for Phase 1 prototype development and scales well to the complete 7-button system outlined in CLAUDE.md.