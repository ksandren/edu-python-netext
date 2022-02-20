#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
from enum import Enum
from classes.stringgenerator import StringGenerator


LINE_LEN = 40


class HighlightType(Enum):
    EMPTY = '_'
    CORRECT = '+'
    INCORRECT = '-'
    DELETED = 'x'
    FIXED = 'v'


class TextState:
    def __init__(self):
        self._str_gen = None
        self.current_line = ''
        self.next_line = ''
        self.current_input = []
        self.current_highlight = []
        self.prev_line = ''
        self.cursor_pos = 0
        self.input_len = 0
        self.useful_keys = 0
        self.useless_keys = 0
        self.input_speed = 0
        self.round_started = False
        self.round_time = 0
        self.round_finished = None
        self.start_time_ns = 0

    def drop_char(self):
        self.useless_keys += 1
        if self.cursor_pos > 0:
            if self.input_len == self.cursor_pos:
                self.input_len -= 1
            self.cursor_pos -= 1
            self.current_input[self.cursor_pos] = ''
            self.current_highlight[self.cursor_pos] = HighlightType.DELETED

    def put_char(self, char):
        if self.useful_keys + self.useless_keys == 0:
            self.round_started = True
            self.start_time_ns = time.time_ns()
        if self.cursor_pos >= len(self.current_line):
            self.useless_keys += 1
            return
        if self.current_line[self.cursor_pos] == char:
            if self.current_line[self.cursor_pos] ==\
                    self.current_input[self.cursor_pos]:
                self.useless_keys += 1
            else:
                self.useful_keys += 1
            if self.current_highlight[self.cursor_pos] == HighlightType.EMPTY:
                self.current_highlight[self.cursor_pos] = HighlightType.CORRECT
            else:
                self.current_highlight[self.cursor_pos] = HighlightType.FIXED
        else:
            self.current_highlight[self.cursor_pos] = HighlightType.INCORRECT
            self.useless_keys += 1
        self.current_input[self.cursor_pos] = char
        self.cursor_pos += 1
        if self.input_len < self.cursor_pos:
            self.input_len = self.cursor_pos

    def new_line(self):
        self.useful_keys += 1
        self.prev_line = self.current_line + ' ' + str(round(self.input_speed)) + 'spm'
        self.current_line = self.next_line
        self.next_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.current_highlight = [HighlightType.EMPTY] * len(self.current_line)
        self.current_input = [''] * len(self.current_line)
        self.cursor_pos = 0
        self.input_len = 0

    def move_left(self):
        self.useless_keys += 1
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def move_right(self):
        self.useless_keys += 1
        if self.cursor_pos < self.input_len:
            self.cursor_pos += 1

    def stop(self):
        self.round_started = False
        self.round_finished()
        self.current_line = ''
        self.next_line = ''
        self.prev_line = ''

    def update_timer(self):
        if self.round_started:
            time_left = (time.time_ns() - self.start_time_ns) / 60_000_000_000
            self.input_speed = self.useful_keys / time_left
            if time_left >= self.round_time:
                self.stop()

    def set_lang(self, lang):
        self._str_gen = StringGenerator(lang)
        self.current_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.next_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.current_input = [''] * len(self.current_line)
        self.current_highlight = [HighlightType.EMPTY] * len(self.current_line)
        self.prev_line = ''
        self.cursor_pos = 0
        self.input_len = 0
        self.useful_keys = 0
        self.useless_keys = 0
        self.input_speed = 0
        self.start_time_ns = 0

    def is_active(self):
        return len(self.current_line) > 0
