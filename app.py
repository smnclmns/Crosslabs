from flask import Flask, render_template, request, flash
from uml_handling import UML_Handler, get_ids

app = Flask(__name__)

@app.route("/")
def home():
    handler = UML_Handler()
    return render_template("index.html", src=handler.get_plantuml_url('index'))

if __name__ == "__main__":

    app.run(debug=True, port=8000)

