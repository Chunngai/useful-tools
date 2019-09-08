#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os


def get_inputs():
    # receive a dir path
    dir_path = input("input the dir path >>> ")

    # check if the dir path exists
    while not os.path.exists(dir_path):
        dir_path = input("the path does not exists! input again >>> ")

    # receive the pat to match file names
    pat_input = input("receive the pattern >>> ")

    return dir_path, pat_input


def find_files():
    # get the dir path and the pattern
    dir_path, pat_input = get_inputs()

    # compile the pat
    pat = re.compile(r"{}".format(pat_input))

    # put file names in the dir into a list
    file_names = os.listdir(dir_path)

    # find files whose names match the pattern
    file_matched = [file_name for file_name in file_names if pat.search(file_name)]

    # print(file_matched)
    # move matched files to a newly created dir


if __name__ == '__main__':
    # file files
    find_files()
