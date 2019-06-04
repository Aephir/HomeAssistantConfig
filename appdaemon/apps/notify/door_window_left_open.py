# Notify if we forget to close door/window if it is cold, windy, or there is high chance of significant amounth
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass


class Notify(hass.Hass):

    def initialize(self):

        # Door and window sensors to monitor.
        self.sensor_ids = [
            'binary_sensor.door_window_sensor_158d0002286a78', # Bathroom Window
            'binary_sensor.door_window_sensor_158d00022b3b66', # Basement Door
            'binary_sensor.door_window_sensor_158d00022d0917', # Front Door
            'binary_sensor.door_window_sensor_158d000234dc7b', # Conservatory Door
            'binary_sensor.neo_coolcam_doorwindow_detector_sensor' # Shed Door
            ]

        self.sensor_1 = 'binary_sensor.door_window_sensor_158d0002286a78', # Bathroom Window
        self.sensor_2 = 'binary_sensor.door_window_sensor_158d00022b3b66', # Basement Door
        self.sensor_3 = 'binary_sensor.door_window_sensor_158d00022d0917', # Front Door
        self.sensor_4 = 'binary_sensor.door_window_sensor_158d000234dc7b', # Conservatory Door
        self.sensor_5 = 'binary_sensor.neo_coolcam_doorwindow_detector_sensor' # Shed Door

        # Temperature, precipitation and wind conditions to monitor.
        self.weather_ids = [
            'sensor.dark_sky_temperature', # Monitor temperature drops.
            'sensor.dark_sky_precip', # Monitor procipitation type.
            'sensor.dark_sky_wind_speed' # Monitor wind speed.
            ]

        # Set this to "False" initially.
        self.open_1 = False # Need one for each door/window sensor.
        self.open_2 = False
        self.open_3 = False
        self.open_4 = False
        self.open_5 = False

        self.listOfOpen = [
            self.open_1,
            self.open_2,
            self.open_3,
            self.open_4,
            self.open_5
            ]

        self.anyOpen = False

        self.timer_1 = None
        self.timer_2 = None
        self.timer_3 = None
        self.timer_4 = None
        self.timer_5 = None

        self.timers = [
            self.timer_1,
            self.timer_2,
            self.timer_3,
            self.timer_4,
            self.timer_5
            ]

        self.time_1 = None
        self.time_2 = None
        self.time_3 = None
        self.time_4 = None
        self.time_5 = None

        # Run when state changes.
        for entity_id in self.sensor_ids:
            self.listen_state(self.MessageDoorWindow, entity_id)

        # for entity_id in self.sensor_ids:
        #     self.listen_state(self.timerState, entity_id)

        for entity_id in self.weather_ids:
            self.listen_state(self.MessageWeather, entity_id)


    def cancelTimers(self):
        for entity_id in self.timers:
            if entity_id != None:
                self.cancel_timer(entity_id)



    def MessageDoorWindow(self, entity, attribute, old, new, kwargs):
        """
        Set to "False" if door/window closes. Otherwise, run function.
        """

        self.cancelTimers(self.timers)


        if new == 'off':
            if entity == 'binary_sensor.door_window_sensor_158d0002286a78':
                self.open_1 = False
            elif entity == 'binary_sensor.door_window_sensor_158d00022b3b66':
                self.open_2 = False
            elif entity == 'binary_sensor.door_window_sensor_158d00022d0917':
                self.open_3 = False
            elif entity == 'binary_sensor.door_window_sensor_158d000234dc7b':
                self.open_4 = False
            elif entity == 'binary_sensor.neo_coolcam_doorwindow_detector_sensor':
                self.open_5 = False
        else:
            if entity == 'binary_sensor.door_window_sensor_158d0002286a78':
                self.timer_1 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)
            elif entity == 'binary_sensor.door_window_sensor_158d00022b3b66':
                self.timer_2 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)
            elif entity == 'binary_sensor.door_window_sensor_158d00022d0917':
                self.timer_3 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)
            elif entity == 'binary_sensor.door_window_sensor_158d000234dc7b':
                self.timer_4 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)
            elif entity == 'binary_sensor.neo_coolcam_doorwindow_detector_sensor':
                self.timer_5 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)


    def MessageWeather(self, entity, attribute, old, new, kwargs):
        """

        """
        if any(self.listOfOpen):
            if entity == "sensor.dark_sky_temperature":
                if float(self.get_state("sensor.dark_sky_temperature")) < 18.0:
                    self.SendNoticationWeather(type="temperature")
            elif entity == "sensor.dark_sky_precip":
                if float(self.get_state("sensor.dark_sky_precip_intensity")) > 4.0 and float(self.get_state("sensor.dark_sky_precip_probability")) > 25.0:
                    self.SendNoticationWeather(type="precipitation")
            elif entity == "sensor.dark_sky_wind_speed":
                if float(self.get_state("sensor.dark_sky_wind_speed")) > 14.0:
                    self.SendNoticationWeather(entity, type="wind")

    def isOpen(self, entity_id):
        return self.get_state(entity_id) == 'on'

    def ListOfOpen(self):
        count = 0
        door_window_list = ''
        for entity_id in self.sensor_ids:
            if self.IsOpen(entity_id):
                door_window_list += entity_id
                count += 1
        door_window_list.replace("binary_sensor.door_window_sensor_158d0002286a78","bathroom window, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d00022b3b66","basement door, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d00022d0917","front door, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d000234dc7b","conservatory door, ")
        door_window_list.replace("binary_sensor.neo_coolcam_doorwindow_detector_sensor","shed door, ")
        door_window_list = door_window_list[:-2]
        if count == 1:
            door_window_list += " is"
        else:
            door_window_list += " are"
        if count != 0:
            return door_window_list
            self.log(door_window_list)
        else:
            return False


    def SendNoticationDoorWindow(self, entity, kwargs):

        # Variables to get from HASS sensors.
        outdoor_temp = float(self.get_state("sensor.dark_sky_temperature"))
        precip_type = self.get_state("sensor.dark_sky_precip")
        precip_intensity = float(self.get_state("sensor.dark_sky_precip_intensity"))
        precip_probability = float(self.get_state("sensor.dark_sky_precip_probability"))
        precip_problem = ''
        wind_speed = float(self.get_state("sensor.dark_sky_wind_speed"))
        door_window = ''

        # Define a new friendly name for the sensor that triggered. Can probably be done smarter.
        if entity == "binary_sensor.door_window_sensor_158d0002286a78":
            door_window = "bathroom window"
        elif entity == "binary_sensor.door_window_sensor_158d00022b3b66":
            door_window = "basement door"
        elif entity == "binary_sensor.door_window_sensor_158d00022d0917":
            door_window = "front door"
        elif entity == "binary_sensor.door_window_sensor_158d000234dc7b":
            door_window = "conservatory door"
        elif entity == "binary_sensor.neo_coolcam_doorwindow_detector_sensor":
            door_window = "shed door"

        # If any type of precipitation is expected, make "True".
        if precip_type != "unknown" and precip_intensity > 4.0 and precip_probability > 25.0:
            precip_problem = True

        self.timer_1 = self.run_in(self.SendNoticationDoorWindow, 900, entity=entity)

        # Notify based on which sensor and what potential problem.
        if precip_problem:
            self.call_service("notify/home_aephir_bot", message="It might " + precip_type + ", and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It might " precip_type ", and the " + door_window + "has been open for 15 minutes. Please close it!")
            self.log("It might " + precip_type + ", and the " + door_window + "has been open for 15 minutes. Please close it!")
        elif outdoor_temp < 18.0: # Temperature 18°C. Is this appropriate?
            self.call_service("notify/home_aephir_bot", message="It is cold, and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It is cold, and the " + door_window + "has been open for 15 minutes. Please close it!")
            self.log("It is cold, and the " + door_window + "has been open for 15 minutes. Please close it!")
        elif wind_speed > 14.0: # Wind speed 14 m/s. Is this appropriate?
            self.call_service("notify/home_aephir_bot", message="It is windy, and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It is windy, and the " + door_window + "has been open for 15 minutes. Please close it!")
            self.log("It is windy, and the " + door_window + "has been open for 15 minutes. Please close it!")


    def SendNoticationWeather(self, entity, type):

        # Variables to get from HASS sensors.
        precip_type = self.get_state("sensor.dark_sky_precip")
        precip_problem = ''
        wind_speed = float(self.get_state("sensor.dark_sky_wind_speed"))
        door_window_list = self.ListOfOpen()

        # Define a new friendly name for the sensor that triggered.
        if door_window_list != False:
            if type == "temperature":
                self.call_service("notify/home_aephir_bot", message="It is getting cold outside, and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It is getting cold outside, and the " + door_window_list + " still open.")
                self.log("It is getting cold outside, and the " + door_window_list + " still open.")
            elif type == "precipitation":
                self.call_service("notify/home_aephir_bot", message="It might start to" + precip_type + ", and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It might start to" precip_type ", and the " + door_window_list + " still open.")
                self.log("It might start to" + precip_type + ", and the " + door_window_list + " still open.")
            elif type == "wind":
                self.call_service("notify/home_aephir_bot", message="It it getting windy, and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It it getting windy, and the " + door_window_list + " still open.")
                self.log("It it getting windy, and the " + door_window_list + " still open.")
