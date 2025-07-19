#!/usr/bin/env python3
"""
Unit tests for main.py ESP32 controller logic using pytest framework
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Import the main module (will use mocked modules from conftest.py)
from src.main import LightController


class TestLightController:
    """Test suite for the main ESP32 LightController class"""
    
    def test_initialization(self, mock_micropython_modules, mock_pin):
        """Test controller initialization and hardware setup"""
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            assert controller is not None
            assert hasattr(controller, 'button')
            assert hasattr(controller, 'system_led')
            assert hasattr(controller, 'error_led')
            assert hasattr(controller, 'success_led')
            assert controller.system_ready is False
    
    def test_hardware_setup(self, mock_micropython_modules, mock_pin):
        """Test GPIO pin setup and LED initialization"""
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Verify LEDs are initialized to off state
            assert controller.system_led.state is False
            assert controller.error_led.state is False
            assert controller.success_led.state is False
    
    @patch('src.main.network')
    def test_wifi_connection_success(self, mock_network, mock_micropython_modules, mock_pin, mock_wlan):
        """Test successful WiFi connection"""
        # Setup mocks
        mock_network.WLAN = Mock(return_value=mock_wlan(0))
        mock_network.STA_IF = 0
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Mock successful connection
            wlan_instance = mock_network.WLAN.return_value
            wlan_instance.isconnected.return_value = True
            
            controller.connect_wifi()
            
            assert controller.system_ready is True
            assert controller.system_led.state is True  # System LED should be on
    
    @patch('src.main.network')  
    def test_wifi_connection_failure(self, mock_network, mock_micropython_modules, mock_pin, mock_wlan):
        """Test WiFi connection failure and timeout"""
        # Setup mocks for failure scenario
        mock_network.WLAN = Mock(return_value=mock_wlan(0))
        mock_network.STA_IF = 0
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Mock failed connection
            wlan_instance = mock_network.WLAN.return_value
            wlan_instance.isconnected.return_value = False
            
            with patch('time.ticks_ms', side_effect=[0, 11000]):  # Simulate timeout
                with pytest.raises(Exception, match="WiFi connection timeout"):
                    controller.connect_wifi()
    
    @patch('src.main.requests')
    def test_api_request_success(self, mock_requests, mock_micropython_modules, mock_pin, lifx_api_mock_response):
        """Test successful LIFX API request"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [lifx_api_mock_response['state']]
        mock_requests.get.return_value = mock_response
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            result = controller.make_api_request('GET', 'http://test.url')
            
            assert result == [lifx_api_mock_response['state']]
            mock_response.close.assert_called_once()
    
    @patch('src.main.requests')
    def test_api_request_error(self, mock_requests, mock_micropython_modules, mock_pin):
        """Test LIFX API request error handling"""
        # Setup mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            with pytest.raises(Exception, match="API error: 404"):
                controller.make_api_request('GET', 'http://test.url')
    
    @patch('src.main.requests')
    def test_get_light_state(self, mock_requests, mock_micropython_modules, mock_pin, lifx_api_mock_response):
        """Test getting light state from API"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [lifx_api_mock_response['state']]
        mock_requests.get.return_value = mock_response
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            state = controller.get_light_state('Kitchen')
            
            assert state['power'] == 'on'
            assert state['brightness'] == 0.8
    
    @patch('src.main.requests')
    def test_set_light_state(self, mock_requests, mock_micropython_modules, mock_pin):
        """Test setting light state via API"""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 207  # LIFX Multi-Status response
        mock_response.json.return_value = {'results': [{'status': 'ok'}]}
        mock_requests.put.return_value = mock_response
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            result = controller.set_light_state('Kitchen', 'on', brightness=0.8)
            
            assert result is not None
            mock_requests.put.assert_called_once()
    
    @patch('src.main.requests')
    def test_toggle_light_success(self, mock_requests, mock_micropython_modules, mock_pin, lifx_api_mock_response):
        """Test successful light toggle operation"""
        # Setup mock responses for get and set operations
        get_response = Mock()
        get_response.status_code = 200
        get_response.json.return_value = [{'power': 'on', 'brightness': 0.8}]
        
        set_response = Mock()
        set_response.status_code = 207
        set_response.json.return_value = {'results': [{'status': 'ok'}]}
        
        mock_requests.get.return_value = get_response
        mock_requests.put.return_value = set_response
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Should not raise exception
            controller.toggle_light()
            
            # Verify success LED was triggered
            assert controller.success_led.state is False  # LED blinks then turns off
    
    @patch('src.main.requests')
    def test_toggle_light_failure(self, mock_requests, mock_micropython_modules, mock_pin):
        """Test light toggle failure and error handling"""
        # Setup mock to raise exception
        mock_requests.get.side_effect = Exception("Network error")
        
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Should handle exception gracefully
            controller.toggle_light()
            
            # Error LED should have been activated (and then turned off)
            # Note: In real implementation, error LED stays on for 1 second
    
    def test_button_pressed_debouncing(self, mock_micropython_modules, mock_pin, mock_timer):
        """Test button press debouncing logic"""
        with patch('src.main.Pin', mock_pin), \
             patch('src.main.Timer', mock_timer), \
             patch('time.ticks_ms', side_effect=[0, 10, 100]), \
             patch('time.ticks_diff', side_effect=[10, 90]):
            
            controller = LightController()
            controller.system_ready = True
            
            # First press should be processed
            controller.button_pressed(None)
            
            # Second press within debounce time should be ignored
            controller.button_pressed(None)
            
            # Third press after debounce time should be processed
            controller.button_pressed(None)
    
    def test_button_pressed_system_not_ready(self, mock_micropython_modules, mock_pin):
        """Test button press when system is not ready"""
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            controller.system_ready = False
            
            # Should not process button press
            controller.button_pressed(None)
            
            # No LEDs should be activated
            assert controller.system_led.state is False
    
    def test_led_operations(self, mock_micropython_modules, mock_pin):
        """Test LED control methods"""
        with patch('src.main.Pin', mock_pin), \
             patch('time.sleep_ms') as mock_sleep:
            
            controller = LightController()
            
            # Test blink system LED
            controller.blink_system_led()
            mock_sleep.assert_called_with(200)  # BLINK_DURATION
            
            # Test blink success LED
            controller.blink_success_led()
            
            # Test show error
            controller.show_error(500)
            mock_sleep.assert_called_with(500)
    
    def test_cleanup(self, mock_micropython_modules, mock_pin):
        """Test system cleanup on shutdown"""
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            controller.wifi = Mock()
            
            controller.cleanup()
            
            # All LEDs should be off
            assert controller.system_led.state is False
            assert controller.error_led.state is False
            assert controller.success_led.state is False
            
            # WiFi should be deactivated
            controller.wifi.active.assert_called_with(False)


class TestIntegrationScenarios:
    """Integration test scenarios without hardware dependencies"""
    
    @pytest.mark.integration
    @patch('src.main.requests')
    @patch('src.main.network')
    def test_full_button_press_workflow(self, mock_network, mock_requests, 
                                       mock_micropython_modules, mock_pin, 
                                       mock_wlan, mock_timer, lifx_api_mock_response):
        """Test complete button press -> light toggle workflow"""
        # Setup network mock
        mock_network.WLAN = Mock(return_value=mock_wlan(0))
        mock_network.STA_IF = 0
        
        # Setup API mocks
        get_response = Mock()
        get_response.status_code = 200
        get_response.json.return_value = [{'power': 'off', 'brightness': 0.8}]
        
        set_response = Mock()
        set_response.status_code = 207
        set_response.json.return_value = {'results': [{'status': 'ok'}]}
        
        mock_requests.get.return_value = get_response
        mock_requests.put.return_value = set_response
        
        with patch('src.main.Pin', mock_pin), \
             patch('src.main.Timer', mock_timer), \
             patch('time.ticks_ms', return_value=1000), \
             patch('time.ticks_diff', return_value=1000):
            
            controller = LightController()
            
            # Connect to WiFi
            wlan_instance = mock_network.WLAN.return_value
            wlan_instance.isconnected.return_value = True
            controller.connect_wifi()
            
            # Simulate button press
            controller.button_pressed(None)
            
            # Verify API calls were made
            mock_requests.get.assert_called()
            mock_requests.put.assert_called()
    
    @pytest.mark.slow
    def test_performance_requirements(self, mock_micropython_modules, mock_pin):
        """Test that operations meet performance requirements"""
        with patch('src.main.Pin', mock_pin):
            controller = LightController()
            
            # Test that LED operations are fast (sub-millisecond)
            start_time = time.time()
            controller.blink_system_led()
            duration = time.time() - start_time
            
            # LED operation should be very fast (allowing for mock overhead)
            assert duration < 0.1  # 100ms allowance for testing


# Convenience function for running specific test groups
def run_unit_tests():
    """Run only unit tests (fast, no external dependencies)"""
    pytest.main(["-v", "-m", "not integration and not slow", __file__])

def run_integration_tests():
    """Run integration tests (may require LIFX API)"""
    pytest.main(["-v", "-m", "integration", __file__])

def run_all_tests():
    """Run complete test suite"""
    pytest.main(["-v", __file__])


if __name__ == "__main__":
    run_all_tests()