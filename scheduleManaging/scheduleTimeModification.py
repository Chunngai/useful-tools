#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from scheduleCommonFunc import print_task_info_list
from scheduleCommonFunc import input_
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import get_task_info
from scheduleCommonFunc import add_time
from scheduleCommonFunc import minus_time
from scheduleCommonFunc import get_delta_time
from scheduleCommonFunc import compare_time
from scheduleCommonFunc import h_to_min


def get_modified_time(start_time_, end_time_):
    # match input and return the result
    def get_rst(prompt, t_):
        pat_1 = re.compile(r"^\d{4}$")  # forms like 0800
        pat_2 = re.compile(r"^([+\-]?)(\d+)\s?(min?|h?)$")  # forms like +30 min, -2h
        pat_3 = re.compile(r"^/$")

        input_start = input(prompt)
        rst_1_ = pat_1.search(input_start)
        rst_2_ = pat_2.search(input_start)
        rst_3_ = pat_3.search(input_start)
        if t_ != 'd':
            rst_3_ = None

        while not (rst_1_ or rst_2_ or rst_3_):
            input_start = input("invalid input! input again >>> ")
            rst_1_ = pat_1.search(input_start)
            rst_2_ = pat_2.search(input_start)
            rst_3_ = pat_3.search(input_start)
            if t_ != 'd':
                rst_3_ = None

        # return the number and the result of the pattern which matches the str
        rst_list = [rst_1_, rst_2_, rst_3_]
        for i_ in range(len(rst_list)):
            if rst_list[i_]:
                return i_, rst_list[i_]

    # return modified time
    def get_modified_time_inner(rst_, original_time_):
        delta_time_ = int(rst_.group(2))

        # h -> min
        delta_time_ = h_to_min(rst.group(3), delta_time_)

        # add/minus
        if rst.group(1) in ['+', '']:
            modified_time_ = add_time(original_time_, delta_time_)
        else:
            modified_time_ = minus_time(original_time_, delta_time_)

        return modified_time_

    flag = ''
    # if a new duration or an end time with the hhmm form is given, flag = 1 and the task will get an end time
    if end_time_ == -1:
        flag = 0

    # modify the start time
    i, rst = get_rst("""How to modify the start time?
     valid input i): hhmm. such as 0830
     valid input ii): ([+\-]?)(\d+)\s?(min|h?). such as +30min, -2 h, 30
     * 30 -> 30min, 20 -> 20min
     >>> """, 's')
    if i == 0:  # the input is something like 0800
        modified_start_time = int(rst.group(0))
    else:  # the input is something like +2 h
        modified_start_time = get_modified_time_inner(rst, start_time_)

    # modify the end time
    input_end = input("modify duration or end time >>> ")
    while input_end not in ['d', 'e']:
        input_end = input("invalid input! input again >>> ")
    t = input_end

    if input_end == 'd':
        # modify the end time by modifying the duration
        i, rst = get_rst("How to modify the duration? >>> ", t)

        # calculate duration
        duration = get_delta_time(end_time_, start_time_)

        if i == 1:  # the input is something like +30 min
            sign = rst.group(1)  # the sign(if there is one) before digits
            delta_time = int(rst.group(2))

            if sign == '+':
                modified_duration = duration + delta_time
            elif sign == '-':
                modified_duration = duration - delta_time
            else:
                modified_duration = delta_time

                # a duration is given to a task which originally has not an end time
                flag = 1
        else:  # the input is /
            modified_duration = duration

        modified_end_time = add_time(modified_start_time, modified_duration)
    else:
        # modify the end time directly
        i, rst = get_rst("""How to modify the end time?
     valid input i): hhmm. such as 0830
     valid input ii): ([+\-]?)(\d+)\s?(min|h?). such as +30min, -2 h, 30
     * 30 -> 30min, 20 -> 20min
     >>> """, t)
        if i == 0:  # the input is something like 0800
            modified_end_time = int(rst.group(0))

            # an end time is given to a task which originally has not one
            flag = 1
        else:  # the input is something like +30 min
            modified_end_time = get_modified_time_inner(rst, end_time_)

    if flag == 0:
        # the task originally has not an end time and a duration or an end time is not given
        modified_end_time = -1

    # modify the duration
    modified_duration = 0
    if modified_end_time != -1:
        modified_duration = get_delta_time(modified_end_time, modified_start_time)

    print("modified_start_time: {}, modified_end_time: {}\n".format(modified_start_time, modified_end_time))
    return modified_start_time, modified_end_time, modified_duration


def modify_remaining(task_index_, task_info_list_, delta_time_, modified_start_time_, modified_end_time_,
                     modified_duration_):
    new_task_info_list = task_info_list_.copy()

    # add modified start time, end time and duration to the list
    new_task_info_list[task_index_ - 1][0] = modified_start_time_
    new_task_info_list[task_index_ - 1][1] = modified_end_time_
    new_task_info_list[task_index_ - 1][2] = modified_duration_

    # the parameter original_time_ in add_time() and minus_time() is greater than or equal to 0
    delta_time_parameter = abs(delta_time_)
    # modify the time of tasks which are after the task having been modified
    for i in range(len(task_info_list_)):
        # find the task from which the time is to be modified
        if i == task_index_ - 1:
            # modify the remaining tasks
            for j in range(i + 1, len(task_info_list_)):
                # get start time and end time of every task
                task = task_info_list_[j]
                start_time_ = task[0]
                end_time_ = task[1]

                # calculate modified start time
                if delta_time_ >= 0:
                    start_time_modified = add_time(start_time_, delta_time_parameter)
                else:
                    start_time_modified = minus_time(start_time_, delta_time_parameter)
                # calculate modified end time
                if delta_time_ >= 0:
                    end_time_modified = add_time(end_time_, delta_time_parameter)
                else:
                    end_time_modified = minus_time(end_time_, delta_time_parameter)
                if end_time_ == -1:
                    end_time_modified = -1

                # update the schedule
                task_ = new_task_info_list[j]
                task_[0] = start_time_modified
                task_[1] = end_time_modified

    print_task_info_list(new_task_info_list)

    return new_task_info_list


def modify_time():
    # receive data
    data = input_()

    # make data into a nested list
    task_info_list = generate_task_list(data)

    # ask how to modify
    task_index, start_time, end_time = get_task_info(task_info_list, 't')
    modified_start_time, modified_end_time, modified_duration = get_modified_time(start_time, end_time)

    while end_time != -1 and compare_time(modified_end_time, modified_start_time) == 0:
        print("modified end time is earlier than modified start time! input data again!")
        modified_start_time, modified_end_time, modified_duration = get_modified_time(start_time, end_time)

    # calculate modified_time - end_time
    delta_time = get_delta_time(modified_end_time, end_time)
    if end_time == -1:
        delta_time = 0

    # modify schedule
    new_task_info_list = modify_remaining(task_index, task_info_list, delta_time,
                                          modified_start_time, modified_end_time, modified_duration)

    return new_task_info_list


if __name__ == '__main__':
    modify_time()
