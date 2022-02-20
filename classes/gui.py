#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
from classes.textstate import TextState
from wsmgr import DICT_PATH
import os

IDENT = 5
LINE_HEIGHT = 20
FONT = ('Consolas', 14)


class MainWindow:
    def __init__(self):
        self.text_state = TextState()
        self.text_state.round_finished = self.round_finished

        self.root = Tk()
        self.root.title("Not Enough Text")
        self.root.geometry('600x150')

        # TODO settings = self.load_settings()

        self.translations = dict()
        self.language = 'EN'  # settings['lang']
        self.load_translations()

        self.lbl1 = Label(self.root, text=self.translate('Choose language:'))
        self.lbl1.grid(column=0, row=0)

        self.cb_lang = ttk.Combobox(self.root, values=['EN', 'RU'])
        self.cb_lang.grid(column=1, row=0)
        self.cb_lang.current(0)
        self.cb_lang.bind("<<ComboboxSelected>>", self.change_lang)

        self.lbl2 = Label(self.root, text=self.translate('Choose round time:'))
        self.lbl2.grid(column=2, row=0)

        self.cb_round_time = ttk.Combobox(self.root, values=['1', '2', '3'])
        self.cb_round_time.grid(column=3, row=0)
        self.cb_round_time.current(0)

        self.btn_start = Button(self.root, text=self.translate('Start'), width=10, command=self.btn_start_clicked)
        self.btn_start.grid(column=4, row=0)

        self.cvs = Canvas(self.root, width=600, height=105, bg='white')
        self.cvs.grid(column=0, row=1, columnspan=5)
        self.cvs.bind('<Key>', self.cvs_key_event)
        self.draw_text = self.cvs.create_text

        self.timer()

    def update(self):
        raise NotImplementedError()

    def btn_start_clicked(self):
        if self.text_state.is_active():
            self.text_state.stop()
        else:
            self.cb_lang.config(state='disabled')
            self.cb_round_time.config(state='disabled')
            self.btn_start.config(text=self.translate('Stop'))
            self.text_state.set_lang(self.cb_lang.get())
            self.text_state.round_time = int(self.cb_round_time.get())
            self.cvs.focus_set()

    def round_finished(self):
        self.cb_lang.config(state='normal')
        self.cb_round_time.config(state='normal')
        self.btn_start.config(text=self.translate('Start'))
        self.btn_start.focus_set()

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
        self.root.after(100, self.timer)

    def translate(self, string):
        if string not in self.translations:
            self.add_template_to_translations(string)
        return self.translations[string]

    def load_translations(self):
        self.translations.clear()
        path = DICT_PATH
        if not os.path.isdir(path):
            os.mkdir(path)
        path += self.language
        if not os.path.isdir(path):
            os.mkdir(path)
        path += '/translations.txt'
        if os.path.isfile(path):
            file = open(path, 'r')
        else:
            file = open(path, 'w')
            file.close()
            return
        lines = [line.encode('cp1251').decode('u8') for line in file]
        file.close()
        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                self.translations[lines[i][:-1]] = lines[i + 1][:-1]

    def add_template_to_translations(self, string):
        self.translations[string] = string
        path = DICT_PATH + self.language + '/translations.txt'
        file = open(path, 'a')
        file.write(string + '\n')
        file.write(string + '\n')
        file.close()

    def change_lang(self, e):
        self.language = self.cb_lang.get()
        self.load_translations()
        self.lbl1.config(text=self.translate('Choose language:'))
        self.lbl2.config(text=self.translate('Choose round time:'))
        self.btn_start.config(text=self.translate('Start'))
