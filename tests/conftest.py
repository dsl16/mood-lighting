"""
pytest configuration and shared fixtures for mood-lighting tests
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add src to Python path for imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

@pytest.fixture
def mock_micropython_modules():
    """Mock MicroPython-specific modules for desktop testing"""
    # Mock machine module
    machine_mock = Mock()
    machine_mock.Pin = Mock()
    machine_mock.Timer = Mock()
    machine_mock.Pin.IN = 0
    machine_mock.Pin.OUT = 1
    machine_mock.Pin.PULL_UP = 1
    machine_mock.Pin.IRQ_FALLING = 1
    machine_mock.Timer.ONE_SHOT = 0
    
    # Mock network module
    network_mock = Mock()
    network_mock.WLAN = Mock()
    network_mock.STA_IF = 0
    
    # Mock gc module
    gc_mock = Mock()
    gc_mock.collect = Mock()
    
    # Apply mocks to sys.modules
    sys.modules['machine'] = machine_mock
    sys.modules['network'] = network_mock
    sys.modules['gc'] = gc_mock
    
    yield {
        'machine': machine_mock,
        'network': network_mock,
        'gc': gc_mock
    }
    
    # Cleanup
    for module in ['machine', 'network', 'gc']:
        if module in sys.modules:
            del sys.modules[module]

@pytest.fixture
def mock_pin():
    """Mock GPIO Pin for hardware testing"""
    class MockPin:
        IN = 0
        OUT = 1
        PULL_UP = 1
        IRQ_FALLING = 1
        
        def __init__(self, pin, mode, pull=None):
            self.pin = pin
            self.mode = mode
            self.pull = pull
            self.state = False
            self.irq_handler = None
        
        def on(self):
            self.state = True
        
        def off(self):
            self.state = False
        
        def irq(self, trigger, handler):
            self.irq_handler = handler
        
        def simulate_press(self):
            if self.irq_handler:
                self.irq_handler(self)
    
    return MockPin

@pytest.fixture
def mock_wlan():
    """Mock WiFi WLAN for network testing"""
    class MockWLAN:
        STA_IF = 0
        
        def __init__(self, interface):
            self.interface = interface
            self.connected = False
            self.active_state = False
        
        def active(self, state=None):
            if state is not None:
                self.active_state = state
            return self.active_state
        
        def connect(self, ssid, password):
            self.connected = True
        
        def isconnected(self):
            return self.connected
        
        def ifconfig(self):
            return ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
    
    return MockWLAN

@pytest.fixture
def mock_timer():
    """Mock Timer for scheduling testing"""
    class MockTimer:
        ONE_SHOT = 0
        
        def __init__(self, id):
            self.id = id
            self.callback = None
        
        def init(self, mode, period, callback):
            self.callback = callback
            # Execute immediately for testing
            if callback:
                callback(self)
    
    return MockTimer

@pytest.fixture
def lifx_api_mock_response():
    """Mock LIFX API response data"""
    return {
        'lights': [
            {
                'id': 'test-light-id',
                'label': 'Kitchen',
                'power': 'on',
                'brightness': 0.8,
                'color': {'hue': 0, 'saturation': 0, 'kelvin': 3500}
            }
        ],
        'state': {
            'power': 'on',
            'brightness': 0.8,
            'color': {'hue': 0, 'saturation': 0, 'kelvin': 3500}
        }
    }

@pytest.fixture
def sample_secrets():
    """Sample secrets for testing"""
    return {
        'WIFI_SSID': 'TestNetwork',
        'WIFI_PASSWORD': 'TestPassword123',
        'LIFX_TOKEN': 'a' * 64  # Valid length LIFX token format
    }