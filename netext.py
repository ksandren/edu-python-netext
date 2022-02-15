#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
from tkinter import *
import wsmgr

IDENT = 5
LINE_LEN = 40
LINE_HEIGHT = 20


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
        self.current_input = ''
        self.current_highlight = ['_'] * len(self.current_line)
        self.prev_line = ''

    def drop_char(self):
        if len(self.current_input) > 0:
            self.current_input = self.current_input[:-1]
            ci_len = len(self.current_input)
            self.current_highlight[ci_len] = 'x'

    def put_char(self, char):
        ci_len = len(self.current_input)
        if ci_len >= len(self.current_line):
            return
        if self.current_line[ci_len] == char:
            if self.current_highlight[ci_len] == '_':
                self.current_highlight[ci_len] = '+'
            else:
                self.current_highlight[ci_len] = 'v'
        else:
            self.current_highlight[ci_len] = '-'
        self.current_input += char

    def new_line(self):
        self.prev_line = self.current_line
        self.current_line = self.next_line
        self.next_line = self._str_gen.gen_rand_string(LINE_LEN)
        self.current_highlight = ['_'] * len(self.current_line)
        self.current_input = ''


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

        self.update()

    def update(self):
        # Clear canvas
        self.cvs.delete('all')
        # Draw next line
        self.cvs.create_text(IDENT, IDENT,
                             anchor='nw',
                             text=self.text_state.next_line, font='Consolas')
        # Draw current line with current input and highlight
        last_x = IDENT
        for i in range(len(self.text_state.current_line)):
            if len(self.text_state.current_input) > i:
                # Draw symbols from input
                new_char = self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                                anchor='nw',
                                                text=self.text_state.current_input[i],
                                                font='Consolas')
                x1, y1, x2, y2 = self.cvs.bbox(new_char)
            else:
                # Draw symbols from generated text
                new_char = self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                                anchor='nw',
                                                text=self.text_state.current_line[i],
                                                font='Consolas', fill='gray')
                x1, y1, x2, y2 = self.cvs.bbox(new_char)
                # Draw cursor
                if i == len(self.text_state.current_input):
                    self.cvs.create_line(x1 + 1, y1 + 1, x1 + 1, y2 - 1, width=2)
            # Draw highlight
            highlight = self.text_state.current_highlight[i]
            if highlight == '+':  # Correct
                self.cvs.create_line(x1, y2, x2, y2, fill='lightgreen', width='2p')
                pass
            elif highlight == '-':  # Incorrect
                self.cvs.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline='', fill='red', width='2p')
                self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                     anchor='nw',
                                     text=self.text_state.current_input[i],
                                     font='Consolas',
                                     fill='gray')
                pass
            elif highlight == 'x':  # Deleted
                self.cvs.create_line(x1, y2, x2, y2, fill='red', width='2p')
                pass
            elif highlight == 'v':  # Fixed
                self.cvs.create_line(x1, y2, x2, y2, fill='orange', width='2p')
                pass
            last_x = x2 - 1
        # Draw prev line
        self.cvs.create_text(IDENT, IDENT + 2*LINE_HEIGHT,
                             anchor='nw',
                             text=self.text_state.prev_line, font='Consolas')

    def cvs_key_event(self, event):
        if event.keysym == 'BackSpace':
            self.text_state.drop_char()
        elif event.keysym == 'Return':
            if self.text_state.current_input == self.text_state.current_line:
                self.text_state.new_line()
        elif event.char is not None and \
                event.char != '' and event.char.isprintable():
            self.text_state.put_char(event.char)
        self.update()


def main():
    main_window = MainWindow()
    main_window.window.mainloop()


if __name__ == "__main__":
    main()
