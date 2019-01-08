"""
Warn me if the espresso machine is left "on" for more than 45 minutes.
Notify every 15 minutes.
After 1.5 hours, turn off and notify.
Set times is app config (apps.yaml)
"""

import appdaemon.plugins.hass.hassapi as hass
import datetime

class ApplianceStatus(hass.Hass):


    def initialize(self):
        """
        Initialize the timers and set listen_state
        """

        self.starttime = datetime.datetime.now()
        self.timer = None
        self.listen_state(self.StartTimer,"switch.switch")


    def StartTimer(self, entity, attribute, old, new, kwargs):
        """
        Cancel timer if entity is turned offself.
        Otherwise note the time, and start the loop (SendNotification)
        """

        if new == "off":
            if self.timer != None:
                self.cancel_timer(self.timer) # Cancels if switch state changes ('on' or 'off'), cancel so we're ready for new timer.

        else:
            if self.timer != None:
                self.cancel_timer(self.timer)

            self.starttime = datetime.datetime.now()
            self.timer = self.run_in(self.SendNotification,self.args["start_after"])


    def SendNotification(self, kwargs):
        """
        Cancel timer if entity is turned offself.
        Otherwise notify me about leaving the switch on every "time_between_notifications" secondsself.
        After "end_after" seconds, automatically turn off, and notify me.
        """

        delta = datetime.datetime.now() - self.starttime
        seconds = int(datetime.timedelta.total_seconds(delta))
        minutes = round(seconds/60)

        self.log(str(minutes) + " " + str(seconds)) # for troubleshooting

        if self.get_state('switch.switch') == 'off':
            if self.timer != None:
                self.cancel_timer(self.timer)

        elif seconds < self.args["end_after"]:

            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " minutes")
            if self.timer != None:
                self.cancel_timer(self.timer)
            self.run_in(self.SendNotification,self.args["time_between_notifications"])

        else:

            if self.args["switch_off"]:
                self.turn_off(self.args["entity"])
                switchofftext = ", i turned it off."
                self.turn_off('switch.switch')
            else:
                switchofftext = "."
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes" + switchofftext, data={"inline_keyboard":"Turn back on:/espresso_on, OK, thanks!:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " minutes" + switchoffftext,)
            self.cancel_timer(self.timer)
