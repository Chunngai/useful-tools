#!/usr/bin/env python
# -*- coding_ utf-8 -*-

import pandas as pd


def reorganize(file_name):
    # load the question base
    data = pd.read_csv(file_name + ".csv")
    # print(len(data))

    # float -> str for the uncertain attr
    data["uncertain"] = data["uncertain"].astype(str)
    data.loc[data.uncertain == "nan", "uncertain"] = ""

    # incorrect
    incorrect_rows = data[~data["incorrect"].isin([0])]
    # print(len(incorrect_rows))

    # uncertain
    correct_rows = data[data["incorrect"].isin([0])]
    # print(len(correct_rows))
    correct_n_uncertain_rows = correct_rows[~correct_rows["uncertain"].isin([""])]
    # print(len(correct_n_uncertain_rows))

    # correct_and_certain
    correct_n_certain_rows = correct_rows[correct_rows["uncertain"].isin([""])]
    # print(len(correct_n_certain_rows))

    reorganized_data = pd.concat([incorrect_rows, correct_n_uncertain_rows, correct_n_certain_rows])

    # print(len(reorganized_data))

    reorganized_data.to_csv(file_name + " (reorganized).csv", index=False)


if __name__ == '__main__':
    reorganize(input("input file name >>> "))
