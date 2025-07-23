# SSL/HTTPS Troubleshooting: MicroPython Issues

## Overview

This document details the SSL/HTTPS issues encountered with MicroPython on ESP32 when calling the LIFX Cloud API, and the troubleshooting steps that led to switching to Arduino.

## Problem Summary

**Issue**: MicroPython `urequests` consistently failed with SSL Error -202 when making HTTPS calls to `api.lifx.com`
**Impact**: Complete inability to communicate with LIFX Cloud API
**Resolution**: Switched to Arduino C++ with HTTPClient library

## Error Details

### Primary Error
```python
>>> import urequests
>>> response = urequests.get("https://api.lifx.com/v1/lights/all", 
...                          headers={"Authorization": "Bearer your_token_here"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "urequests.py", line 104, in _make_request
LIFXAPIError: Request failed: -202
```

### Additional Error Variations
```python
# Sometimes appeared as:
OSError: [Errno 118] EHOSTUNREACH

# Or connection timeouts:
OSError: [Errno 116] ETIMEDOUT
```

## Troubleshooting Steps Attempted

### 1. Network Connectivity Verification ✅
```python
# WiFi connection was stable
>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.isconnected()
True
>>> wlan.ifconfig()
('192.168.1.204', '255.255.255.0', '192.168.1.1', '192.168.1.1')

# Non-HTTPS requests worked fine
>>> urequests.get("http://httpbin.org/get")
<Response object at 0x3ffb1234>
```

### 2. API Endpoint Testing ✅
```bash
# Desktop curl worked perfectly
$ curl -H "Authorization: Bearer your_token_here" https://api.lifx.com/v1/lights/all
[{"id":"d3b2f1...","label":"Kitchen","power":"on",...}]
```

### 3. Certificate and SSL Configuration ❌
```python
# Attempted various SSL configurations
import ssl

# Try ignoring SSL verification (didn't work)
response = urequests.get(url, headers=headers, verify=False)  # No such parameter

# Try manual SSL context (limited options in MicroPython)
ssl_context = ssl.create_default_context()  # Not available in MicroPython
```

### 4. DNS Resolution Testing ✅
```python
# DNS worked correctly
>>> import socket
>>> socket.getaddrinfo("api.lifx.com", 443)
[(2, 1, 6, '', ('104.18.34.112', 443)), ...]
```

### 5. Alternative HTTP Libraries ❌
```python
# Limited options in MicroPython
# urequests is the primary/only HTTP client library
# No alternatives like httpx, aiohttp available
```

### 6. Firmware and Library Updates ❌
```python
# Tried different MicroPython versions
# ESP32 Generic v1.24.1 - Same issue
# Various urequests versions - Same issue
```

### 7. Network Configuration Changes ❌
```python
# Tried different networks
# Home WiFi - Failed with -202
# Mobile hotspot - Failed with -202
# Different ESP32 boards - Same issue across hardware
```

## Root Cause Analysis

### MicroPython SSL Implementation Issues

1. **Limited SSL/TLS Support**:
   - MicroPython's SSL implementation is minimal compared to desktop Python
   - Doesn't support all cipher suites that LIFX API requires
   - Certificate chain validation issues

2. **ESP32 Hardware Integration**:
   - MicroPython may not fully utilize ESP32's hardware SSL acceleration
   - Memory constraints affect SSL buffer sizes
   - Limited debugging information available

3. **Library Maturity**:
   - `urequests` is a simplified HTTP client
   - Lacks advanced SSL configuration options
   - Error reporting is minimal (just error codes)

### LIFX API Requirements

```bash
# LIFX API SSL certificate details
$ openssl s_client -connect api.lifx.com:443 -servername api.lifx.com
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    # Requires modern TLS support
```

**Requirements that MicroPython struggled with**:
- TLS 1.3 support
- Modern cipher suites
- Certificate chain validation
- SNI (Server Name Indication) support

## Working Solutions Attempted

### None - All MicroPython approaches failed

#### HTTP Relay Approach (Considered but not implemented)
```python
# Could have created HTTP-only relay server
# ESP32 -> HTTP -> Relay Server -> HTTPS -> LIFX API
# Decided against due to complexity and additional infrastructure
```

#### Local Network Protocol (Future consideration)
```python
# LIFX lights support local UDP protocol
# Could bypass HTTPS entirely
# Would require significant additional development
```

## Arduino Solution

### Why Arduino HTTPClient Succeeded

```cpp
// Arduino HTTPClient with same API endpoint
HTTPClient http;
http.begin("https://api.lifx.com/v1/lights/all");
http.addHeader("Authorization", "Bearer " + String(LIFX_TOKEN));
int httpCode = http.GET();  // Returns 200 consistently
```

**Success factors**:
1. **Mature SSL implementation** - Full TLS 1.3 support
2. **Hardware integration** - Proper use of ESP32 SSL acceleration  
3. **Certificate handling** - Automatic certificate chain validation
4. **Error reporting** - Clear HTTP status codes and debugging
5. **Memory management** - Efficient SSL buffer handling

## Lessons Learned

### MicroPython SSL Limitations

1. **Not suitable for production HTTPS** in current state
2. **Limited debugging capabilities** make troubleshooting difficult
3. **Certificate handling** is primitive compared to desktop Python
4. **Hardware acceleration** not fully utilized

### Platform Selection Criteria

For projects requiring HTTPS:
- **Arduino C++** - Proven reliable for production use
- **ESP-IDF** - More control but higher complexity
- **MicroPython** - Good for HTTP-only or local protocols

### Alternative Approaches

If forced to use MicroPython with HTTPS:
1. **HTTP proxy server** - Route through trusted relay
2. **Local protocols** - Avoid cloud APIs when possible  
3. **Hybrid architecture** - Arduino for networking, MicroPython for logic
4. **Regular testing** - MicroPython SSL support may improve

## Error Code Reference

| Error Code | Meaning | Likely Cause |
|------------|---------|--------------|
| -202 | SSL handshake failed | Certificate/cipher suite incompatibility |
| -118 | EHOSTUNREACH | Network routing issue (rare) |
| -116 | ETIMEDOUT | Connection timeout during SSL negotiation |

## Debugging Commands

```python
# Network connectivity
import network
wlan = network.WLAN(network.STA_IF)
print(wlan.isconnected(), wlan.ifconfig())

# DNS resolution  
import socket
print(socket.getaddrinfo("api.lifx.com", 443))

# Basic HTTP test (non-SSL)
import urequests
response = urequests.get("http://httpbin.org/status/200")
print(response.status_code)

# Memory check
import gc
gc.collect()
print(gc.mem_free())
```

## Conclusion

The SSL/HTTPS issues with MicroPython were ultimately unsolvable within the project timeline and requirements. The problem appears to be fundamental limitations in MicroPython's SSL implementation rather than configuration issues.

**Recommendation**: For any IoT project requiring reliable HTTPS communication, strongly consider Arduino C++ or ESP-IDF rather than MicroPython until its SSL support matures.

The 8+ hours spent troubleshooting these issues provided valuable learning about embedded SSL implementations and reinforced the importance of choosing the right platform for specific technical requirements.