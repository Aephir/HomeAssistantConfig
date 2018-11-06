import appdaemon.plugins.hass.hassapi as hass

# UNTESTED!

# Call with:
# triggeredEntity()
# Returns entidi_id, e.g. binary_sensor.motion_sensor_158d000236a0d0

# Get Data from Automation Trigger
    def triggeredEntity(self):
        return data.get('entity_id')
