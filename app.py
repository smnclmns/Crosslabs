from flask import Flask, render_template, request, flash, url_for
from static.py.Levels import get_level_names



app = Flask(__name__)

@app.route("/dev", methods=["POST", "GET"])
def dev():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

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

    # if the user has submitted the form, the input_dict will be updated

    if request.method == "POST":
        
        for key, val in input_dict.items():

            inp = request.form.get(key)
            if inp == None: continue
            else: input_dict[key] = inp

    # checking the input_dict for the right values and updating the score and tips
    
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

    # rendering the template with the right values
    
    return render_template("Levels/tutorial.html",
     uml_src=url_for('static', filename='assets/SVGs/Calibration.svg'),
     value=score,
     tips=tips,
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

    app.run(debug=True, port=8000)



