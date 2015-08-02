import requests
from xml.etree import ElementTree
from xml.dom.minidom import parseString

"""
define {'TV_CMD_FAST_FORWARD': 36}
define ('TV_CMD_REWIND', 37);
define ('TV_CMD_SKIP_FORWARD', 38);
define ('TV_CMD_SKIP_BACKWARD', 39);
define ('TV_CMD_RECORD', 40);
define ('TV_CMD_RECORDING_LIST', 41);
define ('TV_CMD_REPEAT', 42);
define ('TV_CMD_LIVE_TV', 43);
define ('TV_CMD_EPG', 44);
define ('TV_CMD_PROGRAM_INFORMATION', 45);
define ('TV_CMD_ASPECT_RATIO', 46);
define ('TV_CMD_EXTERNAL_INPUT', 47);
define ('TV_CMD_PIP_SECONDARY_VIDEO', 48);
define ('TV_CMD_SHOW_SUBTITLE', 49);
define ('TV_CMD_PROGRAM_LIST', 50);
define ('TV_CMD_TELE_TEXT', 51);
define ('TV_CMD_MARK', 52);
define ('TV_CMD_3D_VIDEO', 400);
define ('TV_CMD_3D_LR', 401);
define ('TV_CMD_DASH', 402);
define ('TV_CMD_PREVIOUS_CHANNEL', 403);
define ('TV_CMD_FAVORITE_CHANNEL', 404);
define ('TV_CMD_QUICK_MENU', 405);
define ('TV_CMD_TEXT_OPTION', 406);
define ('TV_CMD_AUDIO_DESCRIPTION', 407);
define ('TV_CMD_ENERGY_SAVING', 409);
define ('TV_CMD_AV_MODE', 410);
define ('TV_CMD_SIMPLINK', 411);
define ('TV_CMD_EXIT', 412);
define ('TV_CMD_RESERVATION_PROGRAM_LIST', 413);
define ('TV_CMD_PIP_CHANNEL_UP', 414);
define ('TV_CMD_PIP_CHANNEL_DOWN', 415);
define ('TV_CMD_SWITCH_VIDEO', 416);
define ('TV_CMD_APPS', 417);
define ('TV_CMD_MOUSE_MOVE', 'HandleTouchMove');
define ('TV_CMD_MOUSE_CLICK', 'HandleTouchClick');
define ('TV_CMD_TOUCH_WHEEL', 'HandleTouchWheel');
define ('TV_CMD_CHANGE_CHANNEL', 'HandleChannelChange');
define ('TV_CMD_SCROLL_UP', 'up');
define ('TV_CMD_SCROLL_DOWN', 'down');
define ('TV_INFO_CURRENT_CHANNEL', 'cur_channel');
define ('TV_INFO_CHANNEL_LIST', 'channel_list');
define ('TV_INFO_CONTEXT_UI', 'context_ui');
define ('TV_INFO_VOLUME', 'volume_info');
define ('TV_INFO_SCREEN', 'screen_image');
define ('TV_INFO_3D', 'is_3d');
define ('TV_LAUNCH_APP', 'AppExecute');
"""


class LGSmartTV():
    TV_IP = None
    TV_PORT = 8080
    AUTH_KEY = None
    SESSION = None

    COMMANDS = {"TV_CMD_POWER": 1,
                "TV_CMD_NUMBER_0": 2,
                "TV_CMD_NUMBER_1": 3,
                "TV_CMD_NUMBER_2": 4,
                "TV_CMD_NUMBER_3": 5,
                "TV_CMD_NUMBER_4": 6,
                "TV_CMD_NUMBER_5": 7,
                "TV_CMD_NUMBER_6": 8,
                "TV_CMD_NUMBER_7": 9,
                "TV_CMD_NUMBER_8": 10,
                "TV_CMD_NUMBER_9": 11,
                "TV_CMD_UP": 12,
                "TV_CMD_DOWN": 13,
                "TV_CMD_LEFT": 14,
                "TV_CMD_RIGHT": 15,
                "TV_CMD_OK": 20,
                "TV_CMD_HOME_MENU": 21,
                "TV_CMD_BACK": 23,
                "TV_CMD_VOLUME_UP": 24,
                "TV_CMD_VOLUME_DOWN": 25,
                "TV_CMD_MUTE_TOGGLE": 26,
                "TV_CMD_CHANNEL_UP": 27,
                "TV_CMD_CHANNEL_DOWN": 28,
                "TV_CMD_BLUE": 29,
                "TV_CMD_GREEN": 30,
                "TV_CMD_RED": 31,
                "TV_CMD_YELLOW": 32,
                "TV_CMD_PLAY": 33,
                "TV_CMD_PAUSE": 34,
                "TV_CMD_STOP": 35,
                "TV_CMD_FAST_FORWARD": 36,
                "TV_CMD_REWIND": 37,
                "TV_CMD_SKIP_FORWARD": 38,
                "TV_CMD_SKIP_BACKWARD": 39,
                "TV_CMD_RECORD": 40,
                "TV_CMD_RECORDING_LIST": 41,
                "TV_CMD_REPEAT": 42,
                "TV_CMD_LIVE_TV": 43,
                "TV_CMD_EPG": 44,
                "TV_CMD_PROGRAM_INFORMATION": 45,
                "TV_CMD_ASPECT_RATIO": 46,
                "TV_CMD_EXTERNAL_INPUT": 47,
                "TV_CMD_PIP_SECONDARY_VIDEO": 48,
                "TV_CMD_SHOW_SUBTITLE": 49,
                "TV_CMD_PROGRAM_LIST": 50,
                "TV_CMD_TELE_TEXT": 51,
                "TV_CMD_MARK": 52,
                "TV_CMD_3D_VIDEO": 400,
                "TV_CMD_3D_LR": 401,
                "TV_CMD_DASH": 402,
                "TV_CMD_PREVIOUS_CHANNEL": 403,
                "TV_CMD_FAVORITE_CHANNEL": 404,
                "TV_CMD_QUICK_MENU": 405,
                "TV_CMD_TEXT_OPTION": 406,
                "TV_CMD_AUDIO_DESCRIPTION": 407,
                "TV_CMD_ENERGY_SAVING": 409,
                "TV_CMD_AV_MODE": 410,
                "TV_CMD_SIMPLINK": 411,
                "TV_CMD_EXIT": 412,
                "TV_CMD_RESERVATION_PROGRAM_LIST": 413,
                "TV_CMD_PIP_CHANNEL_UP": 414,
                "TV_CMD_PIP_CHANNEL_DOWN": 415,
                "TV_CMD_SWITCH_VIDEO": 416,
                "TV_CMD_APPS": 417,
                "TV_CMD_MOUSE_MOVE": "HandleTouchMove",
                "TV_CMD_MOUSE_CLICK": "HandleTouchClick",
                "TV_CMD_TOUCH_WHEEL": "HandleTouchWheel",
                "TV_CMD_CHANGE_CHANNEL": "HandleChannelChange",
                "TV_CMD_SCROLL_UP": "up",
                "TV_CMD_SCROLL_DOWN": "down",
                "TV_INFO_CURRENT_CHANNEL": "cur_channel",
                "TV_INFO_CHANNEL_LIST": "channel_list",
                "TV_INFO_CONTEXT_UI": "context_ui",
                "TV_INFO_VOLUME": "volume_info",
                "TV_INFO_SCREEN": "screen_image",
                "TV_INFO_3D": "is_3d",
                "TV_LAUNCH_APP": "AppExecute"}

    def __init__(self, ip, port=8080, auth_key=None, session=None):
        self.TV_IP = ip
        self.TV_PORT = port
        self.AUTH_KEY = auth_key
        self.SESSION = session

    def display_auth(self):
        xml = '<?xml version="1.0" ?> <!--?xml version="1.0" encoding="utf-8"?--> <auth> <type>AuthKeyReq</type></auth>'
        headers = {'Content-Type': 'application/atom+xml'}
        requests.post("http://" + self.TV_IP + ":" + str(self.TV_IP) + "/roap/api/auth", data=xml, headers=headers)

    def authenticate(self, key=None):

        key_to_use = None

        if key is not None:
            key_to_use = key
        elif self.AUTH_KEY is not None:
            key_to_use = self.AUTH_KEY
        else:
            print "Auth key required!"
            return None

        xml = """<?xml version="1.0" ?> <!--?xml version="1.0" encoding="utf-8"?--> <auth> <type>AuthReq</type> <value>""" + str(
            key_to_use) + """</value></auth>"""
        headers = {'Content-Type': 'application/atom+xml'}
        r = requests.post("http://" + self.TV_IP + ":" + str(self.TV_PORT) + "/roap/api/auth", data=xml,
                          headers=headers)

        dom = parseString(r.content)
        error_code = dom.getElementsByTagName("ROAPError")[0].childNodes[0].data
        error_detail = dom.getElementsByTagName("ROAPErrorDetail")[0].childNodes[0].data
        session = dom.getElementsByTagName("session")[0].childNodes[0].data

        if error_code == "200" and self.SESSION is None:
            self.SESSION = session
        #else:
        #    raise (str(error_detail))

            # session = xml_response.xpath("/envelope/session")[0]
            #print session

    def send_command(self, command, session=None):
        xml = """<?xml version="1.0" ?> <!--?xml version="1.0" encoding="utf-8"?--> <command><value>""" + \
              str(self.COMMANDS.get(command)) + """</value><name>""" + str(command) + """</name></command>"""
        headers = {'Content-Type': 'application/atom+xml'}

        r = requests.post("http://" + self.TV_IP + ":" + str(self.TV_PORT) + "/roap/api/auth", data=xml,
                          headers=headers)

        print r.content
        #dom = parseString(r.content)
        #error_code = dom.getElementsByTagName("ROAPError")[0].childNodes[0].data
        #error_detail = dom.getElementsByTagName("ROAPErrorDetail")[0].childNodes[0].data
        #session = dom.getElementsByTagName("session")[0].childNodes[0].data


