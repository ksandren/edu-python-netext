#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
from classes.textstate import TextState

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

        self.lbl1 = Label(self.root, text='Choose language:')
        self.lbl1.grid(column=0, row=0)

        self.cb_lang = ttk.Combobox(self.root, values=['EN', 'RU'])
        self.cb_lang.grid(column=1, row=0)
        self.cb_lang.current(0)

        self.lbl2 = Label(self.root, text='Choose round time:')
        self.lbl2.grid(column=2, row=0)

        self.cb_round_time = ttk.Combobox(self.root, values=['1', '2', '3'])
        self.cb_round_time.grid(column=3, row=0)
        self.cb_round_time.current(0)

        self.btn_start = Button(self.root, text='Start', width=10, command=self.btn_start_clicked)
        self.btn_start.grid(column=4, row=0)

        self.cvs = Canvas(self.root, width=600, height=105, bg='white')
        self.cvs.grid(column=0, row=1, columnspan=5)
        self.cvs.bind('<Key>', self.cvs_key_event)

        self.timer()

    def update(self):
        raise NotImplementedError()

    def btn_start_clicked(self):
        self.cb_lang.config(state='disabled')
        self.cb_round_time.config(state='disabled')
        self.btn_start.config(state='disabled')
        self.text_state.set_lang(self.cb_lang.get())
        self.text_state.round_time = int(self.cb_round_time.get())
        self.cvs.focus_set()

    def round_finished(self):
        self.cb_lang.config(state='normal')
        self.cb_round_time.config(state='normal')
        self.btn_start.config(state='normal')
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
