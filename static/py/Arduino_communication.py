from serial import Serial
from serial.tools.list_ports import comports


import time
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import threading
from flask import url_for

# Path: static\py\Arduino_communication.py


class Arduino():
    """Class for communicating with the Arduino."""

    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1, QUERY_ITERATIONS = 10, MIN_DATA_SIZE = 10, csv_name: str = "readings_0.csv") -> None:
        """Initialises the Arduino object.

        Args:
            port (str): port of the Arduino
            baudrate (int, optional): baudrate of the Arduino. Defaults to 9600.
            timeout (int, optional): timeout of the Arduino. Defaults to 1.

        """

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        print("Try connection...")
        self.serial = Serial(self.port, self.baudrate, timeout=self.timeout)
        print("No Error")

        self.lock = threading.Lock()
        self.should_stop = False

        self.QUERY_ITERATIONS = QUERY_ITERATIONS
        self.MIN_DATA_SIZE = MIN_DATA_SIZE

        self.last_rawline = b""
        self.log_adress = os.path.join("csv_folder", "log.csv")
        self.create_log()
        self.sensor_adress = os.path.join("csv_folder", csv_name)
        self.create_sensor_data()

        self.is_measuring = False
        self.user_commands = []



    def __repr__(self) -> str:
        return f"Arduino: {self.port}"
    
    def __str__(self) -> str:
        return self.port
    
    def stop(self) -> None:
        """Stops the Arduino."""

        with self.lock:

            self.should_stop = True

    def read(self) -> bytes:
        """Reads a line from the Arduino.

        Returns:
            bytes: line from the Arduino
        """
        print("before reading")

        print(f"is currently locked: {self.lock.locked()}")
        with self.lock:

            print("in reading")

            rawline = self.serial.readline()

            print("after reading")

            return rawline
    
    
    def send(self, msg: str) -> None:
        """Sends a message to the Arduino.

        Args:
            msg (str): message to send
        """

        time.sleep(2)

        with self.lock:

            print("before sending")

            self.serial.write(f"{msg}\n".encode())

            print("after sending")

        for i in range(self.QUERY_ITERATIONS):
            rawline = self.read()
            print(f"rawline after sending: , {rawline}")
            if rawline != b"":
                self.last_rawline = rawline
            if rawline == f"{msg}\n".encode():
                break

        self.update_log()

    
    def create_log(self) -> None:
        """Creates a log file for the Arduino."""

        if os.path.exists(self.log_adress): return

        with self.lock:
            with open(self.log_adress, "w") as f:
                f.write("")

    def get_log(self) -> list[str]:
        """Returns the log of the Arduino.

        Returns:
            list[str]: log of the Arduino
        """

        with self.lock:
            with open(self.log_adress, "r") as f:
                log = f.readlines()

        return log
    
    def update_log(self, line: bytes = b"") -> None:
        """Updates the log of the Arduino."""

        with self.lock:

            with open(self.log_adress, "r") as f:
                log = f.readlines()

            if line != b"":
                log.append(line.decode())

            else:
                if self.last_rawline == b"":
                    return
                
                else:
                    log.append(self.last_rawline.decode())
                    self.last_rawline = b""

            with open(self.log_adress, "w") as f:
                f.writelines(log)

    def create_sensor_data(self) -> None:
        """Creates a file for the sensor data."""

        if os.path.exists(self.sensor_adress): return

        with self.lock:
            with open(self.sensor_adress, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Violet", "Blue", "Green", "Yellow", "Orange", "Red"])

    def measurement(self, recurrsion_depth=0) -> None:

        columns = [
            "Time",
            "Violet",   # 405 nm
            "Blue",     # 450 nm
            "Green",    # 510 nm
            "Yellow",   # 570 nm
            "Orange",   # 590 nm
            "Red",      # 630 nm
        ]

        if not self.serial.in_waiting > self.MIN_DATA_SIZE:
            if recurrsion_depth < 10:
                time.sleep(1)
                self.measurement(recurrsion_depth + 1)
            else:
                self.update_log(f"Measurement failed")
                return
            
        try:
            rawline = self.read()
        
            data = rawline.decode().rstrip(",\r\n") # bringt die Daten in die Form "time,violet,blue,green,yellow,orange,red"
            values = np.array(object=data.split(","), dtype=np.uint32).reshape((1,7))
            with open(self.sensor_adress, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(values)
        except:
            self.update_log(rawline)
            self.update_log(b"===================== Measurement failed =======================")
            print("Measurement failed")



def attempt_connection(port: str, baudrate: int = 9600, timeout: int = 1) -> tuple[bool, Arduino | None]:
    """Attempts to connect to the Arduino.

    Args:
        port (str): port of the Arduino
        baudrate (int, optional): baudrate of the Arduino. Defaults to 9600.
        timeout (int, optional): timeout of the Arduino. Defaults to 1.

    Returns:
        bool: True if connection was successful, False otherwise
    """

    try:
        arduino = Arduino(port, baudrate, timeout)
        print(f"Connected to Arduino on port {port}")
        return True, arduino
    except:
        return False, None

def get_arduino_ports() -> list[str]:
    """Returns a list of all available ports.

    Returns:
        list[str]: list of all available ports
    """

    arduino_ports = [port for port, desc, hwid in sorted(comports()) if "Arduino" in desc]

    print("Available ports:")
    for port in arduino_ports:
        print(port)

    return arduino_ports

def connection_state(connected: bool, arduino: Arduino) -> str:
    """Returns the connection state of the Arduino."""
    
    if not connected:
        response = "> Arduino is not connected"

    elif connected and not isinstance(arduino, Arduino):
        response = "> Something went wrong"
    
    elif connected and isinstance(arduino, Arduino):
        response = "> Arduino is connected"

    return response
