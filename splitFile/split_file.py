#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math


def split_file(file_path, size):
    print("splitting {}".format(file_path))

    with open(file_path, "rb") as f:
        data = f.read()

    for i in range(math.ceil(len(data) / size)):
        path = file_path.split('.')[0] + "_{}".format(i)
        with open(path, "wb") as f:
            f.write(data[:size])
            print("{} saved".format(path))
        data = data[size:]

    print("done")


def connect_files(file_path):
    print("connecting files split from {}".format(file_path))

    for dir_path, dir_names, file_names in os.walk(os.path.dirname(file_path)):
        file_names.remove(os.path.basename(file_path))

        file_paths = [os.path.join(dir_path, file_name) for file_name in file_names
                      if os.path.basename(file_path.split('.')[0]) in os.path.basename(file_name).split('.')[0]]
        file_paths.sort(key=lambda x: int(x.split('_')[-1]))

        new_file_data = b''
        for i in range(len(file_paths)):
            with open(file_paths[i], "rb") as f:
                new_file_data += f.read()

        new_file_path = file_path.split('.')[0] + '_.' + file_path.split('.')[1]
        with open(new_file_path, "wb") as f:
            f.write(new_file_data)

        break

    print("done")


if __name__ == "__main__":
    file_path = "/home/neko/Desktop/cn_windows_10_consumer_edition_version_1803_updated_sep_2018_x64_dvd_a3fcbed0(1).iso"
    size = 2 ** 30

    split_file(file_path, size)
    # connect_files(file_path)
