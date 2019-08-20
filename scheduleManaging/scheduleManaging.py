#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pyperclip

from scheduleCreation import create_schedule
from scheduleTimeModification import modify_time
from scheduleTaskNameModification import modify_task_name


def get_task():
    # choose a task
    task_num = input(
        """1. create a schedule
        \r2. modify a schedule
        \r3. modify a task name
        \r4. copy schedule from txt
        \rwhat to do? >>> """)
    # input should be '1', '2', '3' and '4'
    while task_num not in ['1', '2', '3', '4'] or not task_num.isdigit():
        task_num = input("\rinput 1, 2, 3 or 4 only! >>> ")
    print()

    # str -> int
    task_num = int(task_num)

    return task_num


def copy_from_txt():
    with open("tmp.txt", encoding="utf-8") as f:
        pyperclip.copy(f.read())


def save_to_txt():
    schedule = pyperclip.paste()
    with open("tmp.txt", 'w', encoding="utf-8") as f:
        f.write(schedule)


def schedule_managing():
    task = get_task()

    if task == 1:
        create_schedule()
    if task == 2:
        modify_time()
    if task == 3:
        modify_task_name()
    if task == 4:
        copy_from_txt()

    save_to_txt()


if __name__ == '__main__':
    schedule_managing()
