
from global_const import app_config

import sys
sys.path.append(app_config.path.text_color)
from color_print import const

from robot_eye import RobotEye
from robot_arms import RobotArms
from servo_array_driver import ServoArrayDriver
import paho.mqtt.client as mqtt
from mqtt_agent import MqttAgent


class SowerManager():

    def __init__(self):
        self.__eye = RobotEye()
        self.__arm = RobotArms()
        self.__servos = ServoArrayDriver()

        self.__goto = self.__on_state_begin
        self.__matt = mqtt
        self.__mqtt_agent = MqttAgent()
        self.__system_turn_on = False

        self.__YELLOW = const.print_color.fore.yellow
        self.__GREEN = const.print_color.fore.green
        self.__RESET = const.print_color.control.reset

    def __on_state_begin(self):
        if self.__system_turn_on:
            # Turn on light
            # Trun on main motor
            # Trun on vaccum motor
            self.__mqtt.publish('sower/switch/light/command', 'ON')
            self.__mqtt.publish('sower/switch/motor/command', 'ON')
            self.__mqtt.publish('sower/switch/vaccum/command', 'ON')
            self.__goto = self.__on_state_working

    def __on_state_idle(self):
        if False:
            self.__goto = self.__on_state_working

    def __on_state_working(self):
        if self.__system_turn_on:
            # Turn off light
            # Trun off main motor
            self.__mqtt.publish('sower/light/command', 'OFF')
            self.__mqtt.publish('sower/motor/command', 'OFF')
            self.__goto = self.__on_state_begin

        if False:
            self.__goto = self.__on_state_emergency_stop

    def __on_state_emergency_stop(self):
        if self.__mqtt_system_on:
            self.__goto = self.__on_state_begin

    def __on_eye_got_new_plate(self, plate_array, image):
        self.__arm.set_new_plate(plate_array)

        # flask return image to web ui

            
    def setup(self):
        self.__mqtt = self.__mqtt_agent.connect()
        self.__eye.setup(self.__mqtt, self.__on_eye_got_new_plate)
        print(const.print_color.background.blue + self.__YELLOW)
        print('System is initialized. Now is working')
        print(self.__RESET)

    def main_loop(self):
        last_function = self.__goto
        self.__goto()
        if last_function != self.__goto:
            print(const.print_color.background.blue + self.__YELLOW)
            print(self.__goto.__name__)
            print(self.__RESET)


if __name__ == "__main__":
    runner = SowerManager()
    runner.setup()
    while True:
        runner.main_loop()


#
#         |-----------> ??? ----------->|
#         ^                             |
#         |-----------> ??? ----------->|
#         ^                             |
#         |-----------> ??? ----------->|
#         ^                             |
#         |-----------> ??? ----------->|
#         ^
#         |           |--->--->--->--->--->--->---|
#         ^           |                           |
#        begin ---> idle ---> working ------> EmergencyStop
#         ^           ^          |                 |
#         |           |--<---<---|                 |
#         ^                      |                 |
#         |<---<---<---<---<---<--                 |
#         ^                                        |
#         |<---<---<---<---<---<---<---<---<---<----
#   
#
#        idle, EmergencyStop: are not avaliable before version 1.0