import time
from threading import Timer
from datetime import datetime

class TimerEngine:
    def __init__(self, work_minutes, break_seconds, on_tick, on_break_due, on_break_complete):
        self.work_interval = work_minutes * 60
        self.break_duration = break_seconds
        self.on_tick = on_tick
        self.on_break_due = on_break_due
        self.on_break_complete = on_break_complete

        self.remaining = self.work_interval
        self.is_paused = False
        self.is_in_break = False
        self.timer = None

    def start(self):
        if not self.timer:
            self._schedule_next_tick()

    def _schedule_next_tick(self):
        self.timer = Timer(1.0, self._tick)
        self.timer.start()

    def _tick(self):
        if not self.is_paused:
            if not self.is_in_break:
                self.remaining -= 1
                print(f"Work tick: {self.remaining}s remaining")
                self.on_tick(self.remaining)
                if self.remaining <= 0:
                    print("Break due! Triggering callback...")
                    self.is_in_break = True
                    self.on_break_due()
                    self.remaining = self.break_duration
            else:
                self.remaining -= 1
                print(f"Break tick: {self.remaining}s remaining")
                self.on_tick(self.remaining)
                if self.remaining <= 0:
                    print("Break complete! Triggering callback...")
                    self.is_in_break = False
                    self.on_break_complete()
                    self.remaining = self.work_interval
        else:
            print("Timer paused")

        self._schedule_next_tick()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def reset(self):
        self.remaining = self.work_interval
        self.is_in_break = False
        self.on_tick(self.remaining)

    def skip(self):
        if self.is_in_break:
            # Cannot skip during overlay (as per rules)
            return
        self.remaining = 0 # Trigger break immediately
