"""
Update radiator thermostat states when doors or windows open or close
"""

import appdaemon.plugins.hass.hassapi as hass

class RadiatorThermostat(hass.Hass):

    def initialize(self):

        self.radiatorThermostats = [
            'climate.fibaro_system_fgt001_heat_controller_heating' # Bathroom radiator thermostat
            ]

        # self.doors = [
        #     ''
        #     ]

        self.windows = [
            'binary_sensor.door_window_sensor_158d0002286a78' # Bathroom window
            ]

        for entity in self.windows:
            self.listen_state(self.updateState, entity)

        # for entity in self.doors:
        #     self.listen_state(self.updateState, entity)

    def updateState(self, entity, attribute, old, new, kwargs):

        self.call_service('zwave/refresh_entity', entity_id = "zwave.fibaro_system_fgt001_heat_controller")
