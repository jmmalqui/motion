import time
import typing
from enum import Enum
from dataclasses import dataclass
from .curves import *


class LoopType(Enum):
    ONEWAY = 0
    CLOSED = 1


_AnimNodePoint: typing.TypeAlias = typing.Union[int, float, list[int | float]]


def _node_sum(n: _AnimNodePoint, n2: _AnimNodePoint):
    if isinstance(n, list) and isinstance(n2, list):
        mult_list = []
        for idx, entry in enumerate(n):
            mult_list.append(entry + n2[idx])
        return mult_list
    else:
        return n + n2


def _node_mult(n: _AnimNodePoint, factor: int | float):
    if isinstance(n, list):
        mult_list = []
        for entry in n:
            mult_list.append(entry * factor)
        return mult_list
    else:
        return n * factor


@dataclass
class _AnimNode:
    start: _AnimNodePoint
    end: _AnimNodePoint
    duration_ms: int
    easing_type: typing.Callable

    def diff(self):
        if isinstance(self.start, list) and isinstance(self.end, list):
            diff_list = []
            for idx, entry in enumerate(self.end):
                diff_list.append(entry - self.start[idx])
            return diff_list
        else:
            return self.end - self.start


def check_for_data_type_coherence(d1, d2):
    d1_type = type(d1)
    d2_type = type(d2)

    if isinstance(d1, int) and isinstance(d2, float):
        d1 = float(d1)
    elif isinstance(d1, float) and isinstance(d2, int):
        d2 = float(d2)
    elif isinstance(d1, list) and isinstance(d2, list):
        return len(d1) == len(d2)

    return d1_type == d2_type


class Animator:
    def __init__(self) -> None:
        self.frame = 0
        self.frames: list[_AnimNode] = []
        self.current_value: typing.Optional[_AnimNodePoint] = None
        self.loop_type: typing.Optional[LoopType] = None
        self.time_stamp = time.time()
        self._is_playing = False
        self.going_backwards = False

    def get_value(self):
        return self.current_value

    def add_frame(self, start, end, duration_ms, easing_type):
        data_type_check_pass = check_for_data_type_coherence(start, end)
        if not data_type_check_pass:
            raise TypeError()
        self.frames.append(_AnimNode(start, end, duration_ms, easing_type))

    def play(self, loops: int, loop_type: LoopType):
        self.loops = loops
        self.loop_type = loop_type
        self._is_playing = True
        self.current_value = self.frames[self.frame].start
        self.time_stamp = time.time()

    def is_playing(self):
        return self._is_playing

    def update(self):
        if self.is_playing():
            frame = self.frames[self.frame]
            time_diff = (time.time() - self.time_stamp) * 1000
            t = time_diff / frame.duration_ms
            if time_diff / frame.duration_ms >= 1:
                if self.frame == len(self.frames) - 1 and not self.going_backwards:
                    self.current_value = frame.end
                    if self.loop_type == LoopType.ONEWAY:
                        self.loops -= 1
                        if self.loops == 0:
                            self._is_playing = False
                        else:
                            self.frame = 0
                            self.current_value = self.frames[self.frame].start
                            self.time_stamp = time.time()
                    elif self.loop_type == LoopType.CLOSED:
                        self.going_backwards = True
                        self.time_stamp = time.time()
                    else:
                        self._is_playing = False
                elif self.frame == 0 and self.going_backwards:
                    self.loops -= 1
                    if self.loops == 0:
                        self._is_playing = False
                    else:
                        self.going_backwards = False
                        self.current_value = self.frames[self.frame].start
                        self.time_stamp = time.time()
                else:
                    if self.going_backwards:
                        self.frame -= 1
                        self.current_value = self.frames[self.frame].end
                        self.time_stamp = time.time()
                    elif not self.going_backwards:
                        self.frame += 1
                        self.current_value = self.frames[self.frame].start
                        self.time_stamp = time.time()
            else:
                if not self.going_backwards:
                    self.current_value = _node_sum(
                        frame.start, _node_mult(frame.diff(), frame.easing_type(t))
                    )
                elif self.going_backwards:
                    self.current_value = _node_sum(
                        frame.start,
                        _node_mult(frame.diff(), frame.easing_type(1 - t)),
                    )
