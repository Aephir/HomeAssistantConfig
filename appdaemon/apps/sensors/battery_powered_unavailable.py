import hassapi as hass

class Availability(hass.Hass):

    def initialize(self):

        self.make_sensor

        self.battery_powered_devices = self.args["devices"]
        self.unavailable = ['unavailable', 'unknown']

        for device in self.battery_powered_devices:
            self.listen_state(self.make_sensor, device, state='unavailable')

    def make_sensor(self, entity, attribute, old, new, kwargs):

        unavailable_devices = None
        unavailable_devices_list = []

        for device in self.battery_powered_devices:
            if self.get_state(device) in self.unavailable:
                unavailable_devices_list.append(device)

        if unavailable_devices_list != []:
            any_unavailable = 'on'

        self.set_state('sensor.unavailable_devices',
            state       = any_unavailable,
            attributes  = {'devices' : unavailable_devices_list})
