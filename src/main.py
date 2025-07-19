#!/usr/bin/env micropython
"""
ESP32 Single Button LIFX Controller - Phase 1 Prototype
Main application file for MicroPython on ESP32

Features:
- Single button input with hardware debouncing
- LIFX light toggle via cloud API
- LED status feedback (system/error/success)
- WiFi auto-connection and reconnection
- Sub-second response time target
- Fail-fast error handling

Hardware:
- ESP32 DevKit V1
- Button on GPIO 4 (with pull-up + debouncing capacitor)
- System LED on GPIO 2 (built-in)
- Error LED on GPIO 5 (external red)
- Success LED on GPIO 18 (external green)
"""

import time
import gc
from machine import Pin, Timer
import network
import json

# Conditional imports for MicroPython vs desktop testing
try:
    import urequests as requests
    import ujson as json_lib
    MICROPYTHON = True
except ImportError:
    import requests
    import json as json_lib
    MICROPYTHON = False

# Import credentials
from secrets import WIFI_SSID, WIFI_PASSWORD, LIFX_TOKEN

# Hardware pin assignments
BUTTON_PIN = 4          # Button input with pull-up
SYSTEM_LED_PIN = 2      # Built-in LED for system status
ERROR_LED_PIN = 5       # External red LED for errors
SUCCESS_LED_PIN = 18    # External green LED for success

# Configuration
WIFI_TIMEOUT = 10000    # 10 seconds
API_TIMEOUT = 400       # 400ms for fail-fast behavior
DEBOUNCE_TIME = 50      # 50ms button debouncing
BLINK_DURATION = 200    # LED blink duration in ms

# LIFX API configuration
LIFX_BASE_URL = "https://api.lifx.com/v1"
DEFAULT_LIGHT = "Kitchen"  # Primary light for toggle

class LightController:
    """Main controller for ESP32 button -> LIFX light system"""
    
    def __init__(self):
        self.setup_hardware()
        self.wifi = None
        self.last_button_time = 0
        self.system_ready = False
        
        print("🚀 ESP32 LIFX Button Controller Starting...")
        print(f"   Target light: {DEFAULT_LIGHT}")
        print(f"   API timeout: {API_TIMEOUT}ms")
    
    def setup_hardware(self):
        """Initialize GPIO pins and hardware"""
        print("🔧 Setting up hardware...")
        
        # Button input with internal pull-up
        self.button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        
        # LED outputs
        self.system_led = Pin(SYSTEM_LED_PIN, Pin.OUT)
        self.error_led = Pin(ERROR_LED_PIN, Pin.OUT)
        self.success_led = Pin(SUCCESS_LED_PIN, Pin.OUT)
        
        # Initialize LEDs off
        self.system_led.off()
        self.error_led.off()
        self.success_led.off()
        
        # Button interrupt for responsive input
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_pressed)
        
        print("   ✅ Hardware initialized")
    
    def connect_wifi(self):
        """Connect to WiFi with timeout and status indication"""
        print("📶 Connecting to WiFi...")
        self.blink_system_led()  # Indicate connection attempt
        
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        
        if not self.wifi.isconnected():
            self.wifi.connect(WIFI_SSID, WIFI_PASSWORD)
            
            # Wait for connection with timeout
            start_time = time.ticks_ms()
            while not self.wifi.isconnected():
                if time.ticks_diff(time.ticks_ms(), start_time) > WIFI_TIMEOUT:
                    self.error_led.on()
                    raise Exception("WiFi connection timeout")
                time.sleep_ms(100)
        
        ip = self.wifi.ifconfig()[0]
        print(f"   ✅ Connected to {WIFI_SSID}")
        print(f"   📍 IP address: {ip}")
        
        self.system_led.on()  # Solid LED = connected and ready
        self.system_ready = True
    
    def blink_system_led(self):
        """Quick blink to show system activity"""
        self.system_led.on()
        time.sleep_ms(BLINK_DURATION)
        self.system_led.off()
    
    def blink_success_led(self):
        """Quick green blink for successful operation"""
        self.success_led.on()
        time.sleep_ms(BLINK_DURATION)
        self.success_led.off()
    
    def show_error(self, duration_ms=1000):
        """Show error LED for specified duration"""
        self.error_led.on()
        time.sleep_ms(duration_ms)
        self.error_led.off()
    
    def button_pressed(self, pin):
        """Button interrupt handler with debouncing"""
        current_time = time.ticks_ms()
        
        # Debouncing - ignore rapid presses
        if time.ticks_diff(current_time, self.last_button_time) < DEBOUNCE_TIME:
            return
        
        self.last_button_time = current_time
        
        # Only process if system is ready
        if not self.system_ready:
            print("⚠️  System not ready, ignoring button press")
            return
        
        print("🔘 Button pressed!")
        self.blink_system_led()  # Immediate feedback
        
        # Schedule the actual light toggle (non-blocking)
        Timer(-1).init(mode=Timer.ONE_SHOT, period=10, callback=lambda t: self.toggle_light())
    
    def make_api_request(self, method, url, data=None):
        """Make HTTP request to LIFX API with timeout and error handling"""
        headers = {
            'Authorization': f'Bearer {LIFX_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=API_TIMEOUT/1000)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=API_TIMEOUT/1000)
            
            if response.status_code not in [200, 207]:  # 207 = Multi-Status (LIFX bulk ops)
                raise Exception(f"API error: {response.status_code}")
            
            result = response.json()
            response.close()  # Important for MicroPython memory management
            return result
            
        except Exception as e:
            print(f"❌ API request failed: {e}")
            raise
    
    def get_light_state(self, light_name):
        """Get current state of specified light"""
        url = f"{LIFX_BASE_URL}/lights/{light_name}/state"
        response = self.make_api_request('GET', url)
        
        if not response:
            raise Exception(f"No state data for {light_name}")
        
        return response[0]  # LIFX returns list with single item
    
    def set_light_state(self, light_name, power, brightness=None):
        """Set light power and optionally brightness"""
        url = f"{LIFX_BASE_URL}/lights/{light_name}/state"
        
        data = {'power': power}
        if brightness is not None:
            data['brightness'] = brightness
        
        response = self.make_api_request('PUT', url, data)
        return response
    
    def toggle_light(self):
        """Toggle the default light using stateless approach"""
        try:
            print(f"💡 Toggling {DEFAULT_LIGHT}...")
            
            # Step 1: Get current state (with timeout)
            current_state = self.get_light_state(DEFAULT_LIGHT)
            current_power = current_state['power']
            
            print(f"   Current state: {current_power}")
            
            # Step 2: Set opposite state
            new_power = 'off' if current_power == 'on' else 'on'
            self.set_light_state(DEFAULT_LIGHT, new_power)
            
            print(f"   ✅ {DEFAULT_LIGHT} -> {new_power}")
            self.blink_success_led()
            
        except Exception as e:
            print(f"❌ Light toggle failed: {e}")
            self.show_error()
            
            # Check WiFi connection and attempt reconnect
            if not self.wifi.isconnected():
                print("📶 WiFi disconnected, attempting reconnect...")
                try:
                    self.connect_wifi()
                except:
                    print("❌ WiFi reconnection failed")
    
    def run(self):
        """Main application loop"""
        try:
            # Initialize system
            self.connect_wifi()
            
            print("✅ System ready! Press button to toggle light.")
            print("   🔴 Red LED = Error")
            print("   🟢 Green LED = Success")
            print("   🔵 Blue LED = System Status")
            print()
            
            # Main loop - just keep system alive and handle WiFi
            while True:
                # Periodic WiFi check (every 30 seconds)
                if not self.wifi.isconnected():
                    print("📶 WiFi connection lost, reconnecting...")
                    self.system_ready = False
                    self.system_led.off()
                    try:
                        self.connect_wifi()
                    except Exception as e:
                        print(f"❌ WiFi reconnect failed: {e}")
                        self.show_error(2000)  # Longer error indication
                        time.sleep(5)  # Wait before retry
                        continue
                
                # Memory cleanup for long-running operation
                gc.collect()
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted! Cleaning up...")
            self.cleanup()
        except Exception as e:
            print(f"❌ System error: {e}")
            self.show_error(3000)
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown of system"""
        self.system_led.off()
        self.error_led.off()
        self.success_led.off()
        
        if self.wifi:
            self.wifi.active(False)
        
        print("🔄 System shutdown complete")

# Main execution
if __name__ == "__main__":
    controller = LightController()
    controller.run()