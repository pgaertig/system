#!/usr/bin/env python3

# This script shows a tray icon that allows you to adjust the brightness of monitor(s) using DDC/CI.
# Interact with the tray icon by scrolling up or down to increase or decrease brightness by 10% respectively.

import gi
gi.require_version('AppIndicator3', '0.1')
from monitorcontrol import get_monitors, Monitor
from gi.repository import AppIndicator3 as AI
from gi.repository import Gtk, Gdk
from gi.repository import GObject
import functools
import time
from typing import Iterable
from monitorcontrol.vcp.vcp_abc import VCPIOError

APPNAME = "Monitor Brightness Control"
ICON = "video-display-symbolic"

brightness_change_in_progress = False

class MonitorInfo(GObject.GObject):
    def __init__(self, monitor):
        super().__init__()
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
        old_luminance = self.luminance
        with self.monitor:
            self.monitor.set_luminance(value)
        self.luminance = value
        self.emit("luminance-changed")
        return old_luminance != self.luminance

    def brighten(self, amount=10):
        if self.luminance >= 100:
            return False
        return self.set_luminance(min(self.luminance + amount, 100))

    def darken(self, amount=10):
        if self.luminance <= 0:
            return False
        return self.set_luminance(max(self.luminance - amount, 0))


GObject.signal_new("luminance-changed", MonitorInfo, GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ())

@functools.lru_cache(maxsize=None)
def get_all_monitors() -> Iterable[MonitorInfo]:
    return [MonitorInfo(monitor) for monitor in get_monitors()]

def refresh_monitors(menu):
    print("Refreshing monitors...")
    last_refresh = time.time()
    get_all_monitors.cache_clear()
    build_menu(menu, get_all_monitors())

def handle_scroll(ai=None, steps=None, direction=None):
    global brightness_change_in_progress
    if brightness_change_in_progress:
        return

    brightness_change_in_progress = True
    monitors_info = get_all_monitors()
    for monitor_info in monitors_info:
        if direction == Gdk.ScrollDirection.UP:
            if monitor_info.brighten():
                print("Increased brightness by 10%")
        elif direction == Gdk.ScrollDirection.DOWN:
            if monitor_info.darken():
                print("Decreased brightness by 10%")
    brightness_change_in_progress = False
    # Flush the event queue to discard all pending scroll events
    for _ in range(100):
        if Gtk.events_pending():
            event = Gdk.event_peek()
            if event and event.type == Gdk.EventType.SCROLL:
                Gdk.event_get()
    return

def build_menu(menu, all_monitors=None):

    # Clear the menu before rebuilding it
    for child in menu.get_children():
        menu.remove(child)

    for monitor_info in all_monitors:
        monitor_label = Gtk.MenuItem(label=f"{monitor_info.model}: {monitor_info.luminance}")
        menu.append(monitor_label)

        monitor_info.connect("luminance-changed", lambda info, label=monitor_label: label.set_label(f"{info.model}: {info.luminance}"))

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
    refresh_item = Gtk.MenuItem(label='Refresh')
    refresh_item.connect('activate', lambda *args: refresh_monitors(menu))
    menu.append(refresh_item)

    menu.append(Gtk.SeparatorMenuItem())

    exit_item = Gtk.MenuItem(label='Quit')
    exit_item.connect('activate', Gtk.main_quit)

    menu.append(exit_item)
    menu.show_all()
    return menu

def startapp():
    ai = AI.Indicator.new(APPNAME, ICON, AI.IndicatorCategory.HARDWARE)
    ai.set_status(AI.IndicatorStatus.ACTIVE)
    menu = Gtk.Menu()
    ai.set_menu(build_menu(menu, get_all_monitors()))
    ai.connect("scroll-event", handle_scroll)
    ai.set_label("Brightness", APPNAME)
    Gtk.main()

if __name__ == "__main__":
    startapp()