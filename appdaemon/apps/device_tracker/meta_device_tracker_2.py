# Combine multiple device trackers into one entity
# You can call the script using the following:
# - service: python_script.meta_device_tracker
#   data_template:
#     entity_id: '{{trigger.entity_id}}'

# OPTIONS
# List the trackers for each individual
WaldenTrackers = ['device_tracker.google_maps_110730659630480268471', 'device_tracker.walden_cd926e1b047646b986d2f0c0c3e7d530',
                  'device_tracker.aephir_ping']
KristinaTrackers = ['device_tracker.kristinas_iphone', 'device_tracker.kristinabrody_612a3f1e8eae425e9cc514e48649cc46',
                'device_tracker.kristina_ping']
EmilieTrackers = ['device_tracker.emilie_aa172623f9cd406b9007dc08461d2c24', 'device_tracker.emilie_iphone_ping']
EmilieTrackers = ['device_tracker.niels_brodys_ipad_2', 'device_tracker.naia_ipad_ping']
# Get the entity that triggered the automation
triggeredEntity = data.get('entity_id')

# Set friendly name and the metatracker name based on the entity that triggered
if triggeredEntity in WaldenTrackers:
    newFriendlyName = 'Walden Tracker'
    newEntityPicture = '/local/images/aephir_v2.jpg'
    metatrackerName = 'device_tracker.meta_walden'
elif triggeredEntity in KristinaTrackers:
    newFriendlyName = 'Kristina Tracker'
    newEntityPicture = '/local/images/kristina_v2.jpg'
    metatrackerName = 'device_tracker.meta_kristina'
elif triggeredEntity in EmilieTrackers:
    newFriendlyName = 'Emilie Tracker'
    newEntityPicture = '/local/images/emilie.jpg'
    metatrackerName = 'device_tracker.meta_kristina'
else:
    newFriendlyName = None
    metatrackerName = None

# Get current & new state
newState = hass.states.get(triggeredEntity)
currentState = hass.states.get(metatrackerName)
# Get New data
newSource = newState.attributes.get('source_type')
newFriendlyName_temp = newState.attributes.get('friendly_name')

# If GPS source, set new coordinates
if newSource == 'gps':
    newLatitude = newState.attributes.get('latitude')
    newLongitude = newState.attributes.get('longitude')
    newgpsAccuracy = newState.attributes.get('gps_accuracy')
# If not, keep last known coordinates
elif currentState.attributes.get('latitude') is not None:
    newLatitude = currentState.attributes.get('latitude')
    newLongitude = currentState.attributes.get('longitude')
    newgpsAccuracy = currentState.attributes.get('gps_accuracy')
# Otherwise return null
else:
    newLatitude = None
    newLongitude = None
    newgpsAccuracy = None

# Get Battery
if newState.attributes.get('battery') is not None:
    newBattery = newState.attributes.get('battery')
elif currentState.attributes.get('battery') is not None:
    newBattery = currentState.attributes.get('battery')
else:
    newBattery = None

# Get velocity
if newState.attributes.get('velocity') is not None:
    newVelocity = newState.attributes.get('velocity')
elif currentState.attributes.get('velocity') is not None:
    newVelocity = currentState.attributes.get('velocity')
else:
    newVelocity = None

if newState.state is not None:
    newStatus = newState.state
else:
    newStatus = currentState.state

# Create device_tracker.meta entity
hass.states.set(metatrackerName, newStatus, {
    'friendly_name': newFriendlyName,
    'entity_picture': newEntityPicture,
    'source_type': newSource,
    'battery': newBattery,
    'gps_accuracy': newgpsAccuracy,
    'latitude': newLatitude,
    'longitude': newLongitude,
    'velocity': newVelocity,
    'update_source': triggeredEntity,
    'custom_ui_state_card': 'state-card-custom-ui',
    'show_last_changed': 'true'
})
