# import appdaemon.plugins.hass.hassapi as hass
# import datetime$

#Usage:
"""
Usage:

From other app where you want to use one of these functions:

    self.GlobalFunctions.testFunction()

    Define in app.yaml (or other .yaml file):

Alternately, add this one as an app in apps.yaml (or other .yaml file within appdaemon/apps/...)

global_function_app:
  module: global_functions
  class: GlobalFunctions

Then you can use from other app by:

    x = self.get_app("global_function_app")
    y = x.testFunction()

of course you need to add a class in the module.
then you can call it with
fnc = self.get_app("istimebetween")
test  = fnc.IsTimeBetween(start, end)
"""

# Do I need to import libraries here, or can I do that in whatever app I import these into.

class GlobalFunctions:

    def testFunction():
        return True

    def AreWeAwake(entity):
        if self.get_state(entity) == "on":
            return True

    def getIntegerState(entity_id):
        try:
            return int(float(self.get_state(entity_id)))
        except ValueError:
            return 0

    def triggeredEntity(self):
        return data.get('entity_id')

    def isOn(entity_id):
        return self.get_state(entity_id) == 'on'

    def stateIs(entity_id):
        if self.get_state(entity_id) == 'on':
            return "on"
        elif self.get_state(entity_id) == 'off':
            return "off"

    def workday():
        weekday = ''
        vacation = ''
        if datetime.date.weekday(today) < 5:
            weekday = "on"
        else:
            weekday = "off"
        if hass.get_state("input_boolean.vacation_mode") == "on":
            vacation = "on"
        else:
            vacation = "off"
        if weekday == "on" and vacation == "off":
            return True

    def isTimeBetween(first_time, second_time, compared_time = None):
        """
        Is this covered by native AppDaemon now_between??
        """
    #quick way to convert a time string to an integer. Expects a time string formatted 00:00:00 or 00:00 or None
        def split_time(t):
            if t != None:
                try:
                    ts = [ int(t) for t in t.split(':') ]
                except ValueError:
                    ts = [ 0, 0, 0 ]
            else:
                now = datetime.datetime.now()
                ts = [ now.hour, now.minute, now.second ]
            return sum([ t * convert for t, convert in zip(ts, [3600, 60, 0 ])])

        ct = split_time(compared_time)
        t1 = split_time(first_time)
        t2 = split_time(second_time)
        return t1 <= ct <= t2