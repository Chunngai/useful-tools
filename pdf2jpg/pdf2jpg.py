#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pdf2image import convert_from_path


def pdf_2_image():
    # get the path of the pdf file to be processed
    path = input("input the path of the pdf file >>> ")
    while not os.path.exists(path):
        path = input("the file path does not exist! input the path again >>> ")

    # get the output folder
    output_folder = input("input the output folder >>> ")
    while not os.path.exists(output_folder):
        output_folder = input("the output folder does not exists! input again >>> ")

    # pdf2image
    convert_from_path(path, output_folder=output_folder, fmt="jpg")


if __name__ == '__main__':
    pdf_2_image()
