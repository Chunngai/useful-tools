#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from scheduleCommonFunc import add_time
from scheduleCommonFunc import get_delta_time
from scheduleCommonFunc import print_task_info_list
from scheduleCommonFunc import h_to_min


def print_task(task):
    # get the start time
    start_time = task[0]
    # get the duration
    duration = task[2]
    # get the end time
    end_time = task[1]
    # get the task list
    task_list = task[3]

    start_time_str = str(start_time).zfill(4)
    if duration == -1:
        duration = '/'

    end_time_str = str(end_time).zfill(4)
    if end_time == -1:
        end_time_str = '/'

    print("start time: {}, end time: {}, duration: {}, tasks: {}".format(start_time_str,
                                                                         end_time_str, duration,
                                                                         task_list))


def create_schedule():
    print("Creating schedule ...\n")

    # [start time, end time, duration, [task name 1, task name 2...]]
    task_info_list = []  # store task info. time info is int and the name is str.
    end_time = ''  # store the end time of the task which is input in the last loop
    task_num = 0  # count the number of tasks

    # pattern of valid input
    pat_1 = re.compile(r"^(\d{1,3})\s?(min?|h?)(\s+\+(.*))?$")
    pat_2 = re.compile(r"^[012]\d[012345]\d$")
    pat_3 = re.compile(r"^finished$")
    pat_4 = re.compile(r"^redo$")
    pat_5 = re.compile(r"^$")

    while True:
        # get the start time
        s_input = input("Input the start time >>> ")
        rst_s_1 = pat_1.search(s_input)
        if end_time == -1:  # force to set a start time
            rst_s_1 = None
        rst_s_2 = pat_2.search(s_input)
        rst_q = pat_3.search(s_input)
        rst_r = pat_4.search(s_input)

        redo_flag = 0
        while not ((rst_s_1 and task_num > 0) or rst_s_2 or rst_q) or rst_r:
            if rst_r:
                if redo_flag == 0:  # in a loop statements in the if statement can be implemented only once
                    # print what have input the last time
                    print("the input last time:")

                    pat = re.compile(r"Anything")
                    if task_num > 0 and pat.search(task_info_list[task_num - 2][3][0]):
                        # print the automatically generated "Anything (+...)" task
                        print_task(task_info_list[task_num - 2])
                    print_task(task_info_list[task_num - 1])

                    task_num -= 1
                    # record the end time of the task which is input before the wrongly input task
                    end_time = task_info_list[task_num - 1][1]
                    # delete the info of the task which is wrongly input
                    task_info_list.pop()

                    # delete the automatically generated "Anything (+...)" task
                    pat = re.compile(r"Anything")
                    if task_num > 0 and pat.search(task_info_list[task_num - 1][3][0]):
                        task_num -= 1
                        end_time = task_info_list[task_num - 1][1]
                        task_info_list.pop()

                redo_flag = 1
                s_input = input("input the start time again >>> ")
            else:
                s_input = input("invalid input! input the start time again! >>> ")

            rst_s_1 = pat_1.search(s_input)
            if end_time == -1:  # force to set a start time
                rst_s_1 = None
            rst_s_2 = pat_2.search(s_input)
            rst_q = pat_3.search(s_input)
            rst_r = pat_4.search(s_input)

        if rst_s_1:  # the input matches pat_1
            duration_btw = int(rst_s_1.group(1))

            # h -> min
            duration_btw = h_to_min(rst_s_1.group(2), duration_btw)

            start_time = add_time(end_time, duration_btw)

            if int(rst_s_1.group(1)):
                # store info
                try:
                    task_info_list.append([end_time, start_time, duration_btw, ["Anything +" + rst_s_1.group(4)]])
                except:
                    task_info_list.append([end_time, start_time, duration_btw, ["Anything"]])
                # count ++
                task_num += 1
        elif rst_s_2:  # the input matches pat_2
            start_time = int(rst_s_2.group(0))
        elif rst_q:  # the input matches pat_3
            break

        # get the end time
        e_input = input("Input the duration or the end time >>> ")
        rst_d = pat_1.search(e_input)
        rst_e = pat_2.search(e_input)
        rst_n = pat_5.search(e_input)

        while not (rst_d or rst_e or rst_n):
            e_input = input("invalid input! input the duration or the end time again! >>> ")
            rst_d = pat_1.search(e_input)
            rst_e = pat_2.search(e_input)
            rst_n = pat_5.search(e_input)

        if rst_d:  # the input matches pat_1
            duration = int(rst_d.group(1))
            
            # h -> min
            duration = h_to_min(rst_d.group(2), duration)

            end_time = add_time(start_time, duration)
        elif rst_e:  # the input matches pat_2
            end_time = int(rst_e.group(0))
            duration = get_delta_time(end_time, start_time)
        else:  # matches pat_5
            end_time = -1
            duration = -1

        # get task names
        task_input = input("Input task names >>> ")
        while not task_input.strip():
            task_input = input("The task name is empty! Input again >>> ")

        task_list = re.split(r"\s*/\s*", task_input)
        # Capitalize the first letter of every task name
        task_list = [task_name[0].upper() + task_name[1:] for task_name in task_list if len(task_name) > 0]

        # store info
        # schedule_str += "{}-{} {}\n".format(start_time_str, end_time_str, task_name)
        task_info_list.append([start_time, end_time, duration, task_list])
        # count ++
        task_num += 1

        # show info of the current task
        print_task(task_info_list[-1])

        # print the whole schedule
        print('.' * 50)
        print_task_info_list(task_info_list)
        print('.' * 50)
        print()

    return task_info_list


if __name__ == '__main__':
    create_schedule()
