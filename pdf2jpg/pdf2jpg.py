#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pdf2image import convert_from_path


def pdf_exists(dir_path):
    for file in os.listdir(dir_path):
        if os.path.splitext(file)[1] == ".pdf":
            return True

    return False


def pdf_2_image():
    # get the path of the dir containing the pdf file
    dir_path = input("input the path of the dir containing the pdf file >>> ")
    while True:
        if not os.path.exists(dir_path):
            dir_path = input("the path does not exist! input again >>> ")
        elif not pdf_exists(dir_path):
            dir_path = input("there is no pdf file in the dir! input again >>> ")
        else:
            break

    # get the path of the pdf file
    pdf_file_name = dir_path.split('\\')[-1]
    pdf_path = os.path.join(dir_path, pdf_file_name + ".pdf")

    # generate a dir for storing the images
    image_dir = os.path.join(dir_path, pdf_file_name + "PdfImages")
    try:
        os.mkdir(image_dir)
    except FileExistsError:
        pass

    # pdf2image
    convert_from_path(pdf_path, output_folder=image_dir, fmt="jpg")


if __name__ == '__main__':
    pdf_2_image()
