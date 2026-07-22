"""
Timer Module — Pomodoro, Stopwatch & Countdown Timers
=====================================================
Manages Pomodoro focus cycles, stopwatch timing, and countdown timers.
"""

import time
import threading


class PomodoroTimer:
    """
    Pomodoro Focus Timer (25 min focus / 5 min break).
    """

    def __init__(self, work_mins=25, break_mins=5, on_tick=None, on_finish=None):
        self.work_mins = work_mins
        self.break_mins = break_mins
        self.on_tick = on_tick
        self.on_finish = on_finish

        self.seconds_left = work_mins * 60
        self.is_running = False
        self.mode = "work"
        self._thread = None
        self._stop_flag = False

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._stop_flag = False

        def _loop():
            while self.seconds_left > 0 and not self._stop_flag:
                time.sleep(1)
                self.seconds_left -= 1
                if self.on_tick:
                    mins = self.seconds_left // 60
                    secs = self.seconds_left % 60
                    self.on_tick(f"{mins:02d}:{secs:02d}", self.mode)

            self.is_running = False
            if not self._stop_flag and self.on_finish:
                self.on_finish(self.mode)

        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def pause(self):
        self._stop_flag = True
        self.is_running = False

    def reset(self):
        self.pause()
        self.seconds_left = self.work_mins * 60
        self.mode = "work"
