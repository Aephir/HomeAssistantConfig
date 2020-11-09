import hassapi as hass

class Rhasspy(hass.Hass):

    def initialize(self):

        self.light      = {
            "all":"light.all_lights",
            "basement":"light.basement_lights",
            "bedroom":"light.bedroom",
            "conservatory":"light.conservatory_lights",
            "entrance":"light.entrance_lights",
            "kitchen":"light.kitchen_lights",
            "upstairs":"light.top_floor_lights",
            "top floor":"light.top_floor_lights",
            "dining room":"light.dining_room_lights",
            "tv room":"light.tv_room_lights",
            "baby room":"light.baby_room_lights",
            "main floor":"light.main_floor_lights"
        }

        self.color      = {
            "red":[255,0,0 ],
            "green":[0,128,0],
            "blue":[0,0,255],
            "yellow":[255,255,0],
            "purple":[128,0,128],
            "turquoise":[64,224,208],
            "warm white":454,   # color_temp = 2200K
            "cool white":250,   # color_temp = 4000K
            "white":370         # color_temp = 2700K
        }

        if 'event' in self.args:
            self.listen_event(self.change_light, self.args['event'])

    def change_light(self, event_name, data, kwargs):

        # Appademon logs:
        # self.log("Rhasspy", "\nevent_name: " + str(event_name), "\ndata: " + str(data), "\nkwrags: " + str(kwargs))
        # message: Rhasspy, args: ('\nevent_name: rhasspy_ChangeLightState', "\\data: {'_text': 'turn the kitchen lights up', '_raw_text': 'turn the kitchen lights up'}", "\\kwrags: {'__thread_id': 'thread-58'}")
        # event_name: rhasspy_ChangeLightState',
        # data: {'_text': 'turn the kitchen lights up', '_raw_text': 'turn the kitchen lights up'}"
        # kwrags: {'__thread_id': 'thread-58'}")

        self.log(data[_text])

        plurality:str       = ''
        action: str         = ''
        new_brightness:int  = None
        new_color           = None
        current_state:str   = None
        current_bright:str  = None
        type_bright:str     = ''
        type_color:str      = ''
        light:str           = ''
        entity:str          = ''

        if 'lights' in data[_text]:
            plurality = ' lights'
        else:
            plurality = ' light'


        if 'light' in data[_text]:
            text_temp   = data[_text].split(' light')[0].split(' ')
            if 'room' in data[_text] or 'floor' in data[_text:
                light   = text_temp[len(text_temp) - 2] + ' ' + text_temp[len(text_temp) - 1]
            else:
                light   = text_temp[len(text_temp) - 1]
        entity          = self.light[light]


        for color in self.color:
            if color in data[_text]:
                new_color = self.color[color]

        if type(new_color) == int:
            type_color = 'int'
        elif type(new_color) == str:
            type_color = 'str'


        if 'on' in data[_text]:
            action = 'on'
        elif 'off' in data[_text]:
            action = 'off'
        elif 'up' in data[_text]:
            action = 'up'
        elif any['down','dim'] in data[_text]:
            action = 'down'
        elif 'brightness' in data[_text]:
            action          = 'set_brightness'
            first:int       = self.find_first(data[_text)
            new_brightness  = data[_text]
            if 'percent' in data[_text]:
                new_brightness = round(new_brightness * 2.55)
        elif new_color != None:
            action = 'color'
        elif "maximum" in data[_text]: # E.g. set briughtness to 'maximum'. Other words??
            action = 'on'


        current_state:str       = self.get_state(entity)
        current_bright:int      = self.get_state(entity, attribute='brightness')
        current_color:int       = 0
        current_color_temp:list = []

        try:
            current_color = self.get_state(entity, attribute='rgb_color')
        except:
            current_color_temp = self.get_state(entity, attribute='color_temp')


        if action == 'off':
            self.turn_off(entity)
        elif action == 'on':
            self.turn_on(entity, brightness = 255)
        elif action == 'up': # turns up brightness by 50, unless above 206.
            if current_bright >= 205:
                new_brightness = 255
            else:
                new_brightness = current_bright + 50
            self.turn_on(entity, brightness = new_brightness)
        elif action == 'down': # turns down brightness by 50, unless below 51.
            if current_bright <= 50:
                new_brightness = 1
            else:
                new_brightness = current_bright - 50
            self.turn_on(entity, brightness = new_brightness)
        elif action == 'brightness': # Set specified brightness
            self.turn_on(entity, brightness = new_brightness)
        elif action == 'color':
            if type(new_color) == list:
                self.turn_on(entity, rgb_color = new_color) # If a color specified
            elif type(new_color) == int:
                self.turn_on(entity, color_temp = new_color) # If a color temperature (e.g. warm, cold) specified


    def find_first(self, text:str) -> int:

        digits:list[str]    = ['0','1','2','3','4','5','6','7','8','9']
        first:int           = 10000 # Bad programming! How to do better?

        for digit in digits:
            if text.find(digit) < first:
                first = text.find(digit)

        return first
