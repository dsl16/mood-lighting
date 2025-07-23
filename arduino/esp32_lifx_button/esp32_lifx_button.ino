/*
 * ESP32 LIFX Button Controller - Arduino Version
 * 
 * A single-button smart home controller that sets all LIFX lights to a warm
 * orange "sunset" scene (#f08d24) with a single press. Features reliable
 * HTTPS communication, visual LED feedback, and WiFi auto-reconnection.
 * 
 * Hardware:
 * - Button: GPIO 4 (with pull-up resistor and debouncing capacitor)
 * - System LED: GPIO 2 (built-in blue LED)
 * - Error LED: GPIO 5 (external red LED)
 * - Success LED: GPIO 18 (external green LED)
 * 
 * Features:
 * - Sunset scene activation (warm orange #f08d24)
 * - Direct HTTPS to LIFX Cloud API
 * - Hardware interrupt button handling with debouncing
 * - Multi-color LED status feedback
 * - Automatic WiFi reconnection
 * - Completely self-contained operation
 * 
 * Author: Darrin Lim
 * Project: ESP32 Smart Home Button System
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "secrets.h"  // Contains WiFi and LIFX credentials
const char* LIFX_API_URL = "https://api.lifx.com/v1/lights/all/state";

// GPIO pins
const int BUTTON_PIN = 4;
const int SYSTEM_LED_PIN = 2;
const int ERROR_LED_PIN = 5;
const int SUCCESS_LED_PIN = 18;

// Button debouncing
volatile bool buttonPressed = false;
unsigned long lastButtonTime = 0;
const int DEBOUNCE_DELAY = 200;  // Increased from 50ms to 200ms

// Status tracking
bool systemReady = false;
bool wifiConnected = false;

void setup() {
  Serial.begin(115200);
  delay(2000);  // Give serial time to initialize
  Serial.println("🚀 ESP32 LIFX Button Controller Starting...");
  
  // Initialize GPIO pins
  setupHardware();
  
  // Connect to WiFi
  connectWiFi();
  
  // Test LIFX API connection
  if (testLIFXConnection()) {
    systemReady = true;
    digitalWrite(SYSTEM_LED_PIN, HIGH);  // Solid blue = ready
    Serial.println("✅ System ready! Press button for sunset scene.");
    Serial.println("   🌅 Button = All lights to warm orange (#f08d24)");
    Serial.println("   🔴 Red LED = Error");
    Serial.println("   🟢 Green LED = Success");
    Serial.println("   🔵 Blue LED = System Status");
  } else {
    Serial.println("❌ LIFX API test failed - check credentials");
    digitalWrite(ERROR_LED_PIN, HIGH);
  }
}

void loop() {
  // Handle button press
  if (buttonPressed && systemReady) {
    buttonPressed = false;  // Clear flag immediately
    
    Serial.println("🔘 Button pressed!");
    blinkLED(SYSTEM_LED_PIN, 100);  // Quick blink feedback
    
    // Add small delay to prevent rapid processing
    delay(100);
    
    // Activate sunset scene
    if (setSunsetScene()) {
      blinkLED(SUCCESS_LED_PIN, 200);  // Success blink
    } else {
      blinkLED(ERROR_LED_PIN, 1000);   // Error indication
    }
    
    // Extra protection - clear flag again after processing
    buttonPressed = false;
  }
  
  // Check WiFi connection periodically
  static unsigned long lastWiFiCheck = 0;
  if (millis() - lastWiFiCheck > 30000) {  // Check every 30 seconds
    lastWiFiCheck = millis();
    
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("📶 WiFi disconnected, reconnecting...");
      systemReady = false;
      digitalWrite(SYSTEM_LED_PIN, LOW);
      connectWiFi();
      
      if (WiFi.status() == WL_CONNECTED) {
        systemReady = true;
        digitalWrite(SYSTEM_LED_PIN, HIGH);
        Serial.println("✅ WiFi reconnected, system ready");
      }
    }
  }
  
  delay(10);  // Small delay for stability
}

/**
 * Initialize GPIO pins and hardware components
 * Sets up button interrupt and LED outputs
 */
void setupHardware() {
  Serial.println("🔧 Setting up hardware...");
  
  // Button with internal pull-up resistor
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterrupt, FALLING);
  
  // LED outputs for status feedback
  pinMode(SYSTEM_LED_PIN, OUTPUT);
  pinMode(ERROR_LED_PIN, OUTPUT);
  pinMode(SUCCESS_LED_PIN, OUTPUT);
  
  // Initialize all LEDs off
  digitalWrite(SYSTEM_LED_PIN, LOW);
  digitalWrite(ERROR_LED_PIN, LOW);
  digitalWrite(SUCCESS_LED_PIN, LOW);
  
  Serial.println("   ✅ Hardware initialized");
}

/**
 * Connect to WiFi network with visual feedback
 * Blinks system LED during connection attempt
 */
void connectWiFi() {
  Serial.println("📶 Connecting to WiFi...");
  
  // Visual feedback during connection
  for (int i = 0; i < 3; i++) {
    digitalWrite(SYSTEM_LED_PIN, HIGH);
    delay(200);
    digitalWrite(SYSTEM_LED_PIN, LOW);
    delay(200);
  }
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  // Wait for connection with timeout
  int attempts = 0;
  const int MAX_ATTEMPTS = 20;
  while (WiFi.status() != WL_CONNECTED && attempts < MAX_ATTEMPTS) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  // Report connection result
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println();
    Serial.print("   ✅ Connected to ");
    Serial.println(WIFI_SSID);
    Serial.print("   📍 IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("❌ WiFi connection failed");
    digitalWrite(ERROR_LED_PIN, HIGH);
  }
}

bool testLIFXConnection() {
  Serial.println("🔗 Testing LIFX API connection...");
  
  HTTPClient http;
  http.begin("https://api.lifx.com/v1/lights/all");
  http.addHeader("Authorization", "Bearer " + String(LIFX_TOKEN));
  http.setTimeout(10000);  // 10 second timeout
  
  int httpCode = http.GET();
  
  if (httpCode == 200) {
    String payload = http.getString();
    Serial.println("   ✅ LIFX API connection successful");
    
    // Parse JSON to count lights
    DynamicJsonDocument doc(4096);
    deserializeJson(doc, payload);
    
    if (doc.size() > 0) {
      Serial.printf("   💡 Found %d lights ready for sunset mode\n", doc.size());
      http.end();
      return true;
    }
  }
  
  Serial.printf("   ❌ LIFX API test failed (HTTP %d)\n", httpCode);
  http.end();
  return false;
}

bool setSunsetScene() {
  Serial.println("🌅 Activating sunset scene...");
  
  HTTPClient http;
  http.begin(LIFX_API_URL);  // All lights
  http.addHeader("Authorization", "Bearer " + String(LIFX_TOKEN));
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(10000);  // Longer timeout for all lights
  
  // Sunset scene: warm orange color (#f08d24) with full brightness
  String jsonPayload = "{"
    "\"power\": \"on\","
    "\"color\": \"#f08d24\","
    "\"brightness\": 1.0,"
    "\"duration\": 2.0"  // 2 second fade
  "}";
  
  int httpCode = http.PUT(jsonPayload);
  
  if (httpCode == 207 || httpCode == 200) {  // 207 = Multi-Status (LIFX bulk response)
    Serial.println("   ✅ All lights set to sunset mode!");
    Serial.println("   🌅 Color: Warm orange (#f08d24)");
    http.end();
    return true;
  } else {
    Serial.printf("   ❌ Failed to set sunset scene (HTTP %d)\n", httpCode);
    String response = http.getString();
    Serial.println("   Response: " + response);
    http.end();
    return false;
  }
}

/**
 * Button interrupt handler with software debouncing
 * Called on falling edge of button press
 */
void buttonInterrupt() {
  unsigned long currentTime = millis();
  
  // Software debouncing - ignore rapid presses
  if (currentTime - lastButtonTime > DEBOUNCE_DELAY) {
    buttonPressed = true;
    lastButtonTime = currentTime;
  }
}

/**
 * Utility function to blink an LED for specified duration
 * @param pin GPIO pin number for the LED
 * @param duration How long to keep LED on (milliseconds)
 */
void blinkLED(int pin, int duration) {
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
}