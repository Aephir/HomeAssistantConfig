import appdaemon.plugins.hass.hassapi as hass

class your_class_name(hass.Hass):

  def initialize(self):
    self.listen_state(self.light_on,"input_boolean.naiahome360", new="on")
    self.listen_state(self.light_off,"input_boolean.naiahome360", new="off")

  def light_on (self, entity, attribute, old, new, kwargs):
    a_variabele_with_a_usable_name = self.get_state("device_tracker.walden_bjrn_yoshimoto")
    if a_variabele_with_a_usable_name == "home":
      self.turn_on(self.args["lightID"])

  def light_off (self, entity, attribute, old, new, kwargs):
    a_variabele_with_a_usable_name = self.get_state("device_tracker.walden_bjrn_yoshimoto")
    if a_variabele_with_a_usable_name == "home":
      self.turn_off(self.args["lightID"])

      # self.turn_off("light.conservatory_couch")
# self.turn_off(self.args["lightID"])
