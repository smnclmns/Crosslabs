# Crosslabs 

is a project to give students an easy start for creating their first automation in the lab using an Arduino mircocontroller.

## Basic Idea

The students write code in the Blockly environment that is then uploaded to the Arduino Board or evaluated by another programm. The code blocks that can be found in the Blockly Environment represent a chunk of Arduino code (C++) that can be added to the Arduino Sketch. The specific insertion of these code chunks will be realised by a self-written python module "ino_Sketches". The module prvides handy methods to insert the needed lines of code at the right places in order for the blockly program to work. It has the following features:

 - Evaluation if the program can be compiled without any issues (using the arduino-cli.exe)

 - Evaulation if the program contains the obligatory steps to execute a titration, e.g.

    - Start- and Stop-mechanisms

    - Motorcontrol

    - Colormeasurement

 - Uploading the sketch to the arduino board (again via the aruino-cli.exe)

 ## Next steps:

 - Finishing the website

 - add the python backbone

 - create the blockly Implementation