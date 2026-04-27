import rumps
import multiprocessing
from timer import TimerEngine
from overlay import FullscreenOverlay
from config import UserConfig
from utils import format_time, play_sound
from notifications import send_notification

def run_overlay_process(break_duration):
    # This runs in a completely separate process to avoid
    # conflict with the rumps/AppKit event loop.
    overlay = FullscreenOverlay(
        break_duration=break_duration,
        on_close=None # Processes cannot easily call back to the main app
    )
    overlay.show()

class MenubarApp(rumps.App):
    def __init__(self, config):
        super().__init__("👁 20:00")
        self.config = config

        # State
        self.timer_engine = None
        self.overlay_process = None
        self.break_pending = False

        # Menu setup
        self.menu = [
            rumps.MenuItem("Pause / Resume", callback=self.toggle_pause),
            rumps.MenuItem("Skip This Break", callback=self.skip_break),
            rumps.separator,
            rumps.MenuItem("Settings", callback=self.open_settings),
        ]

        self.init_engine()
        self.start_break_checker()

    def init_engine(self):
        self.timer_engine = TimerEngine(
            work_minutes=self.config.get("work_interval_minutes"),
            break_seconds=self.config.get("break_duration_seconds"),
            on_tick=self.update_title,
            on_break_due=self.trigger_break,
            on_break_complete=self.end_break
        )
        self.timer_engine.start()

    def start_break_checker(self):
        @rumps.timer(1)
        def check_break(_):
            if self.break_pending:
                self.break_pending = False
                self.show_overlay()
        self._break_checker = check_break

    def update_title(self, seconds):
        self.set_title_text(seconds)

    def set_title_text(self, seconds):
        self.title = f"👁 {format_time(seconds)}"

    def toggle_pause(self, sender):
        if self.timer_engine.is_paused:
            self.timer_engine.resume()
            self.title = f"👁 {format_time(self.timer_engine.remaining)}"
        else:
            self.timer_engine.pause()
            self.title = "⏸ Paused"

    def skip_break(self, sender):
        self.timer_engine.skip()

    def trigger_break(self):
        if self.config.get("sound_enabled"):
            play_sound("start")
        self.break_pending = True

    def show_overlay(self):
        # Launch overlay in a separate process
        duration = self.config.get("break_duration_seconds")
        self.overlay_process = multiprocessing.Process(target=run_overlay_process, args=(duration,))
        self.overlay_process.start()

    def end_break(self):
        if self.config.get("sound_enabled"):
            play_sound("end")
        self.title = f"👁 {format_time(self.timer_engine.remaining)}"

    def open_settings(self, sender):
        print("Settings panel opened")

    def quit_app(self, sender):
        if self.overlay_process and self.overlay_process.is_alive():
            self.overlay_process.terminate()
        rumps.quit_application()
