import appdaemon.plugins.hass.hassapi as hass
import datetime

# Call with argument "entity_id", e.g.:
# AreWekAwake(light.dining_room_lights)

    def AreWeAwake(entity):
        if self.get_state(entity) == "on":
            return True
