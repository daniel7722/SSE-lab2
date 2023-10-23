from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/")
def hello_world():
    return render_template("index.html")


def process_query(q):
    q = request.args.get("q")

    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 milion years ago"

    elif q == "asteroids":
        return "Unknown"

    elif q == "sausages":
        return "chicken"


@app.route("/query", methods=["GET"])
def query_handle():
    q = request.args.get("q")
    result = process_query(q)
    return result
