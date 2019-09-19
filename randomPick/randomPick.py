#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random


def check():
    members_names_list = []

    # load the membersName.txt file
    with open("membersNames.txt") as f:
        for line in f.readlines():
            members_names_list.append(line)

    print(members_names_list)

    # put names of members who have'nt made a pre into a list
    pat = re.compile(r".{2,3} \+")
    members_not_pre_names_list = [name for name in members_names_list if not pat.search(name)]
    print(members_not_pre_names_list)
    return members_names_list, members_not_pre_names_list


def pick(members_names_list, members_not_pre_names_list):
    # pick two members that have not made a pre
    while True:
        member_1_index = random.randint(1, len(members_not_pre_names_list))
        member_2_index = random.randint(1, len(members_not_pre_names_list))

        if members_names_list[member_1_index - 1] in members_not_pre_names_list and \
                members_names_list[member_2_index - 1] in members_not_pre_names_list and \
                member_1_index != member_2_index:
            break

    return members_names_list[member_1_index - 1], members_names_list[member_2_index - 1]


def update(member_1, member_2, members_names_list):
    print(member_1, member_2, sep='')

    # update the txt file
    for member_index in range(len(members_names_list)):
        if member_1 in members_names_list[member_index]:
            members_names_list[member_index] = members_names_list[member_index][:3] + " +\n"
        if member_2 in members_names_list[member_index]:
            members_names_list[member_index] = members_names_list[member_index][:3] + " +\n"

    with open("membersNames.txt", 'w') as f:
        for member in members_names_list:
            f.write(member)


def random_pick():
    # get a list of members who have not made a pre
    members_names_list, members_not_pre_names_list = check()

    # pick two lucky members
    member_1, member_2 = pick(members_names_list, members_not_pre_names_list)

    # the current state of the two members: not yet -> already
    update(member_1, member_2, members_names_list)


if __name__ == '__main__':
    random_pick()
