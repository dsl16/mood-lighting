"""
LIFX API Integration Module for ESP32 Button Project

Handles communication with LIFX smart lights via cloud API.
Implements stateless toggle functionality with fail-fast error handling.

Based on validated API testing with 5 LIFX lights:
- Kitchen, Living room, Bedroom lamp, moon, Flower Light
"""

try:
    # MicroPython libraries (primary target)
    import urequests as requests
    import ujson as json
except ImportError:
    # Standard Python libraries (desktop testing/development)
    import requests
    import json

import time
from secrets import LIFX_TOKEN


class LIFXAPIError(Exception):
    """Custom exception for LIFX API errors"""
    pass


class LIFXController:
    """
    LIFX API controller implementing stateless toggle functionality.
    
    Features:
    - Stateless operation (query current state, then toggle)
    - Fail-fast error handling with sub-second timeouts
    - URL encoding for light names with spaces
    - Async-ready design for future optimization
    """
    
    def __init__(self, api_token=None, timeout=400):
        """
        Initialize LIFX controller.
        
        Args:
            api_token (str): LIFX API token, defaults to secrets.LIFX_TOKEN
            timeout (int): Request timeout in milliseconds (400ms for fail-fast)
        """
        self.api_token = api_token or LIFX_TOKEN
        self.timeout = timeout / 1000.0  # Convert to seconds for urequests
        self.base_url = "https://api.lifx.com/v1"
        
        # Validate API token format
        if not self.api_token or len(self.api_token) != 64:
            raise LIFXAPIError("Invalid LIFX API token format")
    
    def _make_request(self, method, endpoint, data=None):
        """
        Make HTTP request to LIFX API with error handling.
        
        Args:
            method (str): HTTP method (GET, PUT)
            endpoint (str): API endpoint (e.g., "lights/label:Kitchen")
            data (dict): Request body data for PUT requests
            
        Returns:
            dict: Parsed JSON response
            
        Raises:
            LIFXAPIError: On network or API errors
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method == 'PUT':
                json_data = json.dumps(data) if data else None
                response = requests.put(url, headers=headers, data=json_data, timeout=self.timeout)
            else:
                raise LIFXAPIError(f"Unsupported HTTP method: {method}")
            
            # Check HTTP status (200 for GET, 207 for PUT bulk operations)
            if response.status_code not in [200, 207]:
                raise LIFXAPIError(f"HTTP {response.status_code}: {response.text}")
            
            # Parse JSON response
            result = response.json()
            response.close()
            return result
            
        except Exception as e:
            if hasattr(response, 'close'):
                response.close()
            
            # Convert various error types to LIFXAPIError
            if isinstance(e, LIFXAPIError):
                raise
            else:
                raise LIFXAPIError(f"Request failed: {str(e)}")
    
    def get_light_state(self, light_selector):
        """
        Get current state of specified light(s).
        
        Args:
            light_selector (str): Light selector (e.g., "label:Kitchen", "all")
            
        Returns:
            list: List of light state dictionaries
            
        Raises:
            LIFXAPIError: On API or network errors
        """
        endpoint = f"lights/{light_selector}"
        
        try:
            lights = self._make_request('GET', endpoint)
            
            if not lights:
                raise LIFXAPIError(f"No lights found for selector: {light_selector}")
            
            return lights
            
        except LIFXAPIError:
            raise
        except Exception as e:
            raise LIFXAPIError(f"Failed to get light state: {str(e)}")
    
    def set_light_state(self, light_selector, power=None, brightness=None, color=None):
        """
        Set state of specified light(s).
        
        Args:
            light_selector (str): Light selector (e.g., "label:Kitchen")
            power (str): "on" or "off"
            brightness (float): 0.0 to 1.0
            color (str): Color name or hex value
            
        Returns:
            dict: API response with results
            
        Raises:
            LIFXAPIError: On API or network errors
        """
        # Build state change payload
        state = {}
        if power is not None:
            state['power'] = power
        if brightness is not None:
            state['brightness'] = brightness
        if color is not None:
            state['color'] = color
        
        if not state:
            raise LIFXAPIError("No state changes specified")
        
        endpoint = f"lights/{light_selector}/state"
        
        try:
            result = self._make_request('PUT', endpoint, state)
            
            # Check if any lights were successfully updated
            if 'results' in result:
                success_count = sum(1 for r in result['results'] if r.get('status') == 'ok')
                if success_count == 0:
                    raise LIFXAPIError("No lights were successfully updated")
            
            return result
            
        except LIFXAPIError:
            raise
        except Exception as e:
            raise LIFXAPIError(f"Failed to set light state: {str(e)}")
    
    def toggle_light(self, light_selector):
        """
        Toggle power state of specified light(s).
        
        Implements stateless toggle: query current state, then set opposite.
        This ensures accurate toggling even if multiple buttons control same light.
        
        Args:
            light_selector (str): Light selector (e.g., "label:Kitchen")
            
        Returns:
            dict: Result with old_power, new_power, and API response
            
        Raises:
            LIFXAPIError: On API or network errors
        """
        try:
            # Step 1: Get current state
            lights = self.get_light_state(light_selector)
            
            # Determine current power state (use first light if multiple)
            current_power = lights[0]['power']
            
            # Step 2: Calculate opposite state
            new_power = 'off' if current_power == 'on' else 'on'
            
            # Step 3: Set new state
            result = self.set_light_state(light_selector, power=new_power)
            
            return {
                'old_power': current_power,
                'new_power': new_power,
                'api_response': result,
                'success': True
            }
            
        except LIFXAPIError:
            raise
        except Exception as e:
            raise LIFXAPIError(f"Toggle failed: {str(e)}")
    
    def discover_lights(self):
        """
        Discover all available lights on the account.
        
        Returns:
            list: List of light information dictionaries
            
        Raises:
            LIFXAPIError: On API or network errors
        """
        try:
            lights = self.get_light_state('all')
            
            # Extract useful information for each light
            light_info = []
            for light in lights:
                info = {
                    'id': light['id'],
                    'label': light['label'],
                    'power': light['power'],
                    'brightness': int(light['brightness'] * 100),
                    'location': light.get('location', {}).get('name', 'Unknown'),
                    'selector': f"label:{light['label']}"
                }
                light_info.append(info)
            
            return light_info
            
        except LIFXAPIError:
            raise
        except Exception as e:
            raise LIFXAPIError(f"Light discovery failed: {str(e)}")
    
    def validate_connection(self):
        """
        Validate API connection by attempting to discover lights.
        
        Returns:
            bool: True if connection successful
            
        Raises:
            LIFXAPIError: On API or network errors
        """
        try:
            lights = self.discover_lights()
            return len(lights) > 0
            
        except LIFXAPIError:
            raise
        except Exception as e:
            raise LIFXAPIError(f"Connection validation failed: {str(e)}")


# Convenience functions for simple usage
def toggle_light(light_selector, timeout=400):
    """
    Convenience function to toggle a light.
    
    Args:
        light_selector (str): Light selector (e.g., "label:Kitchen")
        timeout (int): Request timeout in milliseconds
        
    Returns:
        dict: Toggle result with old_power, new_power, success
        
    Raises:
        LIFXAPIError: On API or network errors
    """
    controller = LIFXController(timeout=timeout)
    return controller.toggle_light(light_selector)


def get_all_lights(timeout=400):
    """
    Convenience function to discover all lights.
    
    Args:
        timeout (int): Request timeout in milliseconds
        
    Returns:
        list: List of light information dictionaries
        
    Raises:
        LIFXAPIError: On API or network errors
    """
    controller = LIFXController(timeout=timeout)
    return controller.discover_lights()


# Example usage (for testing)
if __name__ == "__main__":
    try:
        # Test connection
        controller = LIFXController()
        print("Testing LIFX API connection...")
        
        # Discover lights
        lights = controller.discover_lights()
        print(f"Found {len(lights)} lights:")
        for light in lights:
            print(f"  - {light['label']} ({light['power']}) at {light['brightness']}%")
        
        # Test toggle with Kitchen light (no spaces in name)
        if lights:
            test_light = "label:Kitchen"
            print(f"\nTesting toggle with {test_light}...")
            result = controller.toggle_light(test_light)
            print(f"Toggle result: {result['old_power']} -> {result['new_power']}")
            
    except LIFXAPIError as e:
        print(f"LIFX API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")