"""
Update radiator thermostat states
"""

import appdaemon.plugins.hass.hassapi as hass

class RadiatorThermostat(hass.Hass):

    def initialize(self):

        self.radiatorThermostats = [
            'climate.fibaro_system_fgt001_heat_controller_heating' # Bathroom radiator thermostat
            ]

        self.listen_event(self.updateState, event=call_service, domain=climate, service=set_temperature)
        self.listen_event(self.updateState, event=call_service, domain=climate, service=set_operation_mode)
        self.listen_event(self.updateState, event=call_service, domain=climate, service=turn_on)
        self.listen_event(self.updateState, event=call_service, domain=climate, service=turn_off)

        self.run_every(self.updateState, 1, 60)


    def updateState(self, entity, attribute, old, new, kwargs):

        # self.call_service('zwave/refresh_entity', entity_id = 'zwave.fibaro_system_fgt001_heat_controller')
        self.call_service('zwave/refresh_entity', entity_id = 'sensor.fibaro_system_fgt001_heat_controller_system')
        self.call_service('zwave/refresh_entity', entity_id = 'sensor.fibaro_system_fgt001_heat_controller_temperature')
        self.call_service('zwave/refresh_entity', entity_id = 'climate.fibaro_system_fgt001_heat_controller_heating')
