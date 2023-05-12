from flask import Flask, render_template, request, flash, url_for
from UMLs.uml_handling import UML_Handler, get_ids

def check(vorlage_level: str,keywords: list[str], entwurf_input: str) -> dict:

    ouput_dict = {
        "score": 0,
        "Oscore": 0,
        "tips": [""]
    }




    with open(vorlage_level,"r") as f:
        vorlage = f.read().lower().split()
        vorlage = [line.replace(" ", "") for line in vorlage]

    with open(entwurf_input, "r") as v1:
        entwurf = v1.read().lower().split()

    kwords=[]
    keywords1 = keywords.copy()

    for line in entwurf:
        words = line.split()
        for word in words:
                if word in keywords1: 
                    ouput_dict["score"] += 1
                    keywords1.remove(word)
                    kwords.append(word)
    for m,kword in enumerate(kwords):
        if kword == keywords[m]:
            ouput_dict["Oscore"] += 1
                    
    return ouput_dict

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

@app.route("/drafts", methods=["POST", "GET"])
def Drafts():
    return render_template("drafts.html")




        
if __name__ == "__main__":

    app.run(debug=True, port=8000)



