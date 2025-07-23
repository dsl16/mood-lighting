# Security Best Practices for IoT Projects

## Overview

This document captures security best practices learned during the ESP32 LIFX controller project, covering credential management, API security, and repository security for embedded IoT devices.

## Credential Management

### The Secrets Separation Pattern

Both MicroPython and Arduino implementations used the same core pattern:

#### MicroPython Implementation
```python
# project_secrets.py (git-ignored)
WIFI_SSID = "Your_Network_Name"
WIFI_PASSWORD = "your_wifi_password"  
LIFX_TOKEN = "your_lifx_api_token_here"

# main.py (version controlled)
from project_secrets import WIFI_SSID, WIFI_PASSWORD, LIFX_TOKEN
```

#### Arduino Implementation
```cpp
// secrets.h (git-ignored)
const char* WIFI_SSID = "Your_Network_Name";
const char* WIFI_PASSWORD = "your_wifi_password";
const char* LIFX_TOKEN = "your_lifx_api_token_here";

// esp32_lifx_button.ino (version controlled)
#include "secrets.h"
```

### Git Ignore Configuration

```gitignore
# Arduino secrets (NEVER commit credentials)
arduino/*/secrets.h

# Python secrets (if using MicroPython)
project_secrets.py
*.env
.env*
```

### Template Files for New Users

Both implementations provided template files:

```cpp
// secrets.h.example (version controlled)
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* LIFX_TOKEN = "YOUR_LIFX_TOKEN";
```

**Setup Process:**
1. New user copies `secrets.h.example` to `secrets.h`
2. Fills in actual credentials
3. Git automatically ignores `secrets.h` during commits

## API Security

### LIFX Cloud API Security

#### Token-Based Authentication
```cpp
// Proper HTTPS API authentication
http.addHeader("Authorization", "Bearer " + String(LIFX_TOKEN));
```

#### API Token Management
- **Generation**: Create read/write token via LIFX Cloud web interface
- **Scope**: Limit token permissions to only required operations
- **Storage**: Never hardcode in source code, always in separate config file
- **Rotation**: Consider periodic token rotation for long-term deployments

#### Network Security
```cpp
// Always use HTTPS for API calls
http.begin("https://api.lifx.com/v1/lights/all/state");  // ✅ Secure
// http.begin("http://api.lifx.com/...");                // ❌ Insecure
```

### API Error Handling

```cpp
// Don't expose sensitive information in error messages
if (httpCode != 200) {
    Serial.printf("❌ API request failed (HTTP %d)\n", httpCode);
    // Don't log: response body, tokens, or internal details
    return false;
}
```

## Repository Security

### Multiple Security Audits

The project underwent several security reviews:

#### Pre-Commit Security Check
```bash
# Check for potential secrets in staged files
git add -A --dry-run  # Preview what would be committed
rg -i "password|token|key|secret" arduino/ --type-not=md  # Search for secrets
git check-ignore arduino/esp32_lifx_button/secrets.h  # Verify git-ignore
```

#### Pattern Detection
```bash
# Search for specific credential patterns (use your actual network/token patterns)
grep -r "your_network\|your_password\|your_token" arduino/ || echo "No secrets found"
```

### False Positive Management

Some occurrences of "secrets" are legitimate:
```cpp
#include "secrets.h"  // ✅ Reference to config file (no actual secrets)
```

Vs actual secrets that should never be committed:
```cpp
const char* WIFI_PASSWORD = "actual_password";  // ❌ Would be caught by git-ignore
```

## Development Security Practices

### Secure Development Workflow

1. **Initial Setup:**
   ```bash
   git clone project
   cp arduino/esp32_lifx_button/secrets.h.example arduino/esp32_lifx_button/secrets.h
   # Edit secrets.h with actual credentials
   ```

2. **Daily Development:**
   ```bash
   git status  # Verify secrets.h not listed in changes
   git add .   # Git automatically ignores secrets.h
   git commit  # Only code changes committed, never credentials
   ```

3. **Pre-Commit Verification:**
   ```bash
   git diff --cached  # Review exactly what will be committed
   # Ensure no credential strings visible in diff
   ```

### IDE Security Configuration

#### Arduino IDE
- **Serial Monitor**: Avoid logging sensitive data in production
- **Debug Output**: Remove debug prints before production deployment
- **Example Code**: Never use real credentials in example/template code

#### VS Code (for MicroPython)
- **Workspace Settings**: Don't commit `.vscode/settings.json` with credentials
- **Extensions**: Be cautious with extensions that might auto-commit files

## Network Security

### WiFi Security Considerations

```cpp
// ESP32 WiFi security practices
WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

// Security considerations:
// 1. Use WPA2/WPA3 networks (never open WiFi)
// 2. Consider MAC address filtering for high-security environments  
// 3. Use guest networks to isolate IoT devices
// 4. Monitor for deauthentication attacks
```

### HTTPS/TLS Security

#### Arduino Implementation (Successful)
```cpp
HTTPClient http;
http.begin("https://api.lifx.com/v1/lights/all");  // Automatic certificate validation
// Arduino HTTPClient handles:
// - Certificate chain validation
// - TLS 1.3 support  
// - Modern cipher suites
// - Proper hostname verification
```

#### MicroPython Issues (Failed)
```python
# MicroPython SSL limitations encountered:
response = urequests.get("https://api.lifx.com/v1/lights/all")
# Error -202: SSL handshake failed
# Root cause: Limited SSL/TLS implementation
```

**Security Insight**: Platform selection significantly impacts security capabilities. Arduino provided more mature HTTPS implementation than MicroPython.

## Physical Security

### Device Security Considerations

1. **Firmware Protection:**
   - ESP32 supports flash encryption (not implemented in this project)
   - Consider secure boot for high-security environments
   
2. **Physical Access:**
   - Serial console access allows credential extraction
   - Consider disabling serial output in production firmware
   - Physical button could be misused if device is accessible

3. **Network Segmentation:**
   - IoT devices should be on separate network segment
   - Firewall rules to limit internet access to required APIs only

## Threat Model

### Assets to Protect
1. **WiFi Credentials**: Network access
2. **LIFX API Token**: Light control access  
3. **Device Functionality**: Unauthorized light control

### Attack Vectors Considered
1. **Source Code Exposure**: Git repository with hardcoded secrets
2. **Network Sniffing**: Unencrypted API communications
3. **Physical Access**: Serial console credential extraction
4. **Man-in-the-Middle**: API traffic interception

### Mitigations Implemented
1. **Git-Ignored Secrets**: Prevents accidental credential commits
2. **HTTPS Communication**: Encrypts all API traffic
3. **Minimal Attack Surface**: Single-purpose device with limited functionality
4. **Template Files**: Guides users to proper credential management

## Security Lessons Learned

### What Worked Well
1. **Secrets Separation**: Git-ignore pattern prevented any credential leaks
2. **Multiple Security Audits**: Caught potential issues before commits
3. **HTTPS-Only**: Arduino's reliable SSL prevented network-based attacks
4. **Template Pattern**: Made secure setup easy for new users

### Areas for Improvement
1. **Serial Output**: Production firmware still logs some debug information
2. **Certificate Pinning**: Could implement LIFX API certificate pinning
3. **Token Rotation**: No automatic API token rotation mechanism
4. **Physical Security**: No tamper detection or secure enclosure

### MicroPython vs Arduino Security

| Aspect | MicroPython | Arduino |
|--------|-------------|---------|
| HTTPS Support | ❌ SSL Error -202 | ✅ Reliable HTTPClient |
| Certificate Validation | ❌ Limited | ✅ Automatic |
| Cipher Suite Support | ❌ Basic | ✅ Modern TLS 1.3 |
| Development Security | ✅ Good tooling | ✅ Good tooling |
| Credential Management | ✅ Same pattern | ✅ Same pattern |

**Key Insight**: Security capabilities vary significantly between embedded platforms. Always validate security requirements early in platform selection.

## Recommendations for Future Projects

### Credential Management
1. **Always use separate config files** for credentials
2. **Always git-ignore credential files** from day one
3. **Provide template files** for easy user setup
4. **Never hardcode secrets** even for testing
5. **Audit repository history** before making public

### API Security  
1. **Use HTTPS exclusively** for external API calls
2. **Implement proper error handling** without exposing sensitive details
3. **Consider API rate limiting** to prevent abuse
4. **Validate SSL/TLS capabilities** during platform selection
5. **Use minimal API permissions** (read-only when possible)

### Development Security
1. **Review all commits** for accidental credential inclusion
2. **Use security scanning tools** in CI/CD pipeline
3. **Separate development and production credentials**
4. **Document security assumptions** and threat model
5. **Regular security audits** especially before releases

### IoT-Specific Considerations
1. **Plan for device updates** and security patching
2. **Consider network segmentation** for IoT devices
3. **Implement physical security** appropriate to deployment environment
4. **Monitor for unusual network activity** from devices
5. **Design for graceful degradation** during security incidents

## Conclusion

Security in IoT projects requires consideration at every level: code, network, physical, and operational. The secrets separation pattern proved highly effective and should be adopted as standard practice for any IoT project involving credentials.

The platform selection decision had significant security implications - Arduino's mature HTTPS implementation provided security capabilities that MicroPython could not match, demonstrating that security requirements should drive platform selection rather than development convenience.

Most importantly, **security should be designed in from the beginning rather than added later**. The git-ignore patterns, template files, and credential separation architecture established from day one prevented any security incidents throughout the project lifecycle.