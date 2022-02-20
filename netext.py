#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time

from classes.gui import *
from classes.textstate import HighlightType as Ht


class Window(MainWindow):
    def draw_another_symbol(self, i, last_x):
        new_char = self.text_state.current_input[i]
        color = 'black'
        if new_char == '':
            new_char = self.text_state.current_line[i]
            color = 'gray'
        new_char_id = self.draw_text(last_x, IDENT + LINE_HEIGHT, anchor='nw',
                                     text=new_char, font=FONT, fill=color)
        return self.cvs.bbox(new_char_id)

    def draw_highlight(self, i, last_x, x1, y1, x2, y2):
        highlight = self.text_state.current_highlight[i]
        if highlight == Ht.CORRECT:  # '+':  # Correct
            self.cvs.create_line(x1, y2, x2, y2,
                                 fill='lightgreen', width='2p')
        elif highlight == Ht.INCORRECT:  # '-':  # Incorrect
            self.cvs.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                      outline='', fill='red', width='2p')
            self.draw_another_symbol(i, last_x)
            self.cvs.create_rectangle(x1 + 1, y1 + 1 - LINE_HEIGHT * 2 / 3,
                                      x2 - 1, y2 - 1 - LINE_HEIGHT * 2 / 3,
                                      outline='', fill='lightblue',
                                      width='2p')
            self.draw_text(last_x, IDENT + LINE_HEIGHT * 1 / 3, anchor='nw',
                           text=self.text_state.current_line[i], font=FONT,
                           fill='black')
        elif highlight == Ht.DELETED:  # 'x':  # Deleted
            self.cvs.create_line(x1, y2, x2, y2, fill='red', width='2p')
        elif highlight == Ht.FIXED:  # 'v':  # Fixed
            self.cvs.create_line(x1, y2, x2, y2, fill='orange', width='2p')

    def draw_stat(self):
        stat = self.translate('Keys statistics: useful: ') + str(self.text_state.useful_keys) + \
               self.translate(' useless: ') + str(self.text_state.useless_keys) + \
               self.translate(' speed: ') + str(round(self.text_state.input_speed)) + 'cbm'
        self.draw_text(IDENT, IDENT + 3 * LINE_HEIGHT, anchor='nw',
                       text=stat, font=FONT, fill='green')
        if self.text_state.round_started:
            round_timer = self.text_state.round_time * 60
            round_timer -= (time.time_ns() - self.text_state.start_time_ns) / 1_000_000_000
            m = round(round_timer) // 60
            s = round(round_timer) % 60
            self.draw_text(IDENT, IDENT + 4 * LINE_HEIGHT, anchor='nw',
                           text='Time: ' + f'{m:02d}:{s:02d}', font=FONT, fill='green')

    def update(self):
        # Clear canvas
        self.cvs.delete('all')
        # Draw next line
        self.draw_text(IDENT, IDENT + 2*LINE_HEIGHT, anchor='nw',
                       text=self.text_state.next_line, font=FONT)
        # Draw current line with current input and highlight
        last_x = IDENT
        for i in range(len(self.text_state.current_line)):
            x1, y1, x2, y2 = self.draw_another_symbol(i, last_x)
            if self.text_state.cursor_pos == i:
                self.cvs.create_line(x1 + 1, y1 + 1, x1 + 1, y2 - 1, width=2)
            # Draw highlight
            self.draw_highlight(i, last_x, x1, y1, x2, y2)
            last_x = x2 - 1
        # Draw prev line
        self.draw_text(IDENT, IDENT, anchor='nw',
                       text=self.text_state.prev_line, font=FONT)
        # Draw statistics
        self.draw_stat()


def main():
    main_window = Window()
    main_window.root.mainloop()


if __name__ == "__main__":
    main()
