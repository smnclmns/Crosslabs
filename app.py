from flask import Flask, render_template, request, flash
from UMLs.uml_handling import UML_Handler, get_ids

def check():

    with open("UMLs/txt_files/Calibration.txt","r") as cal:
        vorlage = cal.read().split("/n")

    with open("UMLs/txt_files/v1.txt", "r") as v1:
        entwurf = v1.read().split("/n")

    score = 0

    for i,line in enumerate(entwurf):

        entwurf_line = line.replace(" ", "")

        # if line is right: score += 1
        
        pass


    
    return score


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    handler = UML_Handler()
    if request.method == "POST":
        text_input = request.form["user-input"]
    else:
        text_input = handler.get_plantuml_text("v1")

    handler.add_uml_file(text_input)

    
    
   
    
    return render_template("index.html", uml_src=handler.get_plantuml_url("v1", "svg"), state = check())




        
if __name__ == "__main__":

    app.run(debug=True, port=8000)



