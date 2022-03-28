import click
import os
import random
from colorama import Fore
from pyhb.utils import output
from pyhb.listener import XorgListener

# Ignore the pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import json


# Initialize the pygame.mixer submodule
pygame.mixer.init()

RELEASED = True

try:
    with open(
        os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        + "/Soundpacks/config.json"
    ) as f:
        config = json.load(f)
except FileNotFoundError:
    print("Soundpacks not installed, try doing 'pyhb install'")


def set_release(*args, **kwargs) -> None:
    """
    :param args:
    :param kwargs:
    :return: None

    Sets RELEASED variable to True on key release
    """
    global RELEASED
    RELEASED = True


def main(sound_pack: str) -> None:
    user_path = os.path.dirname(os.path.realpath(__file__))
    """
    :param sound_pack: Name of the sound pack
    :return: None
    """
    # Check if soundpack is valid
    if sound_pack not in os.listdir(user_path + "/Soundpacks/") or sound_pack == "config.json":
        output(Fore.RED, f"Soundpack '{sound_pack}' does not exist.")
        output(Fore.YELLOW, 'Have you tried installing them first? `pyhb install-soundpacks`')
        exit()

    global RELEASED
    click.echo(f"pyhb has started playing {sound_pack}...")
    click.echo("Use <ctrl + c> to close")

    conf_vals = list(config["defines"].values())
    conf_keys = list(config["defines"].keys())

    session = {}

    kuping = Kuping(session, conf_vals, conf_keys, sound_pack, user_path)

    with XorgListener(on_press=kuping.on_press, on_release=kuping.on_release) as listener:
        listener.join()

class Kuping:
    def __init__(self, session, conf_vals, conf_keys, sound_pack, user_path):
        self.session = session
        self.conf_vals = conf_vals
        self.conf_keys = conf_keys
        self.sound_pack = sound_pack
        self.user_path = user_path

    def on_press(self, key, event = None):
        if key in self.conf_vals:
            index = self.conf_vals.index(key)
            key = self.conf_keys[index]
        else:
            if key not in self.session:
                value = random.choice(self.conf_vals)
                self.session[key] = value

            key = self.session[key]
            index = self.conf_vals.index(key)
            key = self.conf_keys[index]

    def on_release(self, key, event = None):
        keycode = event.detail

        if self.sound_pack == "nk-cream":
            try:
                sound = pygame.mixer.Sound(
                    f"{self.user_path}/Soundpacks/{self.sound_pack}/{keycode}.wav"
                )
            except FileNotFoundError:
                sound = pygame.mixer.Sound(
                    f"{self.user_path}/Soundpacks/{self.sound_pack}/sound.wav"
                )
        else:
            try:
                sound = pygame.mixer.Sound(
                    f"{self.user_path}/Soundpacks/{self.sound_pack}/{keycode}.ogg"
                )
            except FileNotFoundError:
                sound = pygame.mixer.Sound(
                    f"{self.user_path}/Soundpacks/{self.sound_pack}/sound.ogg"
                )

        sound.play()

        global RELEASED
        RELEASED = False

        set_release()
