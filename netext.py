#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import random
from tkinter import *
import wsmgr
import locale


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
        self.current_line = str_gen.gen_rand_string(80)
        self.next_line = str_gen.gen_rand_string(80)
        self.current_input = ''

    def key_pressed(self, event):
        if event.keysym == 'BackSpace':
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
        elif event.char is not None and event.char.isprintable():
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
        self.cvs.create_text(400, 100,
                             text=self.text_state.next_line, font='Consolas')
        self.cvs.create_text(400, 120,
                             text=self.text_state.current_line, font='Consolas')
        self.cvs.create_text(400, 140,
                             text=self.text_state.current_input, font='Consolas')

    def cvs_key_event(self, event):
        self.text_state.key_pressed(event)
        self.update()


def main():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF8')
    main_window = MainWindow()
    main_window.window.mainloop()


if __name__ == "__main__":
    main()
