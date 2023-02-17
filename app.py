from flask import Flask, render_template, request, flash
from UMLs.uml_handling import UML_Handler, get_ids

def check(vorlage_level: str,keywords: list[str], entwurf_input: str) -> dict:

    ouput_dict = {
        "score": 0,
        "tips": [""]
    }

    with open(vorlage_level,"r") as f:
        vorlage = f.read().split("/n")
        vorlage = [line.replace(" ", "") for line in vorlage]

    with open(entwurf_input, "r") as v1:
        entwurf = v1.read().split("/n")
        # entwurf = [line.replace(" ", "") for line in entwurf]


    for i, line in enumerate(entwurf):

        words = line.split(" ")

        for word in words:

            if word in keywords: ouput_dict["score"] += 1

    
    return ouput_dict


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    handler = UML_Handler()
    if request.method == "POST":
        text_input = request.form["user-input"]
    else:
        text_input = handler.get_plantuml_text("v1")

    handler.add_uml_file(text_input)

    vorlage = r"UMLs\txt_files\Calibration.txt"
    keywords = ["calbibration", "pump", "stepper motor", "Initializing"]
    entwurf = r"UMLs\txt_files\v1.txt"

    output_dict = check(vorlage, keywords, entwurf)

    score = output_dict["score"]   
    
    return render_template("index.html",
     uml_src=handler.get_plantuml_url("v1", "svg"),
     score=score)




        
if __name__ == "__main__":

    app.run(debug=True, port=8000)



