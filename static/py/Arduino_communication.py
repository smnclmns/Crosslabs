from serial import Serial
from serial.tools.list_ports import comports

import time
import os
import csv
import numpy as np
import threading

# Path: static\py\Arduino_communication.py


class Arduino():
    """Class for communicating with the Arduino."""

    def __init__(self, port: str, baudrate: int = 9600, timeout: int = 1, QUERY_ITERATIONS = 10, MIN_DATA_SIZE = 10, csv_name: str = "readings_0.csv") -> None:
        """Initialises the Arduino object.

        Args:
            port (str): port of the Arduino
            baudrate (int, optional): baudrate of the Arduino. Defaults to 9600.
            timeout (int, optional): timeout of the Arduino. Defaults to 1.
            QUERY_ITERATIONS (int, optional): number of iterations to query the Arduino. Defaults to 10.
            MIN_DATA_SIZE (int, optional): minimum size of the data. Defaults to 10.
            csv_name (str, optional): name of the csv file. Defaults to "readings_0.csv".

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

        self.log_adress = os.path.join("csv_folder", "log.txt")
        self.create_log()
        self.sensor_adress = os.path.join("csv_folder", csv_name)
        self.create_sensor_data()

        self.is_measuring = False
        self.is_titrating = False
        self.last_time = 0
        self.thirty_secs_passed = 0
        self.user_commands = []



    def __repr__(self) -> str:
        return f"Arduino: {self.port}"
    
    def __str__(self) -> str:
        return self.port
    
    def stop(self) -> None:
        """Stops the Arduino."""
        
        while self.serial.in_waiting > 0:
            self.read()

    # communication functions

    def read(self, in_send: bool = False, msg = "") -> bytes:
        """Reads a line from the Arduino.

        Returns:
            bytes: line from the Arduino
        """
        print(f"reading is locked: {self.lock.locked()}")
        with self.lock:

            rawline = self.serial.readline()

        if rawline.decode().count(",") > 5:

            try:

                data = rawline.decode().rstrip(",\r\n") # data formation: "time,violet,blue,green,yellow,orange,red"
                values = np.array(object=data.split(","), dtype=np.uint32)
                print(f"values: {values}")

                this_t = values[0] + self.thirty_secs_passed * 30000

                if self.last_time > this_t: 
                    self.thirty_secs_passed += 1
                    this_t += 30000

                self.last_time = this_t
                values[0] = this_t

                with open(self.sensor_adress, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(values)

            except Exception as e:
                if not in_send: print(e)
        
        else:
            if in_send and rawline == f"{msg}\n".encode():
                self.update_log(b"Sent command: " + rawline)
            else:
                self.update_log(rawline)

        return rawline


      
    def send(self, msg: str) -> None:
        """Sends a message to the Arduino.

        Args:
            msg (str): message to send
        """

        time.sleep(2)

        print(f"sending is locked: {self.lock.locked()}")

        with self.lock:

            self.serial.write(f"{msg}\n".encode())

        for i in range(self.QUERY_ITERATIONS):
            rawline = self.read(in_send=True, msg=msg)
            # print(f"rawline after sending: , {rawline}")
            if rawline == f"{msg}\n".encode():
                break

    # log functions

    def create_log(self) -> None:
        """Creates a log file for the Arduino."""

        with self.lock:
            with open(self.log_adress, "w") as f:
                f.write("")

    def get_log(self, n_entries = 10) -> str:
        """Returns the log of the Arduino.

        Returns:
            list[str]: log of the Arduino
        """

        with open(self.log_adress, "r") as f:
            log = f.read()

        if len(log.split("\n")) < n_entries:
            return log

        else:
            return "\n".join(log.split("\n")[-n_entries:])
    
    def update_log(self, line: bytes = b"") -> None:
        """Updates the log of the Arduino."""

        with open(self.log_adress, "r") as f:
            log = f.readlines()
        if line != b"":
            log_time = time.strftime("%H:%M:%S", time.localtime())
            log.append(log_time+" "+line.decode())
        with open(self.log_adress, "w") as f:
            f.writelines(log)

        
    # sensor functions
    
    def create_sensor_data(self) -> None:
        """Creates a file for the sensor data."""

        with open(self.sensor_adress, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Violet", "Blue", "Green", "Yellow", "Orange", "Red"])
            writer.writerow([0, 0, 0, 0, 0, 0, 0])
    

# extra functions

def attempt_connection(port: str, baudrate: int = 9600, timeout: int = 1, QUERY_ITERATIONS = 10, MIN_DATA_SIZE = 10, csv_name: str = "readings_0.csv") -> tuple[bool, Arduino]:
    """Attempts to connect to the Arduino.

    Args:
        port (str): port of the Arduino
        baudrate (int, optional): baudrate of the Arduino. Defaults to 9600.
        timeout (int, optional): timeout of the Arduino. Defaults to 1.
        QUERY_ITERATIONS (int, optional): number of iterations to query the Arduino. Defaults to 10.
        MIN_DATA_SIZE (int, optional): minimum size of the data. Defaults to 10.
        csv_name (str, optional): name of the csv file. Defaults to "readings_0.csv".

    Returns:
        bool: True if connection was successful, False otherwise
    """

    try:
        arduino = Arduino(port, baudrate, timeout, QUERY_ITERATIONS, MIN_DATA_SIZE, csv_name)
        print(f"Connected to Arduino on port {port}")
        return True, arduino
    except:
        return False, None

def get_arduino_ports() -> list[str]:
    """Returns a list of all available ports.

    Returns:
        list[str]: list of all available ports
    """
    arduino_ports = []
    
    for port, desc, hwid in sorted(comports()):
        print(f"port: {port}, desc: {desc}, hwid: {hwid}")
        
        if "SER" in hwid:
            arduino_ports.append(port)

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
