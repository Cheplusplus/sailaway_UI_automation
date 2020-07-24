from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pyautogui as pag


view_options_width, view_options_center = 1023, 17
mouse_clicks = []


class InstrumentPanel:
    heel_tab = False
    panel_top_left, panel_bottom_right, panel_width, panel_height, body_height, body_middle = 0, 0, 0, 0, 0, 0
    button_width = 0
    trim_button = 50
    tack = False   #False is port tack

    @staticmethod
    def port_tack():
        InstrumentPanel.tack = False

    @staticmethod
    def starboard_tack():
        InstrumentPanel.tack = True

    @staticmethod
    def set_button_width():
        InstrumentPanel.button_width = InstrumentPanel.panel_width / 4 if not InstrumentPanel.heel_tab else \
            InstrumentPanel.panel_width / 5

    @staticmethod
    def hide_heel_tab():
        InstrumentPanel.heel_tab = not InstrumentPanel.heel_tab
        InstrumentPanel.set_button_width()

    @staticmethod
    def heel_tab_toggle():
        pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 2.5,
                  InstrumentPanel.panel_bottom_right[1] - 5)

    @staticmethod
    def gps_tab_toggle():
        if not InstrumentPanel.heel_tab:
            try:
                pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 2.5,
                          InstrumentPanel.panel_bottom_right[1] - 5)
            except TypeError:
                print("Please set panel size by pressing 'j' then click"
                      " on top left and bottom right corner of the instrument panel ")
        else:
            try:
                pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 3.5,
                          InstrumentPanel.panel_bottom_right[1] - 5)
            except TypeError:
                print("Please set panel size by pressing 'j' then click"
                      " on top left and bottom right corner of the instrument panel ")

    @staticmethod
    def trim_tab_toggle():
        try:
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 1.5,
                      InstrumentPanel.panel_bottom_right[1] - 5)
        except TypeError:
            print("Please set panel size by pressing 'j' then click"
                  " on top left and bottom right corner of the instrument panel ")

    @staticmethod
    def info_tab_toggle():
        try:
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 0.5,
                      InstrumentPanel.panel_bottom_right[1] - 5)
        except TypeError:
            print("Please set panel size by pressing 'j' then click"
                  " on top left and bottom right corner of the instrument panel ")

    @staticmethod
    def change_tack():
        InstrumentPanel.heel_tab_toggle()
        if InstrumentPanel.tack:
            pag.click(InstrumentPanel.panel_top_left[0] + InstrumentPanel.panel_width/7, InstrumentPanel.body_middle)
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.panel_width/3.5,
                      InstrumentPanel.body_middle + InstrumentPanel.body_height / 4.5)
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.panel_width/3.5,
                      InstrumentPanel.body_middle + InstrumentPanel.body_height / 4.5)
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.panel_width/4, InstrumentPanel.body_middle)
            InstrumentPanel.tack = False
        else:
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.panel_width/7, InstrumentPanel.body_middle)
            pag.click(InstrumentPanel.panel_top_left[0] + InstrumentPanel.panel_width/3.5,
                      InstrumentPanel.body_middle + InstrumentPanel.body_height / 4.5)
            pag.click(InstrumentPanel.panel_top_left[0] + InstrumentPanel.panel_width/3.5,
                      InstrumentPanel.body_middle + InstrumentPanel.body_height / 4.5)
            pag.click(InstrumentPanel.panel_top_left[0] + InstrumentPanel.panel_width/4, InstrumentPanel.body_middle)
            InstrumentPanel.tack = True

        InstrumentPanel.info_tab_toggle()

    @staticmethod
    def panel_size():

        top_left, bottom_right, body_height = find_instrument_panel_size()

        InstrumentPanel.panel_width = bottom_right[0] - top_left[0]
        InstrumentPanel.panel_height = bottom_right[1] - top_left[1]
        InstrumentPanel.panel_top_left = top_left
        InstrumentPanel.panel_bottom_right = bottom_right
        InstrumentPanel.body_height = body_height[1] - bottom_right[1]
        InstrumentPanel.body_middle = InstrumentPanel.body_height/2 + bottom_right[1]
        InstrumentPanel.set_button_width()


def boat_light_toggle():
    pag.click(1000, 5)
    pag.moveTo(1000, 100, duration=0.15)
    pag.click(1000, 100)
    pag.moveTo(1000, 5, duration=0.1)
    pag.click(1000, 5)


def hide_hud():
    pag.click(1800, 5)


def capture_screen():
    return pag.screenshot()


def find_instrument_panel_size():

    clicks = len(mouse_clicks)
    while len(mouse_clicks) <= clicks:
        pass
    top_left = mouse_clicks[-1]
    clicks = len(mouse_clicks)
    while len(mouse_clicks) <= clicks:
        pass
    bottom_right = mouse_clicks[-1]
    clicks = len(mouse_clicks)
    while len(mouse_clicks) <= clicks:
        pass
    body_height = mouse_clicks[-1]
    return top_left, bottom_right, body_height


def on_press(key):
    mouse_pos = pag.position()
    try:
        key = key.char
    except AttributeError:
        return
    keys = {
        '5': InstrumentPanel.gps_tab_toggle,
        '6': InstrumentPanel.trim_tab_toggle,
        '7': InstrumentPanel.info_tab_toggle,
        '8': InstrumentPanel.heel_tab_toggle,
        'o': hide_hud,
        'l': boat_light_toggle,
        'j': InstrumentPanel.panel_size,
        'k': InstrumentPanel.change_tack,
        '0': InstrumentPanel.hide_heel_tab,
        '[': InstrumentPanel.port_tack,
        ']': InstrumentPanel.starboard_tack
    }
    try:
        keys[key]()
    except KeyError:
        pass
    pag.moveTo(mouse_pos)


def on_release(key):
    pass


def on_click(x, y, button, pressed):
    if pressed:
        mouse_clicks.append((x, y))


keyboard_listener = KeyboardListener(
        on_press=on_press,
        on_release=on_release)

mouse_listener = MouseListener(
        on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

while True:
    pass


