from flask import Flask, render_template, request, flash
from UMLs.uml_handling import UML_Handler, get_ids

app = Flask(__name__)

@app.route("/")
def home():
    handler = UML_Handler()
    return render_template("index.html", uml_src=handler.get_plantuml_url('arduino_uml', "svg"))

if __name__ == "__main__":

    app.run(debug=True, port=8000)

