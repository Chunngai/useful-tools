#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math

import pyperclip


def print_task_info_list(task_info_list_):
    for i in range(len(task_info_list_)):
        task = task_info_list_[i]  # for every task

        # get start time, end time, , duration, task name
        start_time = str(task[0]).zfill(4)
        duration = task[2]
        if task[2] == -1:
            duration = ''
        end_time = str(task[1]).zfill(4)
        if task[1] == -1:
            end_time = ''
        task_name_list = task[3]

        # print (i) hhmm-(hhmm) task_name(the first one)
        print("({}){} {}-{} {} {}".format(i + 1, ' ' if len(str(i + 1)) == 1 else '', start_time, end_time, duration,
                                          task_name_list[0]))

        # print other tasks(if there are)
        for j in range(1, len(task_name_list)):
            print(' ' * (16 + len(str(i))), task_name_list[j])


def copy_to_clipboard(task_info_list_):
    schedule_str = ''
    for i in range(len(task_info_list_)):
        task = task_info_list_[i]

        # get start time, end time, duration, task names
        start_time = str(task[0]).zfill(4)
        duration = task[2]
        if task[2] == -1:
            duration = ''
        end_time = str(task[1]).zfill(4)
        if task[1] == -1:
            end_time = ''
        task_name_list = task[3]

        # concatenation
        schedule_str += ("{}-{} {} {}\n".format(start_time, end_time, duration, task_name_list[0]))

        for j in range(1, len(task_name_list)):
            schedule_str += (' ' * 13 + task_name_list[j] + '\n')

    # copy the created schedule to the clipboard
    pyperclip.copy(schedule_str)
    print(schedule_str)


def input_():
    print("input data:")

    stop_word = ''  # stop receiving data when stop_word is input
    input_str = ''  # the parameter concatenate input of multiple lines
    # receive data of multiple lines
    for line in iter(input, stop_word):
        input_str += line + '\n'

    return input_str


def generate_task_list(data_):
    # split the str with '\n'
    input_list = data_.split('\n')[:-1]

    # get time and tasks
    task_info_list = []
    # matches hhmm(-)hhmm task_name
    # pat = re.compile(r"(\d+)\-(\d*)\s?(.*)")
    pat = re.compile(r"(- \[ ] )?((\d+)-(\d*))?\s*(\d+)?\s*(.*)")
    for i in range(len(input_list)):
        rst = pat.search(input_list[i])

        # get start time, end time, duration, task name
        if rst.group(2):
            start_time = 0
            duration = 0
            end_time = 0
            if rst.group(3):
                start_time = int(rst.group(3))
            if rst.group(4):
                end_time = int(rst.group(4))
            if rst.group(3) and not rst.group(4):  # like 2110-
                end_time = -1
            if rst.group(5):
                duration = int(rst.group(5))
            else:  # like 2110-
                duration = -1
            task_name_list = [rst.group(6)]
            task_info_list.append([start_time, end_time, duration, task_name_list])
        else:
            task_info_list[len(task_info_list) - 1][3].append(rst.group(6))

    return task_info_list


def input_index(prompt_, list_):
    index_input = input(prompt_)

    while True:
        if not str(index_input).isdigit():
            index_input = input("invalid index! input again >>> ")
            continue
        if int(index_input) not in range(1, len(list_) + 1):
            index_input = input("invalid index! input again >>> ")
            continue
        else:
            break

    return int(index_input)


def get_task_info(task_info_list_, t):
    # print the schedule with indices
    print_task_info_list(task_info_list_)
    print()

    # get the index of the task whose info is to be modified
    task_index = input_index("input the index of the task from which the time is to be modified >>> ", task_info_list_)

    # get start time, end time, task names
    task = task_info_list_[task_index - 1]

    start_time = task[0]
    end_time = task[1]

    start_time_str = str(task[0]).zfill(4)
    end_time_str = str(task[1]).zfill(4)
    if task[1] == -1:
        end_time_str = '/'
    task_name_list = task[3]

    if t == 't':
        print("task_index: {}, start_time: {}, end_time: {}".format(task_index, start_time_str, end_time_str))
        return task_index, int(start_time), int(end_time)
    else:
        print("task_index: {}, task_name_list: {}".format(task_index, task_name_list))
        return task_index, task_name_list


def get_hour(time_):
    return int(time_ / 100)


def get_minute(time_):
    return time_ % 100


def add_time(original_time_, delta_min_):
    # example a): original_time_: 0820, delta_min_: +10
    # example b): original_time_: 0820, delta_min_: +50
    # example c): original_time_: 2320, delta_min_: +50

    # get hour
    # example a): 0820 / 100 -> 08
    # example b): 0820 / 100 -> 08
    # example c): 2320 / 100 -> 23
    hour_ = get_hour(original_time_)

    # get minute
    # example a): 0820 % 100 -> 20
    # example b): 0820 % 100 -> 20
    # example c): 2320 / 100 -> 20
    min_ = get_minute(original_time_)

    # add min without considering if it's valid. min_ + delta_min_
    # example a): 20 + 10 -> 30
    # example b): 20 + 50 -> 70
    # example C)> 20 + 50 -> 70
    min_added = min_ + delta_min_

    # judge whether min_added is invalid
    if min_added < 60:  # example a): min_added == 30 < 60 satisfies the condition
        # example a): 30
        modified_min_ = min_added

        # calculate modified hour
        # example a): 8 * 100 -> 800
        modified_hour_ = hour_ * 100
    else:  # example b): min_added == 70 > 60, c): min_added == 70 > 60 satisfy the condition
        # calculate delta hour
        # example b): 70 / 60 -> 1
        # example c): 70 / 60 -> 1
        delta_hour = int(min_added / 60)
        # calculate modified min
        # example b): 70 - 60 * 1 -> 10
        # example c): 70 - 60 * 1 -> 10
        modified_min_ = min_added - 60 * delta_hour

        # calculate hour having borrowed one digit
        # example b): 8 + 1 -> 9
        # example c): 23 + 1 -> 24
        hour_borrowed = hour_ + delta_hour

        # judge whether hour_borrowed >= 24
        if hour_borrowed < 24:  # example b): hour_borrowed == 9 < 24 satisfies the condition
            # calculate modified hour
            # example b): 9 * 100 -> 900
            modified_hour_ = hour_borrowed * 100
        else:  # example c): hour_borrowed == 24 >= 24 satisfies the condition
            # calculate overflow hours
            # example c): 24 - 24 -> 0
            hour_overflow = hour_borrowed - 24
            # calculate modified hour
            # example c): 0 * 100 -> 0
            modified_hour_ = hour_overflow * 100

    # example a): 800 + 30 -> 830
    # example b): 900 + 10 -> 910
    # example c): 0 + 10 -> 10
    time_added = modified_hour_ + modified_min_

    return time_added


def minus_time(original_time_, delta_min_):
    # example a): original_time_: 0820, delta_min_: 10
    # example b): original_time_: 0820, delta_min_: 30
    # example c): original_time_: 0020, delta_min_: 30

    # get hour
    # example a): 0820 / 100 -> 8
    # example b): 0820 / 100 -> 8
    # example c): 0020 / 100 -> 0
    hour_ = get_hour(original_time_)

    # get minute
    # example a): 0820 % 100 -> 20
    # example b): 0820 % 100 -> 20
    # example c): 0020 % 100 -> 20
    min_ = get_minute(original_time_)

    # minus time without considering if it's valid. min_ - delta_min_
    # example a): 20 - 10 -> 10
    # example b): 20 - 30 -> -10
    # example c): 20 - 30 -> -10
    min_minus = min_ - delta_min_

    # judge whether min_minus is invalid
    if min_minus >= 0:  # example a): min_minus == 10  >= 0satisfies the condition
        # example a): 10
        modified_min_ = min_minus

        # calculate modified hour
        # example a): 8 * 100 -> 800
        modified_hour_ = hour_ * 100
    else:  # example b): min_minus == -10 < 0, c): min_minus == -10 < 0 satisfy the condition
        # borrow some digits:
        # example b): (30 - 20) / 60 -> 1
        # example c): (30 - 20) / 60 -> 1
        digits_borrowed = math.ceil((delta_min_ - min_) / 60)

        # calculate hour having been borrowed some digits
        # example b): 8 - 1 -> 7
        # example c): 0 - 1 -> -1
        hour_borrowed_ = hour_ - digits_borrowed

        # judge if the hour having been borrowed < 0
        if hour_borrowed_ >= 0:  # example b): borrowed_hour_ == 7 > 0 satisfies the condition
            pass
        else:  # example c): borrowed_hour_ == -1 < 0 satisfies the condition
            # hour_ + 24 h
            # example c): 0 + 24 -> 24
            added_24h_hour_ = hour_ + 24
            # borrow a digit
            # example c): 24 - 1 -> 23
            hour_borrowed_ = added_24h_hour_ - 1

        # calculate min having borrowed some hours
        # example b): 20 + 60 * 1 -> 80
        # example c): 20 + 60 * 1 -> 80
        borrowed_min_ = min_ + 60 * digits_borrowed
        # calculate modified min
        # example b): 80 - 30 -> 50
        # example c): 80 - 30 -> 50
        modified_min_ = borrowed_min_ - delta_min_

        # calculate modified hour
        # example b): 7 * 100 -> 700
        # example c): 23 * 100 -> 2300
        modified_hour_ = hour_borrowed_ * 100

    # example a): 800 + 10 -> 810
    # example b): 700 + 50 -> 750
    # example c): 2300 + 50 -> 2350
    time_minus = modified_hour_ + modified_min_

    return time_minus


def get_delta_time(modified_time_, original_time_):
    # example a): modified_time_: 0820, original_time_: 0810
    # example b): modified_time_: 0820, original_time_: 0730
    # example c): modified_time_: 0020, original_time_: 0730

    cmp = compare_time(modified_time_, original_time_)
    if cmp == 0:
        modified_time_, original_time_ = original_time_, modified_time_

    # get hour
    # example a): 0820 / 100 -> 8, 0810 / 100 -> 8
    # example b): 0820 / 100 -> 8, 0730 / 100 -> 7
    # example c): 0020 / 100 -> 0, 0730 / 100 -> 7
    modified_hour_ = get_hour(modified_time_)
    original_hour_ = get_hour(original_time_)

    # get minute
    # example a): 0820 % 100 -> 20, 0810 % 100 -> 10
    # example b): 0820 % 100 -> 20, 0730 % 100 -> 30
    # example c): 0020 % 100 -> 20, 0730 % 100 -> 30
    modified_min_ = get_minute(modified_time_)
    original_min_ = get_minute(original_time_)

    # calculate delta min
    # example a): 20 - 10 -> 10
    # example b): 20 - 30 -> -10
    # example c): 20 - 30 -> -10
    delta_min = modified_min_ - original_min_

    # judge whether delta_min is invalid
    if delta_min >= 0:  # example a): delta_min == 10  >= 0 satisfies the condition
        # delta min represented in min
        # example a): 10
        delta_min_m = delta_min

        # calculate delta h represented in h
        # example a): 8 - 8 -> 0
        delta_hour_h = modified_hour_ - original_hour_
    else:  # example b): delta_min == -10 < 0, c): delta_min == -10 < 0 satisfy the condition
        # borrow a digit: modified_hour_ - 1
        # example b): 8 - 1 -> 7
        # example c): 0 - 1 -> -1
        modified_hour_borrowed = modified_hour_ - 1

        # judge if the hour having been borrowed < 0
        if modified_hour_borrowed >= 0:  # example b): modified_hour_borrowed == 7 > 0 satisfies the condition
            pass
        else:  # example c): modified_hour_borrowed == -1 < 0 satisfies the condition
            # hour_ + 24 h
            # example c): 0 + 24 -> 24
            added_24h_modified_hour_ = modified_hour_ + 24
            # borrow a digit
            # example c): 24 - 1 -> 23
            modified_hour_borrowed = added_24h_modified_hour_ - 1

        # modified_min_ + 60 min
        # example b): 20 + 60 -> 80
        # example c): 20 + 60 -> 80
        borrowed_modified_min_ = modified_min_ + 60
        # calculate delta min represented in min
        # example b): 80 - 30 -> 50
        # example c): 80 - 30 -> 50
        delta_min_m = borrowed_modified_min_ - original_min_

        # calculate delta h represented in h
        # example b): 7 - 7 -> 0
        # example c): 23 - 7 -> 16
        delta_hour_h = modified_hour_borrowed - original_hour_

    # calculate delta h represented in min
    # example a): 0 * 60 -> 0
    # example b): 0 * 60 -> 0
    # example c): 16 * 60 -> 960
    delta_hour_min = delta_hour_h * 60

    # calculate delta min: delta_min_m + delta_hour_min
    # example a): 10 + 0 -> 10
    # example b): 50 + 0 -> 50
    # example c): 50 + 960 -> 1010
    delta_min_ = delta_min_m + delta_hour_min

    if cmp == 0:
        delta_min_ *= -1

    return delta_min_


def compare_time(modified_time_, original_time_):
    # example a): modified_time_: 0820, original_time_: 0810
    # example b): modified_time_: 0820, original_time_: 0730
    # example c): modified_time_: 0020, original_time_: 0730

    # get hour
    # example a): 0820 / 100 -> 8, 0810 / 100 -> 8
    # example b): 0820 / 100 -> 8, 0730 / 100 -> 7
    # example c): 0020 / 100 -> 0, 0730 / 100 -> 7
    modified_hour_ = get_hour(modified_time_)
    original_hour_ = get_hour(original_time_)

    # if modified hour is 00, 01, 02
    if modified_hour_ in [0, 1, 2]:
        modified_hour_ += 24

    if modified_hour_ > original_hour_:
        return 1
    elif modified_hour_ < original_hour_:
        return 0
    else:
        # get minute
        # example a): 0820 % 100 -> 20, 0810 % 100 -> 10
        # example b): 0820 % 100 -> 20, 0730 % 100 -> 30
        # example c): 0020 % 100 -> 20, 0730 % 100 -> 30
        modified_min_ = get_minute(modified_time_)
        original_min_ = get_minute(original_time_)

        if modified_min_ >= original_min_:
            return 1
        else:
            return 0