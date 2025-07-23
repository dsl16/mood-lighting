# Arduino ESP32 LIFX Button Controller

## Setup Instructions

1. **Install Arduino IDE** and ESP32 support
2. **Copy credentials** from `../../project_secrets.py` into the Arduino code:
   - Replace `YOUR_WIFI_SSID` with your WiFi network name
   - Replace `YOUR_PASSWORD` with your WiFi password  
   - Replace `YOUR_LIFX_TOKEN` with your LIFX API token

3. **Flash to ESP32**:
   - Open `esp32_lifx_button.ino` in Arduino IDE
   - Select Board: "ESP32 Dev Module"
   - Select Port: `/dev/tty.usbserial-0001` (or your ESP32 port)
   - Click Upload

## Hardware Requirements

Same wiring as MicroPython version:
- Button: GPIO 4 (with pull-up resistor)
- System LED: GPIO 2 (built-in blue)
- Error LED: GPIO 5 (external red)
- Success LED: GPIO 18 (external green)

See `../../docs/hardware/wiring_diagram.md` for complete wiring guide.

## Why Arduino Version?

This version solves HTTPS/SSL issues that MicroPython has with the LIFX API. Arduino's HTTP client has better SSL support for ESP32.