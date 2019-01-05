# Turn off radiator if window is open. Saves state and if it was on, turns it back on when window closes.

import appdaemon.plugins.hass.hassapi as hass

class RadiatorThermostat(hass.Hass):

    def initialize(self):

        self.windowSensors = [
            'binary_sensor.door_window_sensor_158d0002286a78' # Bathroom window
            ]

        for entity in self.windowSensors:
            self.listen_state(self.toggleRadiator, entity)


    def toggleRadiator(self, entity, attribute, old, new, kwargs):

        radiatorState = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating') == 'heat'

        if new == 'on':
            radiatorState = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating') == 'heat'
            self.set_state('sensor.bathroom_heat_when_window_closes', state = radiatorState)
            self.call_service('climate/set_operation_mode', entity_id = "climate.fibaro_system_fgt001_heat_controller_heating", operation_mode = "off")
            self.call_service('zwave/refresh_node', node_id=7)

        elif new == 'off':
            if self.get_state('sensor.bathroom_heat_when_window_closes') == True:
                self.call_service('climate/set_operation_mode', entity_id = "climate.fibaro_system_fgt001_heat_controller_heating", operation_mode = "heat")
                self.call_service('zwave/refresh_node', node_id=7)