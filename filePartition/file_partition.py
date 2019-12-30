#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math

def file_partition(file_path, max_size):
    with open(file_path, "rb") as f:
        data = f.read()

    for i in range(math.ceil(len(data) / max_size)):
        with open(file_path.split('.')[0] + "_{}".format(i), "wb") as f:
            f.write(data[:max_size])
        data = data[max_size:]

if __name__ == "__main__":
    file_partition("/home/neko/Desktop/cn_windows_10_consumer_edition_version_1803_updated_sep_2018_x64_dvd_a3fcbed0(1).iso", 2 ** 31)
