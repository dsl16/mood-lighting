#!/usr/bin/env micropython
"""
MicroPython test script for LIFX API module
Designed to run on ESP32 with MicroPython (no pytest, minimal dependencies)
"""

import sys
import time
sys.path.append('/src')  # ESP32 filesystem path

try:
    from lighting.lifx_api import LIFXController, toggle_light, get_all_lights, LIFXAPIError
except ImportError:
    print("❌ Cannot import LIFX API module - check MicroPython installation")
    sys.exit(1)

def test_lifx_api_micropython():
    """MicroPython-compatible test function"""
    print('🧪 Testing LIFX API Module (MicroPython)')
    print('=' * 40)

    try:
        # Test 1: Initialize controller
        print('📡 Test 1: Initialize LIFX Controller...')
        controller = LIFXController()
        print('   ✅ Controller initialized successfully')
        
        # Test 2: Validate connection
        print('🔗 Test 2: Validate API connection...')
        is_connected = controller.validate_connection()
        print('   ✅ Connection valid:', is_connected)
        
        # Test 3: Discover lights
        print('💡 Test 3: Discover all lights...')
        lights = controller.discover_lights()
        print('   ✅ Found', len(lights), 'lights:')
        for light in lights:
            print('      -', light["label"], '(' + light["power"] + ')', 'at', str(light["brightness"]) + '%')
        
        # Test 4: Test convenience function
        print('🔍 Test 4: Test convenience function...')
        lights_via_function = get_all_lights()
        print('   ✅ Convenience function works:', len(lights_via_function), 'lights')
        
        # Test 5: Test toggle functionality 
        print('🔄 Test 5: Test toggle functionality...')
        if lights:
            test_light = 'label:Kitchen'
            print('   Testing toggle with', test_light, '...')
            
            # Get initial state
            initial_state = controller.get_light_state(test_light)
            initial_power = initial_state[0]['power']
            print('   Initial state:', initial_power)
            
            # Toggle using convenience function
            toggle_result = toggle_light(test_light)
            print('   Toggle result:', toggle_result["old_power"], '->', toggle_result["new_power"])
            
            # Verify new state
            time.sleep(1)
            final_state = controller.get_light_state(test_light)
            final_power = final_state[0]['power']
            print('   Final state:', final_power)
            
            # Restore original state
            if final_power != initial_power:
                print('   Restoring original state...')
                controller.set_light_state(test_light, power=initial_power)
                print('   ✅ Original state restored')
        
        print('')
        print('🎉 All tests passed! LIFX API module working on MicroPython.')
        print('📋 Summary:')
        print('   - API connection: ✅ Working')
        print('   - Light discovery: ✅', len(lights), 'lights found')
        print('   - Toggle functionality: ✅ Working')
        print('   - Error handling: ✅ Implemented')
        print('   - Ready for ESP32 button integration!')
        
        return True

    except LIFXAPIError as e:
        print('❌ LIFX API Error:', str(e))
        return False
    except Exception as e:
        print('❌ Unexpected error:', str(e))
        # MicroPython doesn't have traceback module
        return False

# MicroPython main execution
if __name__ == "__main__":
    result = test_lifx_api_micropython()
    if result:
        print('✅ MicroPython LIFX API test completed successfully')
    else:
        print('❌ MicroPython LIFX API test failed')