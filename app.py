from flask import Flask, render_template, request, url_for, redirect, send_file, jsonify


import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

from static.py.Arduino_communication import Arduino, attempt_connection, get_arduino_ports, connection_state


# Initialing arduino variables

connected = False
arduino: Arduino = None

# Initialising the Flask app

app = Flask(__name__)

# Routes for the different pages

@app.route("/", methods=["POST", "GET"]) # Home page
def home():
    return render_template("home.html")

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
    
    else:
        return jsonify({"data": "no data"})
    
@app.route("/refresh_log", methods=["POST", "GET"]) # updates the log
def refresh_log():
    pass

    


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
    return render_template("workspace.html", lvl1="disabled", lvl2="disabled")



@app.route("/workspace/tutorial", methods=["POST", "GET"])
def tutorial():

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
    
    return render_template("Levels/tutorial.html",
     uml_src=url_for('static', filename='assets/SVGs/Calibration.svg'),
     value=score,
     tips=tips,
     visible_tips=visible_tips,
    )

@app.route("/workspace/level1", methods=["POST", "GET"])
def level1():

    input_dict = {
        "Boolean_state_1": 0,
        "Condition_1": 0,
        "Condition_2": 0,
        "Boolean_state_2": 0,
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
        
        if key == "Boolean_state_1":
            if val != "false" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "false": score += 1

        if key == "Condition_1":
            if val != "<" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "<": score += 1

        if key == "Boolean_state_2":
            if val != "true" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "true": score += 1

        if key == "Condition_2":
            if val != "<" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "<": score += 1

    return render_template("Levels/level1.html",
        uml_src=url_for('static', filename='assets/SVGs/Level1.svg'),
        uml_src2=url_for('static', filename='assets/SVGs/Level1.1.svg'),
        value=score,
        tips=tips,
        visible_tips = visible_tips
    )

@app.route("/workspace/level2", methods=["POST", "GET"])
def level2():

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
            if val != "1/32" and val != "": tips += f"You didn't set the right Microsteps"
            elif val == "1/32": score += 1

        if key == "Velocity_1":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\n"
            elif val == "0": score += 1
        if key == "Velocity_2":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\n"
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
                tips += f"The {key}-value should be a numeric value less than 10.\n"
            else:
                score += 1
        if key == "Velocity_5":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\n"
            elif val == "0": score += 1
        if key == "Velocity_6":
            if val != "0" and val != "": tips += f"You didn't set the right {key}-value.\n"
            elif val == "0": score += 1

    return render_template("Levels/level2.html",
        uml_src=url_for('static', filename='assets/SVGs/Stepper1.svg'),
        uml_src2=url_for('static', filename='assets/Gifs/fullround.gif'),
        value=score,
        tips=tips,
        visible_tips=visible_tips,
    )

@app.route("/workspace/level3", methods=["POST", "GET"])
def level3():

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

        if key == "Microstep":
            if val != "1/32" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "1/32": score += 1

        if key == "Velocity_1":
            if val != "0" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "0": score += 1
        if key == "Velocity_2":
            if val != "0" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "0": score += 1
        if key == "Velocity_3":
            if val != "" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val < "10": score += 1
        if key == "Velocity_4":
            if val != "" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val < "10": score += 1
        if key == "Velocity_5":
            if val != "0" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "0": score += 1
        if key == "Velocity_6":
            if val != "0" and val != "": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            elif val == "0": score += 1

    return render_template("Levels/level3.html",
        uml_src=url_for('static', filename='assets/SVGs/Level3.svg'),
        value=score,
        tips=tips,
    )

@app.route("/workspace/level4", methods=["POST", "GET"])
def level4():

    input_dict = {
        "Tut_iterations": 0,
        "Tut_steps": 0,
        "Tut_delay": 0,
    }

    tips= ""
    score = 0

    if request.method == "POST":

        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():

        if key == "Tut_iterations":
            if val != "15": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            else: score += 1

        if key == "Tut_steps":
            if val != "500": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            else: score += 1

        if key == "Tut_delay":
            if val != "1000": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            else: score += 1

    return render_template("Levels/level4.html",
        uml_src=url_for('static', filename='assets/SVGs/Level4.svg'),
        value=score,
        tips=tips,
    )


if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)



