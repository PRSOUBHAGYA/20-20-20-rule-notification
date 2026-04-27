import json
import os
from pathlib import Path

class UserConfig:
    def __init__(self):
        self.config_dir = Path("~/Library/Application Support/TwentyTwentyTwenty").expanduser()
        self.config_file = self.config_dir / "config.json"
        self.defaults = {
            "work_interval_minutes": 2,
            "break_duration_seconds": 20,
            "pre_warning_seconds": 30,
            "sound_enabled": True,
            "show_blink_counter": True,
            "start_on_login": False
        }
        self.settings = self._load()

    def _load(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return {**self.defaults, **json.load(f)}
        except Exception as e:
            print(f"Error loading config: {e}")
        return self.defaults.copy()

    def save(self):
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def reset_defaults(self):
        self.settings = self.defaults.copy()
        self.save()
