#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scheduleCommonFunc import input_
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import get_task_info
from scheduleCommonFunc import print_task_info_list
from scheduleCommonFunc import input_index


def get_task():
    task = input("modify a task name(m) or add(a) a task name? (m/a) >>> ")
    # check if the input is valid
    while task not in ['a', 'm']:
        task = input("input 'a' or 'm' only! input again >>> ")

    return task


def name_modify(task_info_list_, task_index_, task_name_list_):
    # print task names of the specified index
    for i in range(len(task_name_list_)):
        print("({}){} {}".format(i + 1, ' ' if len(str(i + 1)) == 1 else '', task_name_list_[i]))

    # get the index of the task name to be modified
    name_index = input_index("input the index of the task name to be modified >>> ", task_name_list_)

    # get a new name
    new_name = input("input the new name >>> ")

    # capitalize the first letter
    new_name = new_name[0].capitalize() + new_name[1:]

    # modified the name list
    task_info_list_[task_index_ - 1][3][name_index - 1] = new_name

    return task_info_list_


def name_add(task_info_list_, task_index_):
    new_task_name = input("input the new task name >>> ")
    # check if the input is empty
    while not new_task_name:
        new_task_name = input("the new task name cannot be empty! input again >>> ")

    # append the new name to the task list
    task_info_list_[task_index_ - 1][3].append(new_task_name)

    return task_info_list_


def modify_task_name():
    # receive data
    data = input_()

    # make data into a nested list
    task_info_list = generate_task_list(data)

    # get the task to be modified
    task_index, task_name_list = get_task_info(task_info_list, 'n')

    # ask what to do
    task = get_task()

    if task == 'm':
        # modify the task name
        task_info_list = name_modify(task_info_list, task_index, task_name_list)
    else:
        # add a task name
        task_info_list = name_add(task_info_list, task_index)

    return task_info_list


if __name__ == '__main__':
    modify_task_name()
