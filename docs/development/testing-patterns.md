# Testing Patterns and Strategies

## Overview

This document captures the testing architecture and patterns we developed for the ESP32 LIFX controller project. These patterns are valuable for any embedded/IoT Python project requiring hardware integration testing.

## Testing Architecture

### Test Organization Structure
```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configuration
├── test_main.py                   # Application orchestration tests
├── integration/
│   ├── __init__.py
│   └── test_lifx_scenarios.py     # End-to-end hardware tests
└── test_lighting/
    ├── __init__.py
    ├── test_lifx_api.py           # Desktop Python API tests
    └── test_lifx_api_micropython.py # MicroPython-specific tests
```

### Test Categories with Markers

```python
# pyproject.toml configuration
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests that don't require external resources",
    "integration: Integration tests that require LIFX API", 
    "hardware: Tests that require actual ESP32 hardware",
    "slow: Tests that take longer to run",
]
```

## Key Testing Patterns

### 1. Platform-Specific Testing

#### Dual Test Files Pattern
```python
# test_lifx_api.py - Desktop Python
import requests
import json

class TestLIFXAPI:
    def test_get_lights_desktop(self):
        # Uses full requests library
        response = requests.get(url, headers=headers)
        assert response.status_code == 200

# test_lifx_api_micropython.py - MicroPython 
import urequests as requests
import ujson as json

class TestLIFXAPIMicroPython:
    def test_get_lights_micropython(self):
        # Uses MicroPython-specific libraries
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
```

### 2. Hardware Abstraction Testing

#### Mock Hardware Pattern
```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_gpio():
    """Mock GPIO for testing without hardware"""
    mock_pin = Mock()
    mock_pin.value.return_value = 1
    return mock_pin

@pytest.fixture  
def mock_network():
    """Mock network calls for offline testing"""
    with patch('urequests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"label": "Kitchen", "power": "on"}
        ]
        yield mock_get
```

### 3. Integration Testing Strategy

#### Real Hardware Test Pattern
```python
# test_lifx_scenarios.py
@pytest.mark.integration
@pytest.mark.slow
class TestLIFXScenarios:
    """Integration tests with real LIFX API and hardware"""
    
    def test_button_press_toggles_light(self, real_esp32, real_lifx_api):
        # Test complete workflow with actual hardware
        initial_state = real_lifx_api.get_light_state("Kitchen")
        real_esp32.press_button()
        time.sleep(2)  # Wait for API call
        final_state = real_lifx_api.get_light_state("Kitchen") 
        assert initial_state["power"] != final_state["power"]
```

### 4. Mocking Strategies

#### Network Call Mocking
```python
def test_api_failure_handling(mock_network):
    """Test graceful handling of API failures"""
    mock_network.side_effect = requests.exceptions.Timeout()
    
    controller = LIFXController()
    result = controller.toggle_light("Kitchen")
    
    assert result is False
    # Verify error LED was activated
    assert controller.error_led.on.called
```

#### Time-Based Testing
```python
def test_button_debouncing(mock_time):
    """Test button debouncing logic"""
    mock_time.ticks_ms.side_effect = [0, 25, 100]  # Rapid then delayed
    
    controller = ButtonController()
    controller.button_pressed(None)  # First press
    controller.button_pressed(None)  # Too soon - should ignore
    controller.button_pressed(None)  # Valid press
    
    assert controller.press_count == 2  # Only valid presses counted
```

## Testing Infrastructure

### Fixtures for Embedded Testing

```python
# conftest.py - Comprehensive fixture setup
@pytest.fixture(scope="session")
def lifx_credentials():
    """Load real LIFX credentials for integration tests"""
    from project_secrets import LIFX_TOKEN
    return {"token": LIFX_TOKEN}

@pytest.fixture
def test_light_config():
    """Standard test light configuration"""
    return {
        "name": "Kitchen",
        "brightness": 0.8,
        "color": "warm_white"
    }

@pytest.fixture
def mock_esp32():
    """Mock ESP32 hardware components"""
    esp32 = Mock()
    esp32.wifi = Mock()
    esp32.button = Mock()
    esp32.led = Mock()
    return esp32
```

### Test Utilities

```python
# Test helpers for common operations
def assert_light_state(light_name, expected_power):
    """Helper to verify light state"""
    api = LIFXController()
    state = api.get_light_state(light_name)
    assert state["power"] == expected_power

def wait_for_api_response(timeout=5):
    """Helper to wait for async API calls"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if api_response_received():
            return True
        time.sleep(0.1)
    return False
```

## Test Environment Management

### Configuration for Different Environments

```python
# pytest.ini patterns for different test runs

# Unit tests only (no network/hardware)
pytest tests/ -m "unit"

# Integration tests with real API
pytest tests/ -m "integration" --lifx-token="real_token"

# Hardware tests with connected ESP32  
pytest tests/ -m "hardware" --esp32-port="/dev/tty.usbserial-0001"

# All tests except slow ones
pytest tests/ -m "not slow"
```

## Challenges and Solutions

### MicroPython Testing Issues

**Problem**: Different import paths and library behavior
```python
# Solution: Conditional imports in test files
try:
    import urequests as requests
    import ujson as json
    MICROPYTHON = True
except ImportError:
    import requests
    import json as json_lib
    MICROPYTHON = False
```

**Problem**: Limited mocking capabilities on device
```python
# Solution: Separate desktop and device test suites
# Run comprehensive mocks on desktop
# Run minimal integration tests on device
```

### Hardware Test Reliability

**Problem**: Physical button presses in automated tests
```python
# Solution: GPIO simulation
def simulate_button_press(gpio_pin):
    """Simulate hardware button press via GPIO control"""
    gpio_pin.value(0)  # Pull low
    time.sleep_ms(100)
    gpio_pin.value(1)  # Release
```

### Network-Dependent Tests

**Problem**: Tests failing due to network issues
```python
# Solution: Retry pattern with backoff
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_api_call():
    # Will retry up to 3 times with 2s delay
    pass
```

## Best Practices Learned

### 1. Test Organization
- **Separate unit and integration tests** clearly
- **Use descriptive test names** that explain the scenario
- **Group related tests** in classes with shared setup

### 2. Mock Strategy  
- **Mock at the boundary** (network calls, GPIO)
- **Don't mock what you don't own** (standard library)
- **Verify mocks are called correctly** (assert call counts/args)

### 3. Hardware Testing
- **Always have a fallback** for when hardware isn't available
- **Test both success and failure paths** 
- **Use timeouts** for any operation that might hang

### 4. CI/CD Considerations
- **Separate test suites** for different environments
- **Mark expensive tests** so they can be skipped
- **Provide clear test documentation** for setup requirements

## Reusable Test Templates

These patterns can be applied to any embedded Python project:

1. **Dual-platform testing** (desktop + embedded)
2. **Hardware abstraction mocking**
3. **Integration test organization**
4. **Network call simulation**
5. **Time-based operation testing**

The investment in testing infrastructure paid off during development by catching issues early and enabling confident refactoring.