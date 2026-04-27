import os
import subprocess

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

def play_sound(name):
    sounds = {
        "start": "/System/Library/Sounds/Glass.aiff",
        "end": "/System/Library/Sounds/Ping.aiff"
    }
    sound_path = sounds.get(name)
    if sound_path and os.path.exists(sound_path):
        subprocess.run(["afplay", sound_path])

def get_all_screen_geometries():
    # In a real implementation, we might use screensize or PyObjC
    # For now, we return a basic representation
    return [{"width": 1920, "height": 1080}]
