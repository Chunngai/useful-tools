#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itchat
import sys
import os


def send_files(src_file_path):
    itchat.send_file(src_file_path, toUserName="filehelper")


def receive_files(dest_file_path="/home/neko/Downloads/"):
    if dest_file_path[-1] != "/":
        dest_file_path += "/"

    @itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
    def download_files(msg):
        msg['Text'](dest_file_path + msg['FileName'])

    itchat.run()


def login():
    # itchat.auto_login(hotReload=True)
    itchat.auto_login()


if __name__ == '__main__':
    # python3 wechat_file_manager.py -s src_file_path: send
    # python3 wechat_file_manager.py -r dest_file_path: download
    if len(sys.argv) != 3:
        print("invalid input! usage: python3 wechat_file_manager.py [mode] [file_path]")
        exit(1)

    if os.path.exists(sys.argv[2]):
        if sys.argv[1] in ["-s", "--send"]:
            login()
            send_files(sys.argv[2])
        elif sys.argv[1] in ["-r", "--receive"]:
            login()
            receive_files(sys.argv[2])
        else:
            print("invalid mode!")
    else:
        print("invalid path!")
