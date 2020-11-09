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
                'binary_sensor.openclose_basement_entrance_door',
                'binary_sensor.openclose_front_door',
                'binary_sensor.presence_basement_entrance',
                'binary_sensor.presence_conservatory',
                'binary_sensor.presence_top_floor_stairway',
                'binary_sensor.presence_top_floor_bathroom',
                'binary_sensor.presence_top_floor_tv_room',
                'binary_sensor.presence_bathroom_2',
                'binary_sensor.presence_tv_room',
                'binary_sensor.presence_kitchen',
                'binary_sensor.presence_top_floor_stairway',
                'binary_sensor.smoke_sensor_158d0001bc49bd',
                'sensor.temperature_bathroom',
                'sensor.temperature_wine_cellar',
                'sensor.temperature_washing_room',
                'sensor.temperature_washing_room',
                'sensor.temperature_kitchen',
                'binary_sensor.openclose_basement_entrance_door',
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
        message         = 'Device "' + str(friendly_name) + '" just went offline.\nCheck battery and connection.\n\nLast reported battery state was: ' + str(last_battery)

        for i in self.battery_powered_devices:
            if self.get_state(i) == 'unknown' or self.get_state(i) == 'unavailable':
                list_of_down.append(i)

        if list_of_down:
            self.set_state('sensor.unavailable_devices', state = 'on', attributes = {'devices':list_of_down})
            self.call_service(self.args['notify'], title = title, message = message)
            self.log(message)
        else:
            self.set_state('sensor.unavailable_devices', state = 'off', attributes = {'devices':[]})
