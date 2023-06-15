from serial import Serial
import time
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# Path: static\py\Arduino_communication.py



class Arduino():

    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1, QUERY_ITERATIONS = 10, MAX_DATAFILES = 10, MIN_DATA_SIZE = 10) -> None:
        """Initialises the Arduino object.

        Args:
            port (str): port of the Arduino
            baudrate (int, optional): baudrate of the Arduino. Defaults to 9600.
            timeout (int, optional): timeout of the Arduino. Defaults to 1.
        """

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = Serial(self.port, self.baudrate, timeout=self.timeout)

        self.QUERY_ITERATIONS = QUERY_ITERATIONS
        self.MAX_DATAFILES = MAX_DATAFILES
        self.MIN_DATA_SIZE = MIN_DATA_SIZE

        self.last_rawline = b""
        self.log = []

        self.is_measuring = False
        self.user_commands = []

    def __repr__(self) -> str:
        return f"Arduino: {self.port}"
    
    def __str__(self) -> str:
        return self.port
    
    def send(self, msg: str) -> None:
        """Sends a message to the Arduino.

        Args:
            msg (str): message to send
        """

        time.sleep(2)

        self.serial.write(msg.encode())

        for i in range(self.QUERY_ITERATIONS):

            self.last_rawline = self.serial.readline()
            self.log.append(self.last_rawline)

            if self.last_rawline == msg.encode():
                break

    def get_log(self) -> str:
        """Returns the log of the Arduino.

        Returns:
            str: log of the Arduino
        """

        return "\n".join([line.decode() for line in self.log])

    def measurement(self, name: str = "") -> None:

        columns = [
            "Time",
            "Violet",   # 405 nm
            "Blue",     # 450 nm
            "Green",    # 510 nm
            "Yellow",   # 570 nm
            "Orange",   # 590 nm
            "Red",      # 630 nm
        ]

        sensor_data_dir = os.path.join(os.getcwd(), "Arduino", "Sensorreadings")
        dir_list = os.listdir(sensor_data_dir)

        if len(dir_list) > self.MAX_DATAFILES:
            os.remove(os.path.join(sensor_data_dir, dir_list[0]))

        if name == "":
            if f"Sensorreading_{len(dir_list)}.csv" not in dir_list:
                name = f"Sensorreading_{len(dir_list)}.csv"
            else:
                for i in range(len(dir_list)):
                    if f"Sensorreading_{i}.csv" not in dir_list:
                        name = f"Sensorreading_{i}.csv"
                        break

        with open(os.path.join(sensor_data_dir, name), "w") as f:

            writer = csv.writer(f)
            writer.writerow(columns)


        while True:

            self.is_measuring = True

            if self.serial.in_waiting > self.MIN_DATA_SIZE:

                self.last_rawline = self.serial.readline()
                self.log.append(self.last_rawline)

                data = self.last_rawline.decode().rstrip("\r\n")

                try:
                    values = np.array(data.split(",")).astype(np.uint32).reshape(1, 7)
                except:
                    e = sys.exc_info()[0]
                    print("Error while converting data to numpy array.")
                    print(e)

                    self.log.append("===========================================")                    
                    continue
                
                with open(os.path.join(sensor_data_dir, name), "a") as f:
                        
                        writer = csv.writer(f)
                        writer.writerows(values)

            if len(self.user_commands) > 0:
                for command in self.user_commands:
                    self.send(command)
                    self.user_commands.remove(command)

                    if command == "stop":
                        self.is_measuring = False
                        return