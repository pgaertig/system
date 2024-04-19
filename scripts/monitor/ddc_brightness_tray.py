#!/usr/bin/env python3

from monitorcontrol import get_monitors, Monitor
from gi.repository import AppIndicator3 as AI
from gi.repository import Gtk, Gdk
import functools
from typing import Iterable
from monitorcontrol.vcp.vcp_abc import VCPIOError

APPNAME = "Monitor Brightness Control"
ICON = "video-display-symbolic"  # Example icon path, adjust as necessary

brightness_change_in_progress = False

class MonitorInfo:
    def __init__(self, monitor):
        self.monitor = monitor
        self.model = self.get_model()
        self.luminance = self.get_luminance()

    def get_model(self):
        try:
            with self.monitor:
                monitor_dict = self.monitor.get_vcp_capabilities()
                return monitor_dict["model"]
        except VCPIOError:
            print("An error occurred while getting VCP capabilities for the monitor. Setting model to 'Unknown'.")
            return "Unknown"

    def get_luminance(self):
        with self.monitor:
            return self.monitor.get_luminance()

    def set_luminance(self, value):
        with self.monitor:
            self.monitor.set_luminance(value)
        self.luminance = value


# Function to get connected monitors and their brightness
@functools.lru_cache(maxsize=None)
def get_monitors2() -> Iterable[MonitorInfo]:
    return [MonitorInfo(monitor) for monitor in get_monitors()]

def all_monitors_info():
    monitors_info = []
    for monitor_info in get_monitors2():
        monitors_info.append((monitor_info.model, monitor_info.luminance))
    return monitors_info

# Function to adjust brightness, direction should be either +10 or -10
def adjust_brightness(direction):
    global brightness_change_in_progress
    brightness_change_in_progress = True
    monitors_info = get_monitors2()
    for monitor_info in monitors_info:
        #with(monitor_info.monitor):
        current_brightness = monitor_info.luminance
        if direction == Gdk.ScrollDirection.UP:
            monitor_info.set_luminance(min(current_brightness + 10, 100))
        elif direction == Gdk.ScrollDirection.DOWN:
            monitor_info.set_luminance(max(current_brightness - 10, 0))
    brightness_change_in_progress = False

def scroll(ai=None, steps=None, direction=None):
    global brightness_change_in_progress
    if brightness_change_in_progress:
        return
    if direction == Gdk.ScrollDirection.UP:
        adjust_brightness(Gdk.ScrollDirection.UP)
        print("Increased brightness by 10%")
    elif direction == Gdk.ScrollDirection.DOWN:
        adjust_brightness(Gdk.ScrollDirection.DOWN)
        print("Decreased brightness by 10%")

def makemenu():
    menu = Gtk.Menu()

    for monitor_info in get_monitors2():
        monitor_label = Gtk.MenuItem(f"{monitor_info.model}: {monitor_info.luminance}")
        menu.append(monitor_label)

        # Create a slider with a range of 0 to 100 and a step increment of 10
        #slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 10)
        #slider.set_value(monitor_info.luminance)  # Set the initial value to the current luminance
        #slider.connect('value-changed', lambda s: monitor_info.set_luminance(s.get_value()))  # Update the luminance when the slider is moved

        #slider_item = Gtk.MenuToolButton.new(None, None)
        #slider_item = Gtk.MenuItem.new()
        #slider_item.add(slider)
        #slider_item.set_icon_widget(slider)
        #menu.append(slider_item)

        menu.append(Gtk.SeparatorMenuItem())

    exit_item = Gtk.MenuItem('Quit')
    exit_item.connect('activate', Gtk.main_quit)
    #exit_item.show()
    menu.append(exit_item)
    menu.show_all()
    return menu

def startapp():
    ai = AI.Indicator.new(APPNAME, ICON, AI.IndicatorCategory.HARDWARE)
    ai.set_status(AI.IndicatorStatus.ACTIVE)
    ai.set_menu(makemenu())
    ai.connect("scroll-event", scroll)

    ai.set_label("Brightness", APPNAME)
    Gtk.main()

if __name__ == "__main__":
    startapp()