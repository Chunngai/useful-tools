#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os
import shutil


def get_inputs():
    # receive a dir path
    dir_path = input("input the dir path >>> ")

    # check if the dir path exists
    while not os.path.exists(dir_path):
        dir_path = input("the path does not exists! input again >>> ")

    # receive the pat to match file names
    pat_input = input("receive the pattern >>> ")

    return dir_path, pat_input


def copy_files(files_matched, dir_path):
    # create a dir
    dir_name = input("input the dir name >>> ")

    try:
        os.mkdir(dir_name)
    except:
        pass

    # move files matching the pat to the newly created dir
    for file in files_matched:
        # generate the path of the file to be copied
        file_path_from = os.path.join(dir_path, file)
        # generate the path where the file is to be stored
        file_path_to = os.path.join(dir_name, file)

        # copy the file to the dir
        if os.path.isfile(file_path_from):
            shutil.copy(file_path_from, file_path_to)
        else:
            shutil.copytree(file_path_from, file_path_to)


def find_files():
    # get the dir path and the pattern
    dir_path, pat_input = get_inputs()

    # put file names in the dir into a list
    file_names = os.listdir(dir_path)

    # compile the pat
    pat = re.compile(r"{}".format(pat_input))
    # find files whose names match the pattern
    files_matched = [file_name for file_name in file_names if pat.search(file_name)]

    # copy matched files to a newly created dir
    copy_files(files_matched, dir_path)


if __name__ == '__main__':
    # file files
    find_files()
