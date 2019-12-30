#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup


def get_word_list(file_path_):
    # load words from the file
    with open(file_path_, encoding="utf-8") as f:
        raw_word_data = f.read()

    # split the words
    word_list = raw_word_data.split('\n')

    return word_list


def generate_headers():
    headers = {
        'cookie': 'HJ_UID=0af72702-0a73-8b72-8d39-aa97cabeda7e; _REG=www.baidu.com|; _REF=https://www.baidu.com/link?ur\
l%3D9AoCiI88Q31AHRiwUkPropSrEjnrnbBe6Z3Q4jdNhHnQQ0Pw8uHBGy5_kLqIvggiFWlmU4MbkdfslKxMzUgPvWXeFhI-50fmdQtREVTsAgG&wd%3D&e\
qid%3Ddcf5801000050c70000000065bc2ee0e; _SREG_20=www.baidu.com|; TRACKSITEMAP=3%2C6%2C11%2C19%2C20%2C22%2C23%2C75%2C242\
3%2C2437%2C; _SREF_20=https://www.baidu.com/link?url%3D45luy6TU1rJiMBvHW9Hz3wpuFywb0QdhkfZ7WGqQy4viOTHH91WnN7ca2l5Y36Hq\
&wd%3D&eqid%3Dec1f89ad000d0c0d000000065d33229a; Hm_lvt_d4f3d19993ee3fa579a64f42d860c2a7=1565449039,1565449412; _SREG_3=\
www.baidu.com|; HJ_SID=22465fb1-9abb-af3e-55fa-1ca37c6b47f3; HJ_SSID_3=48c7c028-4b88-a0b0-a3ea-48b7d75ec3ae; HJ_CST=0; \
HJ_CSST_3=0; _SREF_3=https://www.baidu.com/link?url%3D9cpSSix5enS5LJ3QOeDwMB_lMsEqnDoF7imiK07a6EBS9jliyjPw0X98xROWaVTI&\
wd%3D&eqid%3Df42913f70002336e000000065ce510ca; _UZT_USER_SET_106_0_DEFAULT=2|ea3cbaa2f0bb85661c19a0048c3a6f35',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.380\
9.100 Safari/537.36'}

    return headers


def make_request(url):
    headers = generate_headers()

    count = 0
    while count < 3:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            pass
        count += 1

    return ""


def get_info(html_text):
    # store pronunciation, simple meanings
    info_dict = {}

    # get soup
    soup = BeautifulSoup(html_text, "html.parser")

    # get pronunciation
    pronunciation = []
    try:
        pronunciation = soup("span", "pronounce-value-en")[0].string
        info_dict["pronunciation"] = pronunciation
    except:
        info_dict["pronunciation"] = "[]"

    print(pronunciation)

    """# get simple meanings
    simple_meanings = {}
    try:
        div_simple = soup("div", "simple")[0]

        for p in div_simple.children:
            try:
                # get part of speech
                part_of_speech = p.span.string.strip()

                # get simple meanings
                simple_meanings_ = p.span.next_sibling.next_sibling.string.strip()
            except:
                pass
            else:
                simple_meanings[part_of_speech] = simple_meanings_

            # put into info_dict
            info_dict["simple_meanings"] = simple_meanings
    except:
        info_dict["simple_meanings"] = {}"""

    print(info_dict)
    return info_dict


def get_word_info_dict(word_list):
    url_root = "https://dict.hjenglish.com/w/"

    # generate a word_info dict
    word_info = {key: [] for key in word_list}

    # find info of each word
    for word in word_list:
        print("getting info of \"{}\"".format(word))

        # generate the url
        url = url_root + word

        # make a request
        html_text = make_request(url)
        if not html_text:  # '' returned
            continue

        # get info
        info = get_info(html_text)

        # word: [] -> word: info
        word_info[word] = info

    return word_info


def save_info(word_info):
    with open("eng_words_.txt", 'w', encoding="utf-8") as f:
        pass


def get_new_words_from_hujiang(file_path_):
    # put words in a list
    word_list = get_word_list(file_path_)

    # look for meanings
    word_info = get_word_info_dict(word_list)

    # save meanings
    save_info(word_info)


if __name__ == '__main__':
    file_path = "eng_words.txt"
    get_new_words_from_hujiang(file_path)
