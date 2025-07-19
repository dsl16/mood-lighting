#!/usr/bin/env python3
"""
Fun LIFX API Test Script - Colorful Multi-Light Controls
Demonstrates advanced LIFX functionality with colors and scenes
"""

import sys
import time
import random
sys.path.append('src')

from lighting.lifx_api import LIFXController, LIFXAPIError

class ColorfulLightShow:
    """Fun light controller for colorful demonstrations"""
    
    def __init__(self):
        self.controller = LIFXController(timeout=5000)
        self.lights = []
        self.original_states = {}
    
    def discover_and_save_state(self):
        """Discover lights and save their original states"""
        print('🔍 Discovering lights and saving current state...')
        self.lights = self.controller.discover_lights()
        
        for light in self.lights:
            # Get detailed state for restoration later
            state = self.controller.get_light_state(light['selector'])
            self.original_states[light['label']] = {
                'power': state[0]['power'],
                'brightness': state[0]['brightness'],
                'color': state[0].get('color', {})
            }
        
        print(f'   ✅ Found {len(self.lights)} lights:')
        for light in self.lights:
            print(f'      - {light["label"]} ({light["power"]}) at {light["brightness"]}%')
    
    def rainbow_sequence(self):
        """Create a rainbow sequence across all 5 lights"""
        print('\n🌈 Starting Rainbow Sequence across all lights...')
        
        # Perfect for 5 lights - full rainbow spectrum
        rainbow_colors = [
            {'color': 'red', 'brightness': 0.8, 'emoji': '🔴'},      # Kitchen
            {'color': 'orange', 'brightness': 0.8, 'emoji': '🟠'},   # Living room  
            {'color': 'yellow', 'brightness': 0.8, 'emoji': '🟡'},   # Bedroom lamp
            {'color': 'green', 'brightness': 0.8, 'emoji': '🟢'},    # moon
            {'color': 'blue', 'brightness': 0.8, 'emoji': '🔵'}      # Flower Light
        ]
        
        print(f'   Creating rainbow with {len(self.lights)} lights...')
        
        for i, light in enumerate(self.lights):
            if i < len(rainbow_colors):
                color_info = rainbow_colors[i]
                print(f'   {color_info["emoji"]} {light["label"]} -> {color_info["color"]}')
                try:
                    self.controller.set_light_state(
                        light['selector'],
                        power='on',
                        brightness=color_info['brightness'],
                        color=color_info['color']
                    )
                    time.sleep(0.8)  # Slower for dramatic effect
                except LIFXAPIError as e:
                    print(f'      ❌ Failed: {e}')
        
        print('   ✅ Rainbow sequence complete! 🌈')
    
    def party_mode(self):
        """Cycle through random colors on all lights"""
        print('\n🎉 Starting Party Mode (10 seconds)...')
        
        party_colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'pink', 'white']
        
        for round_num in range(5):  # 5 rounds of color changes
            print(f'   🕺 Party round {round_num + 1}/5...')
            
            for light in self.lights:
                color = random.choice(party_colors)
                brightness = random.uniform(0.3, 1.0)
                
                try:
                    self.controller.set_light_state(
                        light['selector'],
                        power='on',
                        brightness=brightness,
                        color=color
                    )
                except LIFXAPIError as e:
                    print(f'      ❌ {light["label"]} failed: {e}')
            
            time.sleep(2)  # Hold colors for 2 seconds
        
        print('   ✅ Party mode complete!')
    
    def sunset_scene(self):
        """Create a warm sunset scene across all lights"""
        print('\n🌅 Creating Sunset Scene (warm cozy vibes)...')
        
        # Warm sunset colors mapped to your specific lights
        sunset_settings = [
            {'color': 'orange', 'brightness': 0.7, 'desc': 'warm cooking glow'},    # Kitchen
            {'color': 'red', 'brightness': 0.5, 'desc': 'cozy living ambiance'},    # Living room
            {'color': 'yellow', 'brightness': 0.4, 'desc': 'soft bedtime light'},   # Bedroom lamp
            {'color': 'orange', 'brightness': 0.6, 'desc': 'ambient moon glow'},    # moon
            {'color': 'red', 'brightness': 0.3, 'desc': 'romantic flower accent'}   # Flower Light
        ]
        
        print('   Setting each light for perfect sunset atmosphere...')
        
        for i, light in enumerate(self.lights):
            if i < len(sunset_settings):
                setting = sunset_settings[i]
                print(f'   🌇 {light["label"]} -> {setting["color"]} ({setting["desc"]})')
                
                try:
                    self.controller.set_light_state(
                        light['selector'],
                        power='on',
                        brightness=setting['brightness'],
                        color=setting['color']
                    )
                    time.sleep(0.5)  # Gentle progression
                except LIFXAPIError as e:
                    print(f'      ❌ Failed: {e}')
        
        print('   ✅ Sunset scene complete! Perfect for relaxing evening 🌇')
    
    def cool_focus_scene(self):
        """Create a cool blue/white focus scene"""
        print('\n💙 Creating Cool Focus Scene...')
        
        focus_settings = [
            {'color': 'white', 'brightness': 0.9},   # Kitchen - bright work light
            {'color': 'blue', 'brightness': 0.7},    # Living room - focus ambiance
            {'color': 'cyan', 'brightness': 0.8},    # Bedroom - cool reading light  
            {'color': 'white', 'brightness': 0.6},   # Moon - clean accent
            {'color': 'blue', 'brightness': 0.5}     # Flower Light - subtle accent
        ]
        
        for i, light in enumerate(self.lights):
            if i < len(focus_settings):
                setting = focus_settings[i]
                print(f'   ❄️  {light["label"]} -> {setting["color"]} at {int(setting["brightness"]*100)}%')
                
                try:
                    self.controller.set_light_state(
                        light['selector'],
                        power='on',
                        brightness=setting['brightness'],
                        color=setting['color']
                    )
                    time.sleep(0.3)
                except LIFXAPIError as e:
                    print(f'      ❌ Failed: {e}')
        
        print('   ✅ Cool focus scene set!')
    
    def restore_original_state(self):
        """Restore all lights to their original states"""
        print('\n🔄 Restoring original light states...')
        
        for light in self.lights:
            original = self.original_states.get(light['label'])
            if original:
                print(f'   ↩️  Restoring {light["label"]} to {original["power"]}...')
                
                try:
                    # Restore power and brightness
                    self.controller.set_light_state(
                        light['selector'],
                        power=original['power'],
                        brightness=original['brightness']
                    )
                    time.sleep(0.2)
                except LIFXAPIError as e:
                    print(f'      ❌ Failed to restore {light["label"]}: {e}')
        
        print('   ✅ Original states restored!')
    
    def run_all_scenarios(self):
        """Run all light scenarios automatically without user input"""
        print('\n🎛️  Running All Light Scenarios Automatically')
        print('=' * 50)
        
        scenarios = [
            ('🌈 Rainbow Sequence', self.rainbow_sequence),
            ('🎉 Party Mode', self.party_mode), 
            ('🌅 Sunset Scene', self.sunset_scene),
            ('💙 Cool Focus Scene', self.cool_focus_scene)
        ]
        
        for scenario_name, scenario_func in scenarios:
            print(f'\n🚀 Starting: {scenario_name}')
            try:
                scenario_func()
                print(f'   ✅ {scenario_name} completed successfully')
                time.sleep(3)  # Brief pause between scenarios
            except Exception as e:
                print(f'   ❌ {scenario_name} failed: {e}')
                continue
        
        print('\n🔄 Restoring original state...')
        self.restore_original_state()
        print('\n✅ All scenarios completed!')

def main():
    print('🎨 LIFX Fun Light Show Controller')
    print('=' * 50)
    
    try:
        light_show = ColorfulLightShow()
        light_show.discover_and_save_state()
        
        if not light_show.lights:
            print('❌ No lights found! Check LIFX API connection.')
            return
        
        print('\n🚀 Ready for colorful light control!')
        light_show.run_all_scenarios()
        
    except LIFXAPIError as e:
        print(f'❌ LIFX API Error: {e}')
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()