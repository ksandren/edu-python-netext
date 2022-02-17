#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
from tkinter import *
import wsmgr

IDENT = 5
LINE_LEN = 40
LINE_HEIGHT = 20
FONT = ('Consolas', 14)


class StringGenerator:
    def __init__(self, lang):
        self.word_set = wsmgr.load_word_set(lang)

    def gen_rand_string(self, approx_length):
        if len(self.word_set) == 0:
            return 'Error: word_set is empty'
        result = ''
        for i in range(approx_length):
            sample = random.sample(list(self.word_set), 1)
            if len(sample) > 0:
                result += sample[0]
            if len(result) >= approx_length:
                return result
            else:
                result += ' '
        return 'Error: bad word_set'


class TextState:
    def __init__(self):
        self._str_gen = StringGenerator('RU')
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
        self.prev_count = 0
        self.cycle_count = 0

    def drop_char(self):
        self.useless_keys += 1
        if self.cursor_pos > 0:
            if self.input_len == self.cursor_pos:
                self.input_len -= 1
            self.cursor_pos -= 1
            self.current_input[self.cursor_pos] = ''
            self.current_highlight[self.cursor_pos] = 'x'

    def put_char(self, char):
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
        self.prev_line = self.current_line + ' ' + str(round(self.input_speed)) + 'spm '
        self.prev_line += str(round(len(self.current_line) / (self.cycle_count / 600))) + 'spm'
        self.current_line = self.next_line
        self.next_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.current_highlight = ['_'] * len(self.current_line)
        self.current_input = [''] * len(self.current_line)
        self.cursor_pos = 0
        self.input_len = 0
        self.cycle_count = 0

    def move_left(self):
        self.useless_keys += 1
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def move_right(self):
        self.useless_keys += 1
        if self.cursor_pos < self.input_len:
            self.cursor_pos += 1

    def update_timer(self):
        self.input_speed += 0.1*((self.useful_keys - self.prev_count)*600 - self.input_speed)
        self.prev_count = self.useful_keys
        self.cycle_count += 1


class MainWindow:
    def __init__(self):
        self.text_state = TextState()

        self.window = Tk()
        self.window.title("Not Enough Text")
        self.window.geometry('800x300')

        self.cvs = Canvas(self.window, width=800, height=200, bg='white')
        self.cvs.grid(column=0, row=0)
        self.cvs.bind('<Key>', self.cvs_key_event)
        self.cvs.focus_set()

        self.timer()
        #self.update()

    def update(self):
        # Clear canvas
        self.cvs.delete('all')
        # Draw next line
        self.cvs.create_text(IDENT, IDENT,
                             anchor='nw',
                             text=self.text_state.next_line, font=FONT)
        # Draw current line with current input and highlight
        last_x = IDENT
        for i in range(len(self.text_state.current_line)):
            new_char = self.text_state.current_input[i]
            color = 'black'
            if new_char == '':
                new_char = self.text_state.current_line[i]
                color = 'gray'
            new_char_id = self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                               anchor='nw',
                                               text=new_char,
                                               font=FONT, fill=color)
            x1, y1, x2, y2 = self.cvs.bbox(new_char_id)
            if self.text_state.cursor_pos == i:
                self.cvs.create_line(x1 + 1, y1 + 1, x1 + 1, y2 - 1, width=2)
            # Draw highlight
            highlight = self.text_state.current_highlight[i]
            if highlight == '+':  # Correct
                self.cvs.create_line(x1, y2, x2, y2, fill='lightgreen', width='2p')
            elif highlight == '-':  # Incorrect
                self.cvs.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline='', fill='red', width='2p')
                self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                     anchor='nw',
                                     text=self.text_state.current_input[i],
                                     font=FONT,
                                     fill='black')
                self.cvs.create_rectangle(x1 + 1, y1 + 1 - LINE_HEIGHT * 2/3,
                                          x2 - 1, y2 - 1 - LINE_HEIGHT * 2/3,
                                          outline='', fill='lightblue', width='2p')
                self.cvs.create_text(last_x, IDENT + LINE_HEIGHT * 1/3,
                                     anchor='nw',
                                     text=self.text_state.current_line[i],
                                     font=FONT,
                                     fill='black')
            elif highlight == 'x':  # Deleted
                self.cvs.create_line(x1, y2, x2, y2, fill='red', width='2p')
            elif highlight == 'v':  # Fixed
                self.cvs.create_line(x1, y2, x2, y2, fill='orange', width='2p')
            last_x = x2 - 1
        # Draw prev line
        self.cvs.create_text(IDENT, IDENT + 2*LINE_HEIGHT,
                             anchor='nw',
                             text=self.text_state.prev_line, font=FONT)
        stat = 'Keys statistics: useful: ' + str(self.text_state.useful_keys) +\
               ' useless: ' + str(self.text_state.useless_keys) +\
               ' speed: ' + str(round(self.text_state.input_speed)) + 'spm'
        self.cvs.create_text(IDENT, IDENT + 3 * LINE_HEIGHT,
                             anchor='nw',
                             text=stat, font=FONT, fill='green')

    def cvs_key_event(self, event):
        if event.keysym == 'BackSpace':
            self.text_state.drop_char()
        elif event.keysym == 'Return':
            if ''.join(self.text_state.current_input) ==\
                    self.text_state.current_line:
                self.text_state.new_line()
        elif event.keysym == 'Left':
            self.text_state.move_left()
        elif event.keysym == 'Right':
            self.text_state.move_right()
        elif event.char is not None and \
                event.char != '' and event.char.isprintable():
            self.text_state.put_char(event.char)
        self.update()

    def timer(self):
        self.text_state.update_timer()
        self.update()
        self.window.after(100, self.timer)

def main():
    main_window = MainWindow()
    main_window.window.mainloop()


if __name__ == "__main__":
    main()
