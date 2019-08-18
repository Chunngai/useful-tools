#!usr/bin/python
# -*- coding: utf-8 -*-env

import re

from scheduleCommonFunc import print_task_info_list
from scheduleCommonFunc import copy_to_clipboard
from scheduleCommonFunc import input_
from scheduleCommonFunc import generate_task_list
from scheduleCommonFunc import get_task_info
from scheduleCommonFunc import add_time
from scheduleCommonFunc import minus_time
from scheduleCommonFunc import get_delta_time
from scheduleCommonFunc import compare_time


"""
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
    pat = re.compile(r"(- \[ ] )?((\d+)-(\d*))?\s*(.*)")
    for i in range(len(input_list)):
        rst = pat.search(input_list[i])

        # get start time, end time, duration, task name
        if rst.group(2):
            start_time = ''
            end_time = ''
            if rst.group(3):
                start_time = int(rst.group(3))
            if rst.group(4):
                end_time = int(rst.group(4))
            if rst.group(3) and not rst.group(4):  # like 2110-
                end_time = -1
            duration = get_delta_time(end_time, start_time)
            task_name_list = [rst.group(5)]
            task_info_list.append([start_time, end_time, duration, task_name_list])
        else:
            task_info_list[len(task_info_list) - 1][3].append(rst.group(5))

    return task_info_list"""

"""
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
"""
"""
def print_task_info_list(task_info_list_):
    for i in range(len(task_info_list_)):
        task = task_info_list_[i]  # for every task

        # get start time, end time, task name
        start_time = str(task[0]).zfill(4)
        end_time = str(task[1]).zfill(4)
        if task[1] == -1:
            end_time = ''
        task_name_list = task[3]

        # print (i) hhmm-(hhmm) task_name(the first one)
        print("({}) {}-{} {}".format(i + 1, start_time, end_time, task_name_list[0]))

        # print other tasks(if there are)
        for j in range(1, len(task_name_list)):
            print(' ' * (12 + len(str(i))), task_name_list[j])"""

"""
def get_task_info(task_info_list_):
    # print the schedule with indices
    print_task_info_list(task_info_list_)
    print()

    # get the index of the task whose time is to be modified
    task_index_input = input("input the index of the task from which the time is to be modified >>> ")
    # check if the input is digits
    while not str(task_index_input).isdigit():
        task_index_input = input("invalid index! input again >>> ")
    # check if the input is in a valid range
    while int(task_index_input) not in range(1, len(task_info_list_) + 1):
        task_index_input = int(input("invalid index! input again >>> "))
    task_index = int(task_index_input)

    # get start time, end time
    start_time = task_info_list_[task_index - 1][0]
    end_time = task_info_list_[task_index - 1][1]

    print("task_index: {}, start_time: {}, end_time: {}".format(task_index, start_time, end_time))
    return task_index, start_time, end_time
"""


def get_modified_time(start_time_, end_time_):
    # match input and return the result
    def get_rst(prompt, t_):
        pat_1 = re.compile(r"^\d{4}$")  # forms like 0800
        pat_2 = re.compile(r"^([+\-]?)(\d+)\s?(min?|h?)$")  # forms like +30 min, -2h  # !!!!!!!!!!!!!!!!?????????
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
        if rst.group(3) == 'h':
            delta_time_ *= 60

        # add/minus
        if rst.group(1) in ['+', '']:
            modified_time_ = add_time(original_time_, delta_time_)
        else:
            modified_time_ = minus_time(original_time_, delta_time_)

        return modified_time_

    if end_time_ == -1:
        # if a new duration or an end time with the hhmm form is given, flag = 1 and the task will get an end time
        global flag
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

                try:
                    # a duration is given to a task which originally has not an end time
                    flag = 1
                except:
                    pass
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

            try:
                # an end time is given to a task which originally has not one
                flag = 1
            except:
                pass
        else:  # the input is something like +30 min
            modified_end_time = get_modified_time_inner(rst, end_time_)

    try:
        if flag == 0:
            # the task originally has not an end time and a duration or an end time is not given
            modified_end_time = -1
    except:
        pass

    print("modified_start_time: {}, modified_end_time: {}\n".format(modified_start_time, modified_end_time))
    return modified_start_time, modified_end_time

"""
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
"""

"""
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
"""


def modify_remaining(task_index_, task_info_list_, delta_time_, modified_start_time_, modified_end_time_):
    new_task_info_list = task_info_list_

    # add modified start time and end time to the list
    new_task_info_list[task_index_ - 1][0] = modified_start_time_
    new_task_info_list[task_index_ - 1][1] = modified_end_time_

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

                task_ = task_info_list_[j]
                task_[0] = start_time_modified
                task_[1] = end_time_modified

    print_task_info_list(new_task_info_list)

    return new_task_info_list

"""
def copy_to_clipboard(new_task_info_list_):
    new_task_str = ''
    for i in range(len(new_task_info_list_)):
        task = new_task_info_list_[i]

        # get start time, end time, task names
        start_time = str(task[0]).zfill(4)
        end_time = str(task[1]).zfill(4)
        if task[1] == -1:
            end_time = ''
        task_name_list = task[3]

        # concatenation
        new_task_str += ("{}-{} {}\n".format(start_time, end_time, task_name_list[0]))

        for j in range(1, len(task_name_list)):
            new_task_str += (' ' * (8 + len(str(i))) + task_name_list[j] + '\n')

    # copy the created schedule to the clipboard
    pyperclip.copy(new_task_str)
    print(new_task_str)
"""


def modify_time():
    # receive data
    data = input_()

    # make data into a nested list
    task_info_list = generate_task_list(data)

    # ask how to modify
    task_index, start_time, end_time = get_task_info(task_info_list, 't')
    modified_start_time, modified_end_time = get_modified_time(start_time, end_time)

    while end_time != -1 and compare_time(modified_end_time, modified_start_time) == 0:
        print("modified end time is earlier than modified start time! input data again!")
        modified_start_time, modified_end_time = get_modified_time(start_time, end_time)

    # calculate modified_time - end_time
    delta_time = get_delta_time(modified_end_time, end_time)
    if end_time == -1:
        delta_time = 0

    # modify schedule
    new_task_info_list = modify_remaining(task_index, task_info_list, delta_time, modified_start_time, modified_end_time)
    print()

    # copy the new list to the clipboard
    print("modified schedule:")
    print('-' * 30)
    copy_to_clipboard(new_task_info_list)


if __name__ == '__main__':
    modify_time()
