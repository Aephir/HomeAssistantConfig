import hassapi as hass

class Sensor(hass.Hass):

    def initialize(self):

        self.timer = None

        if self.get_state('sensor.top_floor_bathroom_previous_humidity') == None:
            self.set_state('sensor.top_floor_bathroom_previous_humidity', state=self.get_state("sensor.humidity_top_bathroom"))

        self.listen_state(self.set_sensor, "sensor.humidity_top_bathroom")


    def set_sensor(self, entity, attribute, old, new, kwargs):

        self.timer = self.run_in(self.set_past_sensor, 600, state=new)

        if float(new) - float(self.get_state('sensor.top_floor_bathroom_previous_humidity')) > 8.0:
            self.set_state('binary_sensor.shower_on', state='on')
        else:
            self.set_state('binary_sensor.shower_on', state='off')


    def set_past_sensor(self, state):

        self.cancel_timer(self.timer)
        self.set_state('sensor.top_floor_bathroom_previous_humidity', state=state)
