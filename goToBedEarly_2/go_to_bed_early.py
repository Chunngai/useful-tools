import os
import signal
import datetime
import time


def wait():
    # get the current time
    current_time = datetime.datetime.now()
    # get the time when specified software should be closed
    exe_time = (current_time + datetime.timedelta(days=1)).replace(hour=1, minute=0, second=0)

    # wait for the execute time
    sleep_time = (exe_time - current_time).seconds

    with open("/home/neko/Desktop/log.txt", "a") as f:
        f.write(str(current_time) + "\n")
        f.write(str(exe_time) + "\n")
        f.write(sleep_time)

    time.sleep(sleep_time)


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

    wait()

    while True:
        if check_time():
            go_to_bed_early(software_list)
        time.sleep(60)
