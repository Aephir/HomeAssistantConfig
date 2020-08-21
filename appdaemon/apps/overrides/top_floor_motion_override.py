import hassapi as hass

class ManualOverride(hass.Hass):

    def initialize(self):

        self.timer = None
        self.listen_state(motion_lights_disabled,self.args["input"])

    def motion_lights_disabled(self, entity, attribute, old, new, kwargs):

        self.cancel_timer(self.timer)
        self.turn_off(self.args["boolean"])
        self.timer = self.run_in(self.turn_on(self.args["boolean"]), new)
