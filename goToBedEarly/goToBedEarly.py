#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import datetime
import time


def check_time():
    # get current_time
    current_time = datetime.datetime.now().strftime("%H%M")

    # time to go to bed
    go_to_bed_time = datetime.time(0, 0).strftime("%H%M")

    # compare
    if int(go_to_bed_time) <= int(current_time) <= int("0200"):
        return True
    else:
        return False


def go_to_bed_early_win(count_):
    # create a win
    win = tk.Tk()

    # title
    win.title("GO TO BED NOW!!!")

    # label
    tk.Label(win, text="GO TO BED NOW!!!", font=("Calibri", 20), width=100, height=2).pack()

    # size and align(centered)
    width = 300
    height = 150
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    align_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)
    win.geometry(align_str)

    # size immutable
    win.resizable(False, False)

    # frame
    frame = tk.Frame(win)
    frame.pack()

    wait_time = tk.IntVar()  # store time to wait

    if count_ <= 3:  # click "05 min" or "10 min" for 3 times at most
        # OK button
        frame_1 = tk.Frame(frame)
        frame_1.pack(side=tk.LEFT, padx=25)

        tk.Button(frame_1, text="OK", width=5, height=1, command=win.quit).pack()

        # time selection button
        frame_2 = tk.Frame(frame)
        frame_2.pack(side=tk.RIGHT, padx=25)

        # select time after which the win will pop-up again
        frame_3 = tk.Frame(frame_2)
        frame_3.pack(side=tk.TOP, pady=3)

        five_min = tk.Radiobutton(frame_3, text="05 min", variable=wait_time, value=5)
        five_min.grid(row=0, column=0)

        five_min_button = tk.Button(frame_3, text="OK", command=win.quit)
        five_min_button.grid(row=0, column=1)

        frame_4 = tk.Frame(frame_2)
        frame_4.pack(side=tk.BOTTOM, pady=3)

        ten_min = tk.Radiobutton(frame_4, text="10 min", variable=wait_time, value=10)
        ten_min.grid(row=0, column=0)

        ten_min_button = tk.Button(frame_4, text="OK", command=win.quit)
        ten_min_button.grid(row=0, column=1)
    else:
        tk.Button(frame, text="OK", command=lambda: tk.messagebox.showwarning(title="SLEEP NOW!",
                                                                              message="SLEEP NOW!")).pack()

    # mainloop
    win.mainloop()
    try:
        win.destroy()
    except:
        pass

    # clicked "OK" only: 1 min
    wait_time_int = int(wait_time.get())
    if wait_time_int == 0:
        wait_time_int = 1

    return wait_time_int


def go_to_bed_early():
    # check time. the win will pop-up after 00:00
    while not check_time():
        pass

    # pop-up the win
    count = 0  # count times. make the win pop-up after 5 min or 10 min for 3 times at most.
    while True:
        count += 1

        # pop-up the win
        wait_time = go_to_bed_early_win(count)

        # by default wait for 1 min and pop-up again
        time.sleep(wait_time * 60)


if __name__ == '__main__':
    go_to_bed_early()
