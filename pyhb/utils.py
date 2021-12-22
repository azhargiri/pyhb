import click
import logging
import random
import os
from colorama import Fore, Style
from typing import List, Union


# Path to which 'pyhb' is installed
user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


def output(color, msg) -> None:
    click.echo(color + msg + Style.RESET_ALL)


def list_options(options: Union[List[str], dict], colorize: bool = False) -> None:
    color = ""
    if colorize:
        colors = [
            Fore.BLUE,
            Fore.CYAN,
            Fore.GREEN,
            Fore.LIGHTBLACK_EX,
            Fore.LIGHTBLUE_EX,
            Fore.LIGHTCYAN_EX,
            Fore.LIGHTGREEN_EX,
            Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTRED_EX,
            Fore.LIGHTYELLOW_EX,
            Fore.MAGENTA,
            Fore.RED,
            Fore.RESET,
            Fore.YELLOW,
        ]

    for index, option in enumerate(options):
        if colorize:
            color = random.choice(colors)
        output(color, f"[{index + 1}] {option}")


