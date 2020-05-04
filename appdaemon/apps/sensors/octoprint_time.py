"""
Script to convert time elapsed/remaining of 3D print from seconds to HH:MM:SS
"""
import time
import hassapi as hass

class Octoprint(hass.Hass):

    def initialize(self):

        time_sensors    = [
        'sensor.prusa_i3_mk3s_time_elapsed',
        'sensor.prusa_i3_mk3s_time_remaining'
        ]
        
        for entity in time_sensors:
            self.listen_state(self.convert_time, entity)

    def convert_time(self, entity, attribute, old, new, kwargs):

        new_entity  = 'sensor.prusa_i3_mk3s_time_' + entity.split('_')[-1] + '_format'
        new_time    = time.strftime('%H:%M:%S', time.gmtime(int(new)))
        self.set_state(new_entity, state = new_time)
