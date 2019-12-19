#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itchat
import sys
import os
import re


def send_files(src_file_path):
    print("sending file {}".format(src_file_path))

    itchat.send_file(src_file_path, toUserName="filehelper")

    print("done")


def receive_files(dest_file_path="/home/neko/Downloads/"):
    print("receiving files")

    if dest_file_path[-1] != "/":
        dest_file_path += "/"

    @itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
    def download_files(msg):
        msg['Text'](dest_file_path + msg['FileName'])
        print("received {}".format(msg['FileName']))

    itchat.run()


def login():
    # itchat.auto_login(hotReload=True)
    itchat.auto_login()


if __name__ == '__main__':
    # python3 wechat_file_manager.py -s src_file_path: send
    # python3 wechat_file_manager.py -r dest_file_path: download
    if sys.argv[1] in ["-s", "--send"]:
        try:
            if os.path.exists(sys.argv[2]):
                login()
                send_files(sys.argv[2])
            else:
                raise FileNotFoundError()
        except IndexError:
            print("file path cannot be empty")
            exit(1)
        except FileNotFoundError:
            print("file path does not exist")
            exit(1)
    elif sys.argv[1] in ["-r", "--receive"]:
        try:
            if os.path.exists(sys.argv[2]):
                login()
                receive_files(sys.argv[2])
            else:
                raise FileNotFoundError()
        except IndexError:
            login()
            receive_files()
        except FileNotFoundError:
            print("file path does not exist")
            exit(1)
    else:
        print("invalid mode")
