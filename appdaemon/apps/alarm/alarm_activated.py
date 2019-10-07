import appdaemon.plugins.hass.hassapi as hass
import time
from multiprocessing import Process


## Alarm triggered. Notify us, sound alarm tts, flash lights.

class AlarmTriggered(hass.Hass):

    # Initialize
    def initialize(self):
        self.listen_state(self.alarm_process,"alarm_control_panel.house")

    # Has the alarm been activated/triggered? Return True/False
    def alarmActivated(self, entity_id):
        if self.get_state("alarm_control_panel.house") == "triggered":
            return True

    # Which door was opened to trigger the alarm? Return the friendly_name
    def whichSensor(self):
        sensors = ['binary_sensor.presence_basement_entrance', 'binary_sensor.presence_conservatory', 'binary_sensor.presence_entrance']
        for s in sensors:
            if self.get_state(s) == "on":
                return self.friendly_name(s)

    # Flash the lights for 20 seconds if home, 180 seconds if not home.
    def alarm_light(self):
        lightsNoColor = ["light.kitchen_lights", "light.conservatory_lights", "light_stairway", "light.dining_table_2", "light.basement_entrance", "light.basement_hallway", "light_top_floor_bathroom"]
        lightsColor = ["light.bathroom", "light.dining_table_1", "light.tv_room", "light.lightstrip_1", "light.living_room_lightstrip"]
        t_end_home = time.time() + 20
        t_end_away = time.time() + 180

        if self.alarmActivated("alarm_control_panel.house"):
            if self.get_state("input_boolean.someonehome360") == "on":
                while time.time() < t_end_home:
                    for lnc in lightsNoColor:
                        self.turn_on(lnc,brightness=255,kelvin=4000,flash=short)
                    for lc in lightsColor:
                        self.turn_on(lc,brightness=255,rgb_color=[255,0,0],flash=short)
            elif self.get_state("input_boolean.someonehome360") == "off":
                while time.time() < t_end_away:
                    pass    for lnc in lightsNoColor:
                        self.turn_on(lnc,brightness=255,kelvin=4000,flash=short)
                    for lc in lightsColor:
                        self.turn_on(lc,brightness=255,rgb_color=[255,0,0],flash=short)

    # Voice notifications in house. Repeat for 180 seconds if not home.
    def alarm_tts(self):
        alarmMessage = 'The ' + whichSensor + ' triggered the alarm at ' + self.time() + '.'
        t_end_home = time.time() + 5
        t_end_away = time.time() + 180

        if self.alarmActivated("alarm_control_panel.house"):
            if self.get_state("input_boolean.someonehome360") == "on":
                self.call_service("media_player.volume_set", attributes = {"entity_id":"media_player.living_room_speaker","volume_level": "0.5"})
                while time.time() < t_end_home:
                    self.call_service("tts.google_say", attributes = {"entity_id":"media_player.living_room_speaker","message":"The alarm has been triggered"})
                    time.sleep(2)
            elif self.get_state("input_boolean.someonehome360") == "off":
                self.call_service("media_player.volume_set", attributes = {"entity_id":"media_player.living_room_speaker","volume_level": "1"})
                while time.time() < t_end_away:
                    self.call_service("tts.google_say", attributes = {"entity_id":"media_player.living_room_speaker","message":"The alarm has been triggered"})
                    time.sleep(2)
                    self.call_service("tts.google_say", attributes = {"entity_id":"media_player.living_room_speaker","message":"Video recordings have been saved offsite"})
                    time.sleep(2)
                    self.call_service("tts.google_say", attributes = {"entity_id":"media_player.living_room_speaker","message":"The police have been notified"})

    # Send (actionalble?) notifications to us.
    def alarm_notify(self):
        alarmMessage = 'The ' + whichSensor + ' triggered the alarm at ' + self.time() + '.'

        if self.alarmActivated("alarm_control_panel.house"):
            # self.call_service("telegram_bot.send_message", attributes = {"title":"Alarm Triggered", "message":"alarmMessage", "data":"keyboard{'/disarm, No action:/removekeyboard'}"})
            self.call_service("telegram_bot.send_message", attributes = {"title":"Alarm Triggered", "message":alarmMessage})
            self.call_service("notify.ios_kristinas_iphone", attributes = {"title":"Alarm Triggered", "message":alarmMessage})

    # Create multiprocessing, so each can run simultaneously.
    def alarm_process(self):
        p1 = Process(alarm_light())
        p2 = Process(alarm_tts())
        p3 = Process(alarm_notify())
        p1.start()
        p2.start()
        p3.start()
