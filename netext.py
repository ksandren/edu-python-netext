#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
from tkinter import *
import wsmgr

IDENT = 5
LINE_LEN = 60
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
        str_gen = StringGenerator('RU')
        self.current_line = str_gen.gen_rand_string(LINE_LEN)
        self.next_line = str_gen.gen_rand_string(LINE_LEN)
        self.current_input = ''
        self.current_highlight = '_' * (len(self.current_line) + 1)

    def key_pressed(self, event):
        if event.keysym == 'BackSpace':
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
                ci_len = len(self.current_input)
                self.current_highlight =\
                    self.current_highlight[:ci_len] +\
                    'x' + self.current_highlight[ci_len + 1:]

        elif event.char is not None and event.char.isprintable():
            ci_len = len(self.current_input)
            if ci_len >= len(self.current_line):
                return
            if self.current_line[ci_len] == event.char:
                if self.current_highlight[ci_len] == '_':
                    self.current_highlight =\
                        self.current_highlight[:ci_len] +\
                        '+' + self.current_highlight[ci_len + 1:]
                else:
                    self.current_highlight =\
                        self.current_highlight[:ci_len] +\
                        'v' + self.current_highlight[ci_len + 1:]
            else:
                self.current_highlight =\
                    self.current_highlight[:ci_len] +\
                    '-' + self.current_highlight[ci_len + 1:]
            self.current_input += event.char


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
        self.cvs.delete('all')
        self.cvs.create_text(IDENT, IDENT,
                             anchor='nw',
                             text=self.text_state.next_line, font='Consolas')
        last_x = IDENT
        for i in range(len(self.text_state.current_line)):
            if len(self.text_state.current_input) > i:
                new_char = self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                                anchor='nw',
                                                text=self.text_state.current_input[i],
                                                font='Consolas')
                x1, y1, x2, y2 = self.cvs.bbox(new_char)
                self.cvs.create_line(x1, y2 + 1, x2, y2 + 1)
            else:
                new_char = self.cvs.create_text(last_x, IDENT + LINE_HEIGHT,
                                                anchor='nw',
                                                text=self.text_state.current_line[i],
                                                font='Consolas')
                x1, y1, x2, y2 = self.cvs.bbox(new_char)
            last_x = x2 - 1

        self.cvs.create_text(IDENT, IDENT + 2*LINE_HEIGHT,
                             anchor='nw',
                             text=self.text_state.current_highlight, font='Consolas')

    def cvs_key_event(self, event):
        self.text_state.key_pressed(event)
        self.update()


def main():
    main_window = MainWindow()
    main_window.window.mainloop()


if __name__ == "__main__":
    main()
