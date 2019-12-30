#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random


def input_number():
    number = input("input the number of members to be picked >>> ")
    while not number.isdigit():
        number = input("input a number! >>> ")

    return int(number)


def check():
    members_names_list = []
    members_not_pre_names_list = []

    # match members who have made a pre
    pat = re.compile(r".{2,3} \+")

    # load the membersName.txt file
    with open("membersNames.txt") as f:
        for line in f.readlines():
            # put names of members who have'nt made a pre into members_not_pre_names_list
            if not pat.search(line):
                members_not_pre_names_list.append(line)

            # put each member's name into members_names_list
            if line[2] == '\n':
                line = line[0:2] + ' ' + line[2:]

            members_names_list.append(line)

    print(members_names_list)

    print(members_not_pre_names_list)

    return members_names_list, members_not_pre_names_list


def pick(members_names_list, members_not_pre_names_list, number):
    # pick members to make a pre

    members_gonna_pre = []  # store the members who are gonna make a pre

    num_ = 0

    while True:
        # randomly pick a member
        member_gonna_pre_index = random.randint(1, 21)
        member_gonna_pre = members_names_list[member_gonna_pre_index - 1]

        # if the member picked has not made a pre and is not in the members_gonna_pre list
        if member_gonna_pre in members_not_pre_names_list and \
                member_gonna_pre not in members_gonna_pre:
            members_gonna_pre.append(member_gonna_pre)  # pick the member

            num_ += 1

        if num_ == number:
            break

    return members_gonna_pre


def update(members_gonna_pre, members_names_list):
    # print members picked
    print()

    for member in members_gonna_pre:
        print(member, end='')

    # update the txt file
    for member_index in range(len(members_names_list)):
        for member_not_pre in members_gonna_pre:
            if member_not_pre in members_names_list[member_index]:  # for the member picked
                # add a '+' after the picked member's name
                members_names_list[member_index] = members_names_list[member_index][:3] + " +\n"

    with open("membersNames.txt", 'w') as f:
        for member in members_names_list:
            f.write(member)


def random_pick():
    # input the number of members to be picked
    number = input_number()

    # get a list of members who have not made a pre
    members_names_list, members_not_pre_names_list = check()

    # pick two lucky members
    members_gonna_pre = pick(members_names_list, members_not_pre_names_list, number)

    # the current state of the two members: not yet -> already
    update(members_gonna_pre, members_names_list)


if __name__ == '__main__':
    random_pick()
