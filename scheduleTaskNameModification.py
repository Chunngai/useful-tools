#!usr/bin/python env
# -*- coding: utf-8 -*-


from scheduleCommonFunc import input_
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import get_task_info


def modify_task_name():
    # receive data
    data = input_()

    # make data into a nested list
    task_info_list = generate_task_list(data)

    # ask how to modify
    task_index, task_name_list = get_task_info(task_info_list, 'n')


if __name__ == '__main__':
    modify_task_name()
