#!/usr/bin/env python
# -*- coding_ utf-8 -*-

import pandas as pd


def reorganize(file_name):
    # load the question base
    data = pd.read_csv(file_name + ".csv")

    # float -> str for the uncertain attr
    data["uncertain"] = data["uncertain"].astype(str)
    data.loc[data.uncertain == "nan", "uncertain"] = ""

    data.loc[data.question_index != 0, "question_index"] = 0

    # incorrect
    incorrect_rows = data[~data["incorrect"].isin([0])]

    # uncertain
    correct_rows = data[data["incorrect"].isin([0])]
    correct_n_uncertain_rows = correct_rows[~correct_rows["uncertain"].isin([""])]

    # correct_and_certain
    correct_n_certain_rows = correct_rows[correct_rows["uncertain"].isin([""])]

    # concatenation
    reorganized_data = pd.concat([incorrect_rows, correct_n_uncertain_rows, correct_n_certain_rows])

    # save the file
    reorganized_data.to_csv(file_name + " (reorganized).csv", index=False)


if __name__ == '__main__':
    reorganize(input("input file name >>> "))
