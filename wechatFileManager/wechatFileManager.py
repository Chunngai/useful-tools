#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itchat
from tkinter.filedialog import askopenfilename


def send_to_wechat_file_manager():
    # select files to be sent
    askopenfilename()

    # log in
    itchat.auto_login()

    # send files


if __name__ == '__main__':
    send_to_wechat_file_manager()
