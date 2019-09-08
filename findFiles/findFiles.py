#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os


def find_files():
    # # add a '\' before escape letters
    # pat = pat_raw
    #
    # escape_list = ['\$', '\(', '\)', '\*', '\+', '\.', '\[', '\]', '\?', r'\\', '\^', '\{', '\}', '\|']
    # for escape_letter in escape_list:
    #     # compile
    #     escape_pat = re.compile(r"{}".format(escape_letter))
    #     print(escape_letter)
    #     print(escape_pat, '\n')
    #
    #     # if there are some escape letters escape_letter in the input, add a '\' before the escape letter
    #     if escape_pat.search(pat_raw):
    #         pat = escape_pat.sub("\\{}".format(escape_letter), pat)
    #
    #         print(pat)
    #
    #     # input()

    # compile the pat
    pat = re.compile(r"{}".format(pat_raw))
    print(pat)

    # list file names in the dir
    file_names = os.listdir(dir_path)
    # print(file_names)

    # find files whose names match the pattern
    file_matched = [file_name for file_name in file_names if pat.search(file_name)]

    print(file_matched)


if __name__ == '__main__':
    # receive a dir path
    dir_path = input("input the dir path >>> ")

    # receive the pat to match file names
    pat_raw = input("receive the pattern >>> ")

    # file files
    find_files()
