import os
import signal
import time


def check_time():
    if 1 <= time.localtime()[3] <= 6:
        return True


def go_to_bed_early(software_list_):
    for software in software_list_:
        # finds out all processes of a program
        process_list = os.popen("ps aux | grep {}".format(software)).read().splitlines()

        # kill the processes
        for process in process_list:
            try:
                os.kill(int(process.split()[1]), signal.SIGKILL)
            except ProcessLookupError:
                pass


if __name__ == '__main__':
    software_list = ["chrome", "notepad-plus-plus", "intellij-idea-community", "clion", "pycharm-community",
                     "libreoffice", "atom"]

    while True:
        if check_time():
            go_to_bed_early(software_list)
        time.sleep(60)
