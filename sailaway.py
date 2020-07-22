from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import pyautogui as pag


view_options_width, view_options_center = 1023, 17
mouse_clicks = []


class InstrumentPanel:
    heel_tab = False
    panel_top_left, panel_bottom_right, panel_width, panel_height = 0, 0, 0, 0
    button_width = 0

    @staticmethod
    def gps_tab_toggle():
        try:
            pag.click(InstrumentPanel.panel_bottom_right[0] - InstrumentPanel.button_width * 2.5,
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
    def panel_size():

        top_left, bottom_right = find_instrument_panel_size()

        InstrumentPanel.panel_width = bottom_right[0] - top_left[0]
        InstrumentPanel.panel_height = bottom_right[1] - top_left[1]
        InstrumentPanel.panel_top_left = top_left
        InstrumentPanel.panel_bottom_right = bottom_right
        InstrumentPanel.button_width = InstrumentPanel.panel_width / 4 if not InstrumentPanel.heel_tab else\
            InstrumentPanel.panel_width / 5


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
    return top_left, bottom_right


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
        'o': hide_hud,
        'l': boat_light_toggle,
        'j': InstrumentPanel.panel_size
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


