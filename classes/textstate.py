#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
from classes.stringgenerator import StringGenerator


LINE_LEN = 40


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
            self.current_highlight[self.cursor_pos] = 'x'

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
            if self.current_highlight[self.cursor_pos] == '_':
                self.current_highlight[self.cursor_pos] = '+'
            else:
                self.current_highlight[self.cursor_pos] = 'v'
        else:
            self.current_highlight[self.cursor_pos] = '-'
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
        self.current_highlight = ['_'] * len(self.current_line)
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

    def update_timer(self):
        if self.round_started:
            self.input_speed = self.useful_keys / ((time.time_ns() - self.start_time_ns) / 60000000000)
            if (time.time_ns() - self.start_time_ns) / 600000000 >= self.round_time * 60:
                self.round_started = False
                self.round_finished()
                self.current_line = ''
                self.next_line = ''

    def set_lang(self, lang):
        self._str_gen = StringGenerator(lang)
        self.current_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.next_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.current_input = [''] * len(self.current_line)
        self.current_highlight = ['_'] * len(self.current_line)
        self.prev_line = ''
        self.cursor_pos = 0
        self.input_len = 0
        self.useful_keys = 0
        self.useless_keys = 0
        self.input_speed = 0
        self.start_time_ns = 0
