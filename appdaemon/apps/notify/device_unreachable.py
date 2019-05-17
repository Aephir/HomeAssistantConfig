"""
Notify if device becomes unreachable (hopefully only when battery is dead).
"""

import appdaemon.plugins.hass.hassapi as hass

class Sensor(hass.Hass):


    def initialize(self):

        self.battery_levels = [
                'sensor.x_cube_1_bat',
                'sensor.x_door_1_bat',
                'sensor.x_door_2_bat',
                'sensor.x_door_3_bat',
                'sensor.x_motion_1_bat',
                'sensor.x_motion_2_bat',
                'sensor.x_motion_3_bat',
                'sensor.x_motion_4_bat',
                'sensor.x_motion_5_bat',
                'sensor.x_motion_6_bat',
                'sensor.x_motion_7_bat',
                'sensor.x_motion_8_bat',
                'sensor.x_motion_9_bat',
                'sensor.x_smoke_1_bat',
                'sensor.x_temphum_1_bat',
                'sensor.x_temphum_2_bat',
                'sensor.x_temphum_3_bat',
                'sensor.x_temphum_4_bat',
                'sensor.x_temphum_5_bat',
                'sensor.z_door_1_bat',
                'sensor.fibaro_heat_01_bat'
                ]

        self.battery_powered_devices = [
                'binary_sensor.cube_158d00028f7196',
                'binary_sensor.door_window_sensor_158d000234dc7b',
                'binary_sensor.door_window_sensor_158d00022b3b66',
                'binary_sensor.door_window_sensor_158d00022d0917',
                'binary_sensor.motion_sensor_158d000200d203',
                'binary_sensor.motion_sensor_158d000200d285',
                'binary_sensor.motion_sensor_158d000200e0c5',
                'binary_sensor.motion_sensor_158d000236a0d0',
                'binary_sensor.motion_sensor_158d000236a0f3',
                'binary_sensor.motion_sensor_158d000236a22f',
                'binary_sensor.motion_sensor_158d000236a116',
                'binary_sensor.motion_sensor_158d0001e0a8e1',
                'binary_sensor.motion_sensor_158d000200e0c5',
                'binary_sensor.smoke_sensor_158d0001bc49bd',
                'sensor.temperature_158d00022c66ff',
                'sensor.temperature_158d000245b4a2',
                'sensor.temperature_158d0002437897',
                'sensor.temperature_158d000243778b',
                'sensor.temperature_158d00027727eb',
                'binary_sensor.door_window_sensor_158d00022b3b66',
                'zwave.fibaro_system_fgt001_heat_controller'
                ]


        for entity in self.battery_powered_devices:
            self.listen_state(self.deviceDown, entity, new='unknown')
            self.listen_state(self.deviceDown, entity, new='unavailable')
            self.listen_state(self.deviceDown, entity, old='unknown')
            self.listen_state(self.deviceDown, entity, old='unavailable')


    def deviceDown(self, entity, attribute, old, new, kwargs):

        friendly_name   = self.friendly_name(entity)
        list_of_down    = []
        sensor          = self.battery_levels[self.battery_powered_devices.index(entity)]
        last_battery    = self.get_state(sensor)
        title           = 'Battery powered devices offline!!'
        message         = 'Device "' + friendly_name + '" just went offline.\nCheck battery and connection.\n\nLast reported battery state was: ' + last_battery

        for i in self.battery_powered_devices:
            if self.get_state(i) == 'unknown' or self.get_state(i) == 'unavailable':
                list_of_down.append(i)

        if list_of_down:
            self.set_state('sensor.unavailable_devices', state = 'on', attributes = {'devices':list_of_down})
            self.call_service('notify/home_aephir_bot', title = title, message = message)
            self.log(message)
        else:
            self.set_state('sensor.unavailable_devices', state = 'off', attributes = {'devices':[]})
