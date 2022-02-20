#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time

from classes.gui import *


class Window(MainWindow):
    def update(self):
        draw_text = self.cvs.create_text
        # Clear canvas
        self.cvs.delete('all')
        # Draw next line
        draw_text(IDENT, IDENT, anchor='nw',
                  text=self.text_state.next_line, font=FONT)
        # Draw current line with current input and highlight
        last_x = IDENT
        for i in range(len(self.text_state.current_line)):
            new_char = self.text_state.current_input[i]
            color = 'black'
            if new_char == '':
                new_char = self.text_state.current_line[i]
                color = 'gray'
            new_char_id = draw_text(last_x, IDENT + LINE_HEIGHT, anchor='nw',
                                    text=new_char, font=FONT, fill=color)
            x1, y1, x2, y2 = self.cvs.bbox(new_char_id)
            if self.text_state.cursor_pos == i:
                self.cvs.create_line(x1 + 1, y1 + 1, x1 + 1, y2 - 1, width=2)
            # Draw highlight
            highlight = self.text_state.current_highlight[i]
            if highlight == '+':  # Correct
                self.cvs.create_line(x1, y2, x2, y2,
                                     fill='lightgreen', width='2p')
            elif highlight == '-':  # Incorrect
                self.cvs.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                          outline='', fill='red', width='2p')
                draw_text(last_x, IDENT + LINE_HEIGHT, anchor='nw',
                          text=self.text_state.current_input[i],
                          font=FONT, fill='black')
                self.cvs.create_rectangle(x1 + 1, y1 + 1 - LINE_HEIGHT * 2/3,
                                          x2 - 1, y2 - 1 - LINE_HEIGHT * 2/3,
                                          outline='', fill='lightblue',
                                          width='2p')
                draw_text(last_x, IDENT + LINE_HEIGHT * 1/3, anchor='nw',
                          text=self.text_state.current_line[i], font=FONT,
                          fill='black')
            elif highlight == 'x':  # Deleted
                self.cvs.create_line(x1, y2, x2, y2, fill='red', width='2p')
            elif highlight == 'v':  # Fixed
                self.cvs.create_line(x1, y2, x2, y2, fill='orange', width='2p')
            last_x = x2 - 1
        # Draw prev line
        draw_text(IDENT, IDENT + 2*LINE_HEIGHT, anchor='nw',
                  text=self.text_state.prev_line, font=FONT)
        stat = 'Keys statistics: useful: ' + str(self.text_state.useful_keys) +\
               ' useless: ' + str(self.text_state.useless_keys) +\
               ' speed: ' + str(round(self.text_state.input_speed)) + 'spm'
        draw_text(IDENT, IDENT + 3 * LINE_HEIGHT, anchor='nw',
                  text=stat, font=FONT, fill='green')
        if self.text_state.round_started:
            round_timer = self.text_state.round_time * 60
            round_timer -= (time.time_ns() - self.text_state.start_time_ns) / 1_000_000_000
            m = round(round_timer) // 60
            s = round(round_timer) % 60
            draw_text(IDENT, IDENT + 4 * LINE_HEIGHT, anchor='nw',
                      text='Time: ' + f'{m:02d}:{s:02d}', font=FONT, fill='green')


def main():
    main_window = Window()
    main_window.root.mainloop()


if __name__ == "__main__":
    main()
