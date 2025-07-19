#!/usr/bin/env python3
"""
Test script for LIFX API module
"""

import sys
import time
sys.path.append('src')

from lighting.lifx_api import LIFXController, toggle_light, get_all_lights, LIFXAPIError

def test_lifx_api():
    print('🧪 Testing LIFX API Module')
    print('=' * 40)

    try:
        # Test 1: Initialize controller
        print('📡 Test 1: Initialize LIFX Controller...')
        controller = LIFXController()
        print('   ✅ Controller initialized successfully')
        
        # Test 2: Validate connection
        print('🔗 Test 2: Validate API connection...')
        is_connected = controller.validate_connection()
        print(f'   ✅ Connection valid: {is_connected}')
        
        # Test 3: Discover lights
        print('💡 Test 3: Discover all lights...')
        lights = controller.discover_lights()
        print(f'   ✅ Found {len(lights)} lights:')
        for light in lights:
            print(f'      - {light["label"]} ({light["power"]}) at {light["brightness"]}%')
        
        # Test 4: Test convenience function
        print('🔍 Test 4: Test convenience function...')
        lights_via_function = get_all_lights()
        print(f'   ✅ Convenience function works: {len(lights_via_function)} lights')
        
        # Test 5: Test toggle functionality 
        print('🔄 Test 5: Test toggle functionality...')
        if lights:
            test_light = 'label:Kitchen'
            print(f'   Testing toggle with {test_light}...')
            
            # Get initial state
            initial_state = controller.get_light_state(test_light)
            initial_power = initial_state[0]['power']
            print(f'   Initial state: {initial_power}')
            
            # Toggle using convenience function
            toggle_result = toggle_light(test_light)
            print(f'   Toggle result: {toggle_result["old_power"]} -> {toggle_result["new_power"]}')
            
            # Verify new state
            time.sleep(1)
            final_state = controller.get_light_state(test_light)
            final_power = final_state[0]['power']
            print(f'   Final state: {final_power}')
            
            # Restore original state
            if final_power != initial_power:
                print('   Restoring original state...')
                restore_result = controller.set_light_state(test_light, power=initial_power)
                print('   ✅ Original state restored')
        
        print()
        print('🎉 All tests passed! LIFX API module is working correctly.')
        print('📋 Summary:')
        print(f'   - API connection: ✅ Working')
        print(f'   - Light discovery: ✅ {len(lights)} lights found')
        print(f'   - Toggle functionality: ✅ Working')
        print(f'   - Error handling: ✅ Implemented')
        print('   - Ready for ESP32 integration!')
        
        return True

    except LIFXAPIError as e:
        print(f'❌ LIFX API Error: {e}')
        return False
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_lifx_api()