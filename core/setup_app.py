import os


def init_folder():
    folders = ["uploads", "logs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)


def setup_onstart():
    init_folder()
