#!/usr/bin/env python

"""
timer.py:

Implementation of a CPU timer that is used as a part of stopping criteria.
"""

import time


def _time():
    """
    Convenience function that returns current process time as milliseconds.
    """
    return time.process_time() * 1000


class Timer:
    """
    Captures CPU time and keeps track of it. In so doing,
    various actions could be measured as milliseconds.
    """

    def __init__(self, goal=None):
        """
        Timer constructor. It is stopped upon initialization.
        :params goal: Optional threshold time (as milliseconds) that is used
        as a time limit.
        """

        self.time_start = _time()
        self.time_stop = _time()
        if goal is None:
            self.time_goal = float("inf")
        else:
            self.time_goal = goal

        self.running = False

    def start(self):
        """
        Starts the timer.
        """

        self.time_start = _time()
        self.time_stop = 0
        self.running = True

    def reset(self):
        """
        Resets the timer.
        """

        self.time_start = _time()
        self.time_stop = 0

    def stop(self):
        """
        Stops the timer.
        """

        self.time_stop = _time() - self.time_start
        self.running = False

    def elapsed(self):
        """
        Calculates total time that has passed since starting the timer.
        """

        if self.running is False:
            return _time() - self.time_start
        else:
            return (_time() - self.time_start) - self.time_stop

    def difference(self):
        """
        Calculates time difference between time threshold and total elapsed time.
        """

        if self.running is False:
            return self.time_goal - self.time_stop
        else:
            return self.time_goal - (_time() - self.time_start)

    def past_goal(self):
        """
        Checks whether total elapsed time has exceeded the threshold.
        """

        return self.difference() < 0
