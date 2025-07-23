# ESP32 Button Controller Wiring Diagram

## Overview

Complete wiring guide for ESP32 DevKit V1 + tactile button + 3 LEDs breadboard assembly for Phase 1 single button prototype.

## Component List

### Primary Components
- **ESP32 DevKit V1** (DOIT board with 30 pins)
- **12x12mm Tactile Push Button** (4-pin)
- **LEDs**: 1x Red (5mm), 1x Green (5mm) 
- **830-point Breadboard**

### Electronic Components  
- **Resistors**: 1x 10kΩ (pull-up), 2x 220Ω (LED current limiting)
- **Capacitor**: 1x 100nF ceramic (debouncing) 
- **Jumper Wires**: Male-to-male breadboard wires

## Pin Assignment Summary

| Function | ESP32 Pin | Component | Notes |
|----------|-----------|-----------|-------|
| Button Input | GPIO 4 | Tactile button | With pull-up + debouncing |
| System Status | GPIO 2 | Built-in LED | Blue LED on ESP32 board |
| Error LED | GPIO 5 | External red LED | Via 220Ω resistor |
| Success LED | GPIO 18 | External green LED | Via 220Ω resistor |
| Power | 3V3 | Breadboard power rail | 3.3V supply |
| Ground | GND | Breadboard ground rail | Common ground |

## Detailed Wiring Diagram

```
ESP32 DevKit V1 Pinout (30-pin version):
                     
    EN  [ ]       [ ] D23
   VP   [ ]       [ ] D22  
   VN   [ ]       [ ] TXD0
   D34  [ ]       [ ] RXD0
   D35  [ ]       [ ] D21
   D32  [ ]       [ ] D19
   D33  [ ]       [ ] D18  ──┐ (Success LED)
   D25  [ ]       [ ] D5   ──┼─┐ (Error LED)  
   D26  [ ]       [ ] TXD2
   D27  [ ]       [ ] RXD2
   D14  [ ]       [ ] D4   ──┼─┼─┐ (Button Input)
   D12  [ ]       [ ] D2   ──┼─┼─┼─┐ (Built-in LED)
   D13  [ ]       [ ] D15     │ │ │ │
   GND  [ ]       [ ] D0      │ │ │ │
   VIN  [ ]       [ ] D1      │ │ │ │
   3V3  [ ]       [ ] GND ────┼─┼─┼─┼─┐ (Ground)
                              │ │ │ │ │
                        Power Rail  │ │ │ │
                             ┌──────┘ │ │ │
                             │        │ │ │
                     Ground Rail ─────┼─┼─┼─┘
                             │        │ │ │
                             │        │ │ │
```

## Breadboard Layout

```
Breadboard Power Rails:
    Red (+)  Power Rail: Connected to ESP32 3V3
    Blue (-) Ground Rail: Connected to ESP32 GND

Component Placement (Left to Right):
    Columns 1-15:  ESP32 DevKit V1 (spans center divide)
    Columns 20-25: Button circuit with pull-up and debouncing
    Columns 30-35: Error LED (red) with resistor
    Columns 40-45: Success LED (green) with resistor
```

## Circuit Details

### 1. Button Circuit (GPIO 4)

```
Detailed Button Wiring:

3V3 Power Rail ──── 10kΩ Resistor ──── GPIO 4 (Pin D4)
                                         │
                    100nF Capacitor ─────┤
                                         │
Ground Rail ──────── Tactile Button ────┘

Physical Connections:
1. GPIO 4 → Breadboard row (e.g., row 25)
2. 10kΩ resistor: Row 25 to Power Rail (+)
3. 100nF capacitor: Row 25 to Ground Rail (-)  
4. Button pin 1: Row 25
5. Button pin 2: Ground Rail (-)
```

**Button Operation**: 
- **Unpressed**: GPIO 4 reads HIGH (3.3V via 10kΩ pull-up)
- **Pressed**: GPIO 4 reads LOW (connected to ground through button)
- **Debouncing**: 100nF capacitor filters electrical noise

### 2. Error LED Circuit (GPIO 5)

```
GPIO 5 ──── 220Ω Resistor ──── Red LED Anode ──── Red LED Cathode ──── GND

Physical Connections:
1. GPIO 5 → 220Ω resistor (one end)
2. Resistor other end → Red LED anode (longer leg)
3. Red LED cathode (shorter leg) → Ground Rail (-)
```

**LED Operation**:
- **GPIO 5 HIGH**: LED turns on (current flows through 220Ω resistor)
- **GPIO 5 LOW**: LED turns off
- **Current**: ~10mA (safe for GPIO pin and LED)

### 3. Success LED Circuit (GPIO 18)

```
GPIO 18 ──── 220Ω Resistor ──── Green LED Anode ──── Green LED Cathode ──── GND

Physical Connections:  
1. GPIO 18 → 220Ω resistor (one end)
2. Resistor other end → Green LED anode (longer leg)
3. Green LED cathode (shorter leg) → Ground Rail (-)
```

### 4. Power Connections

```
ESP32 3V3 pin → Breadboard Power Rail (Red +)
ESP32 GND pin → Breadboard Ground Rail (Blue -)

All components reference these power rails for consistent voltage/ground.
```

## Step-by-Step Assembly Instructions

### Step 1: Prepare Breadboard
1. **Insert ESP32**: Place ESP32 DevKit V1 across center divide of breadboard
   - Pins 1-15 on left side, pins 16-30 on right side
   - USB connector should face away from breadboard for easy access
   - Ensure all pins are properly seated in breadboard holes

### Step 2: Power Rail Connections  
1. **3.3V Power**: Red jumper wire from ESP32 "3V3" pin to breadboard red power rail
2. **Ground**: Black jumper wire from ESP32 "GND" pin to breadboard blue ground rail

### Step 3: Button Circuit Assembly
1. **Place button**: Insert 12x12mm tactile button in breadboard (spans 4 holes)
2. **Pull-up resistor**: 10kΩ resistor from GPIO 4 to power rail (+)
3. **Debouncing capacitor**: 100nF capacitor from GPIO 4 to ground rail (-)
4. **Button connection**: One button pin to GPIO 4, other pin to ground rail (-)

### Step 4: LED Circuits
1. **Error LED (Red)**:
   - 220Ω resistor from GPIO 5 to red LED anode (longer leg)  
   - Red LED cathode (shorter leg) to ground rail (-)
2. **Success LED (Green)**:
   - 220Ω resistor from GPIO 18 to green LED anode (longer leg)
   - Green LED cathode (shorter leg) to ground rail (-)

### Step 5: Verification Checklist
- [ ] ESP32 properly seated and stable
- [ ] Power rails connected (3V3 and GND)
- [ ] Button circuit complete with pull-up and debouncing
- [ ] Both LEDs properly oriented (long leg = anode)
- [ ] All resistors in place (10kΩ for button, 220Ω for each LED)
- [ ] No short circuits (check with multimeter if available)
- [ ] All connections secure and properly inserted

## Electrical Specifications

### Power Requirements
- **ESP32 Supply**: 3.3V (provided by onboard regulator from USB 5V)
- **Total Current**: ~80mA (ESP32: 60mA, LEDs: 20mA max)
- **USB Power**: Sufficient for prototype (500mA available)

### Component Ratings
- **10kΩ Pull-up**: Power = V²/R = (3.3V)²/10kΩ = 1.1mW (well under rating)
- **220Ω LED Resistors**: Current = (3.3V - 2.1V)/220Ω = 5.5mA per LED
- **100nF Capacitor**: Voltage rating > 10V (ceramic capacitors typically 25V+)

### Safety Considerations
- **No high voltages**: Entire circuit operates at 3.3V maximum
- **Current limited**: All GPIO pins protected by resistors
- **ESD protection**: Handle ESP32 with basic anti-static precautions
- **Short circuit protection**: Double-check connections before power-on

## Troubleshooting Guide

### Common Issues
1. **ESP32 doesn't power on**:
   - Check USB cable connection
   - Verify ESP32 is properly seated in breadboard
   - Try different USB port or cable

2. **Button doesn't register presses**:
   - Verify pull-up resistor (10kΩ) is connected
   - Check button is properly inserted (spans 4 holes)
   - Confirm GPIO 4 connection

3. **LEDs don't light up**:
   - Check LED polarity (long leg = anode to resistor)
   - Verify 220Ω resistors are in place
   - Test GPIO pins with multimeter (should show 3.3V when HIGH)

4. **Erratic button behavior**:
   - Confirm 100nF debouncing capacitor is connected
   - Check for loose connections in button circuit

### Test Procedures
1. **Power test**: ESP32 built-in LED should light when connected to USB
2. **GPIO test**: Use multimeter to verify GPIO voltages
3. **Button test**: GPIO 4 should read 3.3V normally, 0V when pressed
4. **LED test**: Manually connect LED circuits to 3.3V to verify operation

## Pin Reference Quick Card

```
┌─────────────────────────────────────┐
│  ESP32 LIFX Button Controller v1.0  │
├─────────────────────────────────────┤
│  GPIO 4  → Button Input (pull-up)   │
│  GPIO 2  → System LED (built-in)    │  
│  GPIO 5  → Error LED (red)          │
│  GPIO 18 → Success LED (green)      │
│  3V3     → Power rail (+)           │
│  GND     → Ground rail (-)          │
└─────────────────────────────────────┘
```

Keep this reference handy during assembly and debugging!

## Next Steps After Assembly

1. **Visual Inspection**: Verify all connections match this diagram
2. **Power Test**: Connect USB and check ESP32 powers on
3. **Firmware Flash**: Upload MicroPython firmware using esptool
4. **Application Deploy**: Upload src/main.py to ESP32
5. **Functional Test**: Press button and verify LIFX light toggles

Assembly complete = Ready for firmware deployment! 🚀