#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pdf2image import convert_from_path


def pdf_2_image():
    # get the path of the pdf file
    pdf_path = input("input the path of the pdf file >>> ")
    while not os.path.exists(pdf_path):
        pdf_path = input("invalid path! input again >>> ")

    # pdf2image
    convert_from_path(pdf_path, output_folder=os.getcwd(), fmt="jpg")


if __name__ == '__main__':
    pdf_2_image()
