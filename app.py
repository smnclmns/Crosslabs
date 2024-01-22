from flask import Flask, render_template, request, url_for, redirect, send_file, jsonify


import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
import time

from static.py.Arduino_communication import Arduino, attempt_connection, get_arduino_ports, connection_state

#User Progress
enable_level1 = False
enable_level2 = False
enable_level3 = False
enable_level4 = False

# Initializing arduino variables

connected = False
arduino: Arduino = None

# Initialising the Flask app

app = Flask(__name__)

# Routes for the different pages

@app.route("/", methods=["POST", "GET"]) # Home page
def home():
    return render_template("home.html")
    

@app.route("/Automated Titration", methods=["POST", "GET"]) # Automated Titration page
def AutomatedTitration():
    
    # Initialising the global variables

    global connected
    global arduino
    

    # Initialising the response

    is_measuring = False
    is_titrating = False
    is_reseting = False
    is_nullpoint = False
    is_nullpoint = False
    is_forward = False
    is_backward = False
    is_change = False
    is_calibrating = False
    terminal_info = ""
    log = ""
    

    # Initialising the input_dict

    input_dict = {
        "connect": "",
        "query-input": "",
        "cali-value":"",

    }


    # if the user has submitted the form, the input_dict will be updated

    if request.method == "POST":

        for key in input_dict:

            inp = request.form.get(key)

            if inp == None: continue
            else:
                input_dict[key] = inp

        # if the user has submitted the form and wants to connect to the Arduino, the connection will be attempted

        if input_dict["connect"] == "connect":
            ino_ports = get_arduino_ports()
            if ino_ports == []:
                terminal_info = "No Arduino found."
            else:
                connected, arduino = attempt_connection(ino_ports[0])
                terminal_info = connection_state(connected, arduino)
                if terminal_info == "> Something went wrong":
                    print("Something went wrong")
                    connected = False

            # Check if weight input is provided and is a number
        cali_value = input_dict.get("cali-value", "").strip()

        if cali_value.replace(".", "", 1).isdigit():  # Allow one decimal point
            weight_value = float(cali_value)
            # Store the weight_value for later calculations
            # You can save it in a database, session, or any suitable storage
            print(f"Weight value submitted: {weight_value}")
        else:
            weight_value = ""  # or set it to another default value if needed
    
            
        
        last_titration_value = "123.45"
        # if the user has submitted the form and wants to query the Arduino, the query will be attempted

        if connected and input_dict["query-input"] != "":
            arduino.send(input_dict["query-input"])

        if connected and input_dict["query-input"] == "mock":
            arduino.is_measuring = True
            is_measuring = True

        if connected and input_dict["query-input"] == "Start":
            arduino.is_titrating = True
            is_titrating = True

        if connected and input_dict["query-input"] == "Stop":
            arduino.is_titrating = False
            is_titrating = False
            arduino.is_measuring = False
            is_measuring = False

        if connected and input_dict["query-input"] == "Reset":
            arduino.is_reseting = True
            is_reseting = True

        if connected and input_dict["query-input"] == "Cali":
            arduino.is_calibrating = True
            is_calibrating = True

        if connected and input_dict["query-input"] == "Foward":
            arduino.is_foward = True
            is_forward = True

        if connected and input_dict["query-input"] == "Backward":
            arduino.is_backward = True
            is_backward = True

        if connected and input_dict["query-input"] == "Nullpoint":
            arduino.is_nullpoint = True
            is_nullpoint = True

        if connected:
            time.sleep(0.1) 
            log = arduino.get_log()

            
            # Check if weight input is provided and is a number
            cali_value = input_dict.get("cali-value", "").strip()

            if cali_value.replace(".", "", 1).isdigit():  # Allow one decimal point
                weight_value = float(cali_value)
                # Store the weight_value for later calculations
                # You can save it in a database, session, or any suitable storage
                print(f"Weight value submitted: {weight_value}")
            else:
                weight_value = ""  # or set it to another default value if needed

        
            
        
    # rendering the template with the right values

    return render_template("Automated Titration.html",last_titration_value=last_titration_value,previous_cali_value=weight_value, connected=connected, is_titrating=is_titrating, is_measuring=is_measuring, is_reseting=is_reseting, is_nullpoint=is_nullpoint, is_forward=is_forward, is_backward=is_backward, is_change=is_change, is_calibrating=is_calibrating, log=log)

    
@app.route("/create_plot", methods=["POST", "GET"]) # Page for getting the data from the csv file
def create_plot():

    # Reading the data from the csv file
    data = pd.read_csv("csv_folder/readings_0.csv") # columns: time_in_ms, violet, blue, green, yellow, orange, red

    # Creating the plot

    plt.plot(data["Time"]/1000, data["Violet"], color="violet")
    plt.plot(data["Time"]/1000, data["Blue"], color="blue")
    plt.plot(data["Time"]/1000, data["Green"], color="green")
    plt.plot(data["Time"]/1000, data["Yellow"], color="yellow")
    plt.plot(data["Time"]/1000, data["Orange"], color="orange")
    plt.plot(data["Time"]/1000, data["Red"], color="red")

    plt.xlabel("Time in s")
    plt.ylabel("Sensorvalues I [-]")
    plt.grid()

    # Saving the plot as a png file
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    # deleting the plot from the memory
    plt.cla()
    plt.clf()

    # Returning the plot
    return send_file(img, mimetype="image/png")
    

@app.route("/read_serial", methods=["POST", "GET"]) # Page for getting the data from the serial connection
def read_serial():
    
    # Reading the data from the serial connection
    if connected and arduino.is_measuring:
        rawline = arduino.read()

        return jsonify({"data": rawline.decode()})
    
    if connected and arduino.is_titrating:
        rawline = arduino.read()

        return jsonify({"data": rawline.decode()}) 
    
    if connected:
        rawline = arduino.read()

        return jsonify({"data": rawline.decode()}) 
        
    else:
        return jsonify({"data": "no data"})
    
@app.route("/refresh_log", methods=["POST", "GET"]) # updates the log
def refresh_log():
    log_path = "csv_folder/log.txt"  # Update the path to your log.txt file
    
    try:
        n_entries = 22
        log_lines = []

        with open(log_path, "r") as log_file:
            for line in log_file:
                log_lines.append(line)
        
        # Retrieve the last 15 entries or the entire log if fewer than 15
        log_content = "".join(log_lines[-n_entries:])

        return jsonify({"log": log_content})
    
    except Exception as e:
        return jsonify({"error": str(e)})
       

    


@app.route("/playground", methods=["POST", "GET"])
def playground():

    # Initialising the global variables

    global connected
    global arduino

    # Initialising the response

    is_measuring = False
    terminal_info = ""
    log = ""

    # Initialising the input_dict

    input_dict = {
        "connect": "",
        "query-input": "",        
    }

    # if the user has submitted the form, the input_dict will be updated

    if request.method == "POST":

        for key in input_dict:

            inp = request.form.get(key)

            if inp == None: continue
            else:
                input_dict[key] = inp

        # if the user has submitted the form and wants to connect to the Arduino, the connection will be attempted

        if input_dict["connect"] == "connect":
            ino_ports = get_arduino_ports()
            if ino_ports == []:
                terminal_info = "No Arduino found."
            else:
                connected, arduino = attempt_connection(ino_ports[0])
                terminal_info = connection_state(connected, arduino)
                if terminal_info == "> Something went wrong":
                    print("Something went wrong")
                    connected = False


        # if the user has submitted the form and wants to query the Arduino, the query will be attempted

        if connected and input_dict["query-input"] != "":
            arduino.send(input_dict["query-input"])

        if connected and input_dict["query-input"] == "mock":
            arduino.is_measuring = True
            is_measuring = True

        if connected and input_dict["query-input"] == "Start":
            arduino.is_measuring = True
            is_measuring = True

        if connected and input_dict["query-input"] == "Stop":
            arduino.is_measuring = False
            is_measuring = False

        if connected: log = arduino.get_log()

    # rendering the template with the right values

    return render_template("playground.html", connected=connected,is_measuring=is_measuring, log=log)





@app.route("/workspace", methods=["GET", "POST"])
def workspace():
    global enable_level1
    global enable_level2
    global enable_level3
    global enable_level4

    return render_template("workspace.html", lvl1="enabled" if enable_level1 else "disabled",  lvl2="enabled" if enable_level2 else "disabled",  lvl3="enabled" if enable_level3 else "disabled",  lvl4="enabled" if enable_level4 else "disabled")

    



@app.route("/workspace/tutorial", methods=["POST", "GET"])
def tutorial():

    #Progress
    global enable_level1
    maximum_score=3


    # All inputs from the user in the tutorial page

    input_dict = {
        "Tut_iterations": 0,
        "Tut_steps": 0,
        "Tut_delay": 0,
    }

    # initialising the score and tips

    tips= ""
    score = 0
    visible_tips = False

    # if the user has submitted the form, the input_dict will be updated

    if request.method == "POST":

        visible_tips = True
        
        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    # checking the input_dict for the right values and updating the score and tips
    
    for key, val in input_dict.items():

        if key == "Tut_iterations":
            if val != "15" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "15": score += 1

        if key == "Tut_steps":
            if val != "500" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "500": score += 1

        if key == "Tut_delay":
            if val != "1000" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "1000": score += 1
        
    # rendering the template with the right values
    if score == maximum_score:
            enable_level1 = True
    return render_template("Levels/tutorial.html",
     uml_src=url_for('static', filename='assets/SVGs/Calibration.svg'),
     value=score,
     tips=tips,
     visible_tips=visible_tips,
    )

@app.route("/workspace/level1", methods=["POST", "GET"])
def level1():
    #Progress
    global enable_level2
    maximum_score=4

    input_dict = {
        "Titration_Condition": 0,
        "First_Light_Condition": 0,
        "Second_Light_Condition": 0,
        "End_Condition": 0,
        }
    
    tips= ""
    score = 0
    visible_tips = False

    if request.method == "POST":

        visible_tips=True
        
        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():
        
        if key == "Titration_Condition":
            if val != "false" and val != "": tips += f"You didn't set the right initial boolean state.\n"
            elif val == "false": score += 1

        if key == "First_Light_Condition":
            if val != "<" and val != "": tips += f"You didn't set the right [ < | > ] symbole for the first check.\n"
            elif val == "<": score += 1

        if key == "End_Condition":
            if val != "true" and val != "": tips += f"You didn't set the right boolean state for the end of the Titration.\n"
            elif val == "true": score += 1

        if key == "Second_Light_Condition":
            if val != "<" and val != "": tips += f"You didn't set the right [ < | > ] symbole for the repeat check.\n"
            elif val == "<": score += 1
    if score == maximum_score:
            enable_level2 = True
    return render_template("Levels/level1.html",
        uml_src=url_for('static', filename='assets/SVGs/Level1.svg'),
        uml_src2=url_for('static', filename='assets/SVGs/Level1.1.svg'),
        value=score,
        tips=tips,
        visible_tips = visible_tips
    )

@app.route("/workspace/level2", methods=["POST", "GET"])
def level2():
    global enable_level3
    maximum_score=7

    input_dict = {
        "Microstep_1":0,
        "Velocity_1":0,
        "Velocity_2":0,
        "Velocity_3":0,
        "Velocity_4":0,
        "Velocity_5":0,
        "Velocity_6":0,

    }

    tips= ""
    score = 0
    visible_tips = False

    if request.method == "POST":
        visible_tips=True

        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():

        if key == "Microstep_1":
            if val != "1/32" and val != "": tips += f"You didn't set the right Microstep setting"
            elif val == "1/32": score += 1

        if key == "Velocity_1":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\nThe motor should be stopped while measuring.\n"
            elif val == "0": score += 1
        if key == "Velocity_2":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\nThe motor should be stopped while measuring.\n"
            elif val == "0": score += 1
        if key == "Velocity_3":
            if not val:
                tips += f"You didn't set the right {key}-value.\n"
            elif not val.isdigit() or float(val) >= 10:
                tips += f"The {key}-value should be a numeric value less than 10.\n"
            else:
                score += 1
        if key == "Velocity_4":
            if not val:
                tips += f"You didn't set the right {key}-value.\n"
            elif not val.isdigit() or float(val) >= 10:
                tips += f"The {key}-value should be a numeric value less than 10.\nThe motor should be stopped while measuring.\n"
            else:
                score += 1
        if key == "Velocity_5":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\nThe motor should be stopped while measuring.\n"
            elif val == "0": score += 1
        if key == "Velocity_6":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\n"
            elif val == "0": score += 1
    if score == maximum_score:
            enable_level3 = True
    return render_template("Levels/level2.html",
        uml_src=url_for('static', filename='assets/SVGs/Stepper1.svg'),
        uml_src2=url_for('static', filename='assets/Gifs/fullround.gif'),
        value=score,
        tips=tips,
        visible_tips=visible_tips,
    )

@app.route("/workspace/level3", methods=["POST", "GET"])
def level3():
    global enable_level4
    maximum_score=3
    input_dict = {
        "Tut_Command":0,
        "Tut_Steps":0,
        "Tut_Variable":0,
       

    }

    tips= ""
    score = 0
    visible_tips = False

    if request.method == "POST":
        visible_tips=True

        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():

        if key == "Tut_Command":
            if val != "Continue" and val != "": tips += f"You didn't set the right function.\nThese could be break; continue; pass; end"
            elif val == "Continue": score += 1

        if key == "Tut_Steps":
            if val != "Steps" and val != "": tips += f"You didn't set the right Varibale inside the calibration function.\n"
            elif val == "Steps": score += 1
        if key == "Tut_Variable":
            if val != "Volume" and val != "": tips += f"What do we want to know after a Titration is ended if it is not directly the concentration.\n"
            elif val == "Volume": score += 1
    
    if score == maximum_score:
            enable_level4 = True
    return render_template("Levels/level3.html",
        uml_src=url_for('static', filename='assets/SVGs/Examplelightsensor.svg'),
        value=score,
        tips=tips,
        visible_tips = visible_tips,
    )

@app.route("/workspace/level4", methods=["POST", "GET"])
def level4():

    input_dict = {
        "Tut_Step": 0,
        "Tut_calibration": 0,
        "Tut_start": 0,
        "Tut_Measure":0,
        "Tut_condition":0,
        "Tut_Variable":0,
        "Condition_1":0,
    }

    tips= ""
    score = 0
    visible_tips = False

    if request.method == "POST":
        visible_tips = True
    
        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():
        if key == "Tut_Step":
            if val != "1/32" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "1/32": score += 1

        if key == "Tut_calibration":
            if val != "Calibration" and val != "": tips += f"You didn't set the right Function.\n"
            elif val == "Calibration": score += 1
        if key == "Tut_start":
            if val != "StartTitration" and val != "": tips += f"You didn't set the right {key.split('_')[1]}.\n"
            elif val == "StartTitration": score += 1
        if key == "Tut_Measure":
            if val != "Measure_color" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "Measure_color": score += 1
        if key == "Condition_1":
            if val != "<" and val != "": tips += f"You didn't set the right {key.split('_')[1]}.\n"
            elif val == "<": score += 1

        if key == "Tut_condition":
            if val != "True" and val != "": tips += f"You didn't set the right Varibale inside the calibration function.\n"
            elif val == "True": score += 1
        if key == "Tut_Variable":
            if val != "Volume" and val != "": tips += f"You didn't set the right {key.split('_')[1]}.\n"
            elif val == "Volume": score += 1

       

    return render_template("Levels/level4.html",
        uml_src=url_for('static', filename='assets/SVGs/Level4.svg'),
        value=score,
        tips=tips,
        visible_tips = visible_tips,
    )


if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)



