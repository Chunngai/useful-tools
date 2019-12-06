#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import string
import os
import traceback

# read the question base
file_path = input("input file path >>> ")
data = pd.read_csv(file_path)

try:
    os.system("clear")
except:
    os.system("cls")

# count choices
choice_num = 0
for i in list(data.columns):
    if len(i) == 1 and i.isalpha():
        choice_num += 1

# separate
questions = data[data.columns[0:1]]
choices = data[data.columns[1:choice_num + 1]]
answers = data[data.columns[choice_num + 1:choice_num + 2]]

# add two columns
if "uncertain" not in list(data.columns):
    data["uncertain"] = ""

# float -> str for the uncertain attr
data["uncertain"] = data["uncertain"].astype(str)
data.loc[data.uncertain == "nan", "uncertain"] = ""

if "incorrect" not in list(data.columns):
    data["incorrect"] = 0

question_index = 0
if "question_index" not in list(data.columns):
    data["question_index"] = 0
else:
    question_index = data["question_index"][0]

if question_index == len(data):
    question_index = 0

# display questions repeatedly
for i in range(question_index, len(data)):
    try:
        # shuffle the columns
        sampler = np.random.permutation(choice_num)
        current_choice = choices.iloc[i].take(sampler, axis=1)

        # mapping
        choices_mapping = {}
        for j in range(choice_num):
            choices_mapping[string.ascii_uppercase[j]] = current_choice.index[j]

        # display the question
        print(str(i + 1) + '.', questions.iloc[i][0])

        # display choices
        for j in range(choice_num):
            # print(current_choice.index[j], current_choice.iloc[j])
            print(string.ascii_uppercase[j], current_choice.iloc[j])

        print()
        # ignore spaces
        input_answer = input().strip()
        while input_answer not in string.ascii_lowercase[:choice_num] + string.ascii_uppercase[
                                                                        :choice_num] + "#" or not len(input_answer):
            if not input_answer.strip():
                pass
            else:
                print("invalid input!")

            input_answer = input().strip()

        # check if the answer is correct
        if input_answer == "#":
            break

        if input_answer in string.ascii_lowercase[:choice_num]:
            data.loc[i, "uncertain"] += choices_mapping[input_answer.upper()]

        input_answer = input_answer.upper()
        input_answer = choices_mapping[input_answer]
        if input_answer == answers.iloc[i][answers.columns[0]]:
            print("correct!")
        else:
            print("wrong!")
            print("the correct answer is:\n",
                  list(filter(lambda x: answers.iloc[i][0] == x[1], choices_mapping.items()))[0][0] + ".",
                  choices.iloc[i][answers.iloc[i]][0])
            data.loc[i, "incorrect"] += 1

        data.loc[0, "question_index"] = i + 1

        # save the csv file
        data.to_csv(file_path, index=False)
    except:
        print("\n\nsome exceptions are raised in this question:\n")
        print(traceback.print_exc())
        if not os.path.exists("question_base_log.txt"):
            with open("question_base_log.txt", "w") as f:
                f.write("question" + str(i + 1) + ":\n")
                f.write(traceback.format_exc() + "\n\n")
        else:
            with open("question_base_log.txt", "a") as f:
                f.write("question" + str(i + 1) + ":\n")
                f.write(traceback.format_exc() + "\n\n")

    input()

    try:
        os.system("clear")
    except:
        os.system("cls")
