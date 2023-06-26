from flask import Flask, render_template, request, flash, url_for

import time, sys, threading
from static.py.Levels import get_level_names
from static.py.Arduino_communication import Arduino, attempt_connection, get_arduino_ports, connection_state


# Initialing arduino variables

connected = False
arduino: Arduino = None

# Initialising the Flask app

app = Flask(__name__)

def check_arduino(connected: bool, arduino: Arduino):

    if connected and isinstance(arduino, Arduino):
        arduino.measurement()


# Routes for the different pages

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

""" @app.route("/start", methods=["POST", "GET"])
def start():
    t = threading.Timer(1.0, check_arduino, args=[connected, arduino])
    t.start() """

@app.route("/playground", methods=["POST", "GET"])
def playground():

    global connected
    global arduino

    response = ">"

    input_dict = {
        "connect": "",
        "query-input": "",        
    }

    if request.method == "POST":

        for key in input_dict:

            inp = request.form.get(key)

            if inp == None: continue
            else:
                input_dict[key] = inp

        if connected and input_dict["query-input"] != "":
            arduino.send(input_dict["query-input"])
            log = arduino.get_log()
            if len(log) > 7: response = "\n> ".join(log[-7:])
            else: response = "\n> ".join(log)

        if input_dict["query-input"] == "mock":
            t = threading.Timer(1.0, check_arduino, args=[connected, arduino])
            t.start()

        if input_dict["connect"] == "connect":
            if get_arduino_ports() == []: response = "No Arduino found."
            else:
                connected, arduino = attempt_connection(get_arduino_ports()[0])
                response = connection_state(connected, arduino)


    return render_template("playground.html", response=response, connected=connected)





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
        "Tut_calibration_steps": 0,
        "Tut_calibration_delay": 0,
        }
    
    tips= ""
    score = 0

    if request.method == "POST":
        
        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    for key, val in input_dict.items():
        
        if key == "Tut_calibration_steps":
            if val != "500": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            else: score += 1

        if key == "Tut_calibration_delay":
            if val != "1000": tips += f"You didn't set the right {key.split('_')[1]}-value.\n"
            else: score += 1

    return render_template("Levels/level1.html",
        uml_src=url_for('static', filename='assets/SVGs/Level1.svg'),
        value=score,
        tips=tips,
    )

@app.route("/workspace/level2", methods=["POST", "GET"])
def level2():

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

    return render_template("Levels/level2.html",
        uml_src=url_for('static', filename='assets/SVGs/Level2.svg'),
        value=score,
        tips=tips,
    )

@app.route("/workspace/level3", methods=["POST", "GET"])
def level3():

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

    app.run(debug=True)



