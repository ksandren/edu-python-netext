#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk
from classes.textstate import TextState
from wsmgr import DICT_PATH
import os

IDENT = 5
LINE_HEIGHT = 20
FONT = ('Consolas', 14)
WIN_WIDTH = 650
WIN_HEIGHT = 150
SETTINGS_FILE = 'settings.txt'


def load_languages():
    result = os.listdir(DICT_PATH)
    return result


class MainWindow:
    def __init__(self):
        self.text_state = TextState()
        self.text_state.round_finished = self.round_finished

        self.root = tk.Tk()
        self.root.title('Not Enough Text')
        self.root.geometry(str(WIN_WIDTH) + 'x' + str(WIN_HEIGHT))
        self.root.minsize(WIN_WIDTH, WIN_HEIGHT)
        self.root.maxsize(WIN_WIDTH, WIN_HEIGHT)

        self.settings = dict()
        self.load_settings()
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

        self.translations = dict()
        self.language = self.settings.get('lang', 'RU')
        self.load_translations()

        self.lbl_ch_lang = tk.Label(self.root, text=self.translate('Choose language:'))
        self.lbl_ch_lang.grid(column=0, row=0)

        self.cb_lang = ttk.Combobox(self.root, values=load_languages(), state='readonly')
        self.cb_lang.grid(column=1, row=0)
        self.cb_lang.current(self.cb_lang['values'].index(self.settings.get('lang', 'RU')))
        self.cb_lang.bind("<<ComboboxSelected>>", self.change_lang)

        self.lbl_ch_time = tk.Label(self.root, text=self.translate('Choose round time:'))
        self.lbl_ch_time.grid(column=2, row=0)

        self.cb_round_time = ttk.Combobox(self.root, values=['1', '2', '3'], state='readonly')
        self.cb_round_time.grid(column=3, row=0)
        self.cb_round_time.current(self.cb_round_time['values'].index(self.settings.get('time', '1')))
        self.cb_round_time.bind("<<ComboboxSelected>>", self.change_round_time)

        self.btn_start = tk.Button(self.root, text=self.translate('Start'), width=10, command=self.btn_start_clicked)
        self.btn_start.grid(column=4, row=0)

        self.cvs = tk.Canvas(self.root, width=WIN_WIDTH, height=105, bg='white')
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
        self.cb_lang.config(state='readonly')
        self.cb_round_time.config(state='readonly')
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
        self.settings['lang'] = self.cb_lang.get()
        self.language = self.cb_lang.get()
        self.load_translations()
        self.lbl_ch_lang.config(text=self.translate('Choose language:'))
        self.lbl_ch_time.config(text=self.translate('Choose round time:'))
        self.btn_start.config(text=self.translate('Start'))

    def change_round_time(self, e):
        self.settings['time'] = self.cb_round_time.get()

    def load_settings(self):
        if os.path.isfile(SETTINGS_FILE):
            file = open(SETTINGS_FILE, 'r')
            for line in file:
                key, value = line[:-1].split('=')
                self.settings[key] = value
            file.close()
        if len(self.settings) == 0:
            self.settings['lang'] = 'RU'
            self.settings['time'] = '1'

    def save_settings(self):
        file = open(SETTINGS_FILE, 'w')
        for key in self.settings:
            file.write(key + '=' + self.settings[key] + '\n')
        file.close()

    def on_close(self):
        self.save_settings()
        self.root.destroy()
