
from global_const import app_config

import sys
sys.path.append(app_config.path.text_color)
from color_print import const




class SowerManager():
    def __init__(self):
        self.__eye = None

        self.__YELLOW = const.print_color.fore.yellow
    def start(self):
        self.hello_world()

    def main_loop(self):
        pass

    def hello_world(self):
        print(self.__YELLOW + 'Hello team!')

if __name__ == "__main__":
    runner = SowerManager()
    runner.hello_world()