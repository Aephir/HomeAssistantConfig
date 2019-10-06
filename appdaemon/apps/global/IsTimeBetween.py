import appdaemon.plugins.hass.hassapi as hass
import datetime

# Call with arguments times, the last could be current time:
# isTimeBetween(07:00, 22:00, 16:53)

#makes your time comparison, returns true/false.
def isTimeBetween(first_time, second_time, compared_time = None):
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
