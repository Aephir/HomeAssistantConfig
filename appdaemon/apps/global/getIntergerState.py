import appdaemon.plugins.hass.hassapi as hass

# Call with argument "entity_id", e.g.:
# getIntegerState("sensor.lightlevel_bathroom_2").
# Returns an integer.

def getIntegerState(entity_id):
    try:
        return int(float(self.get_state(entity_id)))
    except ValueError:
        return 0
