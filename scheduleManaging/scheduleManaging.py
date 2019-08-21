#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pyperclip
import itchat

from scheduleCreation import create_schedule
from scheduleTimeModification import modify_time
from scheduleTaskNameModification import modify_task_name
from scheduleCommonFunc import copy_to_clipboard
from scheduleCommonFunc import generate_schedule_str
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import print_task_info_list


def get_task():
    # choose a task
    task_num = input(
        """1. create a schedule
        \r2. modify time of the schedule
        \r3. modify/add a task name
        \r4. copy schedule from txt
        \r5. sent to chat
        \rwhat to do? >>> """)
    # input should be '1', '2', '3', '4' and '5'
    while task_num not in ['1', '2', '3', '4', '5'] or not task_num.isdigit():
        task_num = input("\rinput 1, 2, 3, 4 or 5 only! >>> ")
    print()

    # str -> int
    task_num = int(task_num)

    return task_num


def copy_from_txt():
    with open("tmp.txt", encoding="utf-8") as f:
        pyperclip.copy(f.read())


def save_to_txt_word():
    schedule = pyperclip.paste()
    with open("tmp.txt", 'w', encoding="utf-8") as f:
        f.write(schedule)


def send_to_chat():
    # get schedule str from tmp.txt
    with open("tmp.txt", encoding="utf-8") as f:
        schedule_str = f.read()

    # generate task info list
    task_info_list = generate_task_list(schedule_str)

    # get schedule str
    schedule_str_ = generate_schedule_str(task_info_list, 'w')

    # log in
    itchat.auto_login()

    # send the schedule
    itchat.send(schedule_str_, toUserName="filehelper")


def schedule_managing():
    task = get_task()
    task_info_list = []

    if task == 1:
        task_info_list = create_schedule()
    if task == 2:
        task_info_list = modify_time()
    if task == 3:
        task_info_list = modify_task_name()
    if task == 4:
        copy_from_txt()
    if task == 5:
        send_to_chat()

    if task in range(1, 4):
        print()

        # print the schedule
        print("new schedule:")
        print('-' * 30)
        print_task_info_list(task_info_list)

        # copy to the clipboard
        copy_to_clipboard(task_info_list)

        # save the schedule to the tmp.txt file
        save_to_txt_word()


if __name__ == '__main__':
    schedule_managing()
