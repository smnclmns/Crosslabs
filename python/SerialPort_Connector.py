import sys

import serial
from serial.tools.list_ports import comports

arg = sys.argv[1]

print(f"\nreveived the arg: {arg}")

