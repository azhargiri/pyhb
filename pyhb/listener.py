import Xlib.X
from pynput import keyboard

class XorgListener(keyboard.Listener):
    def _handle(self, display, event):
        try:
            key = self._event_to_key(display, event)
        except IndexError:
            key = None

        if event.type == Xlib.X.KeyPress:
            self.on_press(key, event)

        elif event.type == Xlib.X.KeyRelease:
            self.on_release(key, event)
