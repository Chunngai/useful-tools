#!usr/bin/python env
# -*- coding: utf-8 -*-


from scheduleCreation import create_schedule
from scheduleTimeModification import modify_time
from scheduleTaskNameModification import modify_task_name


def get_task():
    # choose a task
    task_num = input("1. create a schedule\n2. modify a schedule\n3. modify a task name\nwhat to do? >>> ")
    # input should be '1', '2' and '3'
    while task_num not in ['1', '2', '3'] or not task_num.isdigit():
        task_num = input("input 1, 2 or 3 only! >>> ")

    # str -> int
    task_num = int(task_num)

    return task_num


def schedule_managing():
    task = get_task()

    if task == 1:
        create_schedule()
    if task == 2:
        modify_time()
    if task == 3:
        modify_task_name()


if __name__ == '__main__':
    schedule_managing()
