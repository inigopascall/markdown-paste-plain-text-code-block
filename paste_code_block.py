#!/usr/bin/env python3
import subprocess
import pyperclip
import time

def get_active_window_info():
    try:
        window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
        window_name = subprocess.check_output(['xdotool', 'getwindowname', window_id]).decode().strip().lower()
        window_class = subprocess.check_output(['xprop', '-id', window_id, 'WM_CLASS']).decode().strip().split('"')[-2].lower()
        return window_name, window_class
    except:
        return "", ""

def execute_xdotool_commands(commands):
    for cmd in commands:
        subprocess.run(cmd, shell=False)

def strip_and_paste():
    window_name, window_class = get_active_window_info()
    text = pyperclip.paste().strip()

    is_slack = "slack" in window_name and window_class == "google-chrome"

    if is_slack:
        commands = [
            ['xdotool', 'type', '```'],
            ['xdotool', 'type', '```'],
            ['xdotool', 'key', 'Up']
        ]
    else:
        commands = [
            ['xdotool', 'type', '```'],
            ['xdotool', 'key', 'shift+Return', 'shift+Return'],
            ['xdotool', 'type', '```'],
            ['xdotool', 'key', 'Up']
        ]

    execute_xdotool_commands(commands)
    
    pyperclip.copy(text)
    subprocess.run(['xdotool', 'key', 'ctrl+v'])

    if is_slack:
        execute_xdotool_commands([['xdotool', 'key', 'Down', 'Down', 'Down', 'End']])
    else:
        execute_xdotool_commands([
            ['xdotool', 'key', 'Down', 'Down', 'Down', 'End'],
            ['xdotool', 'key', 'shift+Return', 'shift+Return']
        ])

if __name__ == "__main__":
    strip_and_paste()
