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

        if new == 'on' and old == 'off':
            radiatorState = self.get_state('climate.fibaro_system_fgt001_heat_controller_heating')
            self.set_state('sensor.bathroom_heat_when_window_closes', state = radiatorState)
            if self.get_state('climate.fibaro_system_fgt001_heat_controller_heating') != 'off':
                self.call_service('climate/set_operation_mode', entity_id = "climate.fibaro_system_fgt001_heat_controller_heating", operation_mode = "off")

        elif new == 'off' and old == 'on':

            radiatorState = self.get_state('sensor.bathroom_heat_when_window_closes')

            if self.get_state('sensor.bathroom_heat_when_window_closes') == True:
                self.call_service('climate/set_operation_mode', entity_id = "climate.fibaro_system_fgt001_heat_controller_heating", operation_mode = radiatorState)
                self.log(radiatorState)
