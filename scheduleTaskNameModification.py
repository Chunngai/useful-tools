#!usr/bin/python env
# -*- coding: utf-8 -*-


from scheduleCommonFunc import input_
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import get_task_info
from scheduleCommonFunc import print_task_info_list
from scheduleCommonFunc import copy_to_clipboard
from scheduleCommonFunc import input_index


def name_modify(task_info_list_, task_index_, task_name_list_):
    # print task names of the specified index
    for i in range(len(task_name_list_)):
        print("({}) {}".format(i + 1, task_name_list_[i]))

    # get the index of the task name to be modified
    name_index = input_index("input the index of the task name to be modified >>> ", task_name_list_)

    # get a new name
    new_name = input("input the new name >>> ")

    # modified the name list
    task_info_list_[task_index_ - 1][3][name_index - 1] = new_name

    return task_info_list_


def modify_task_name():
    # receive data
    data = input_()

    # make data into a nested list
    task_info_list = generate_task_list(data)

    # ask how to modify
    task_index, task_name_list = get_task_info(task_info_list, 'n')

    # modify the task name
    task_info_list = name_modify(task_info_list, task_index, task_name_list)

    # print the modified schedule
    print_task_info_list(task_info_list)
    print()

    # copy to the clipboard
    print("modified schedule:")
    print('-' * 30)
    copy_to_clipboard(task_info_list)


if __name__ == '__main__':
    modify_task_name()
