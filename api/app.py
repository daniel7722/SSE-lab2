from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/query", methods=["GET"])
def get_query():
    q = request.args.get("q")
    result = process_query(q)
    return result


def process_query(q):
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 milion years ago"

    elif q == "asteroids":
        return "Unknown"

    elif q == "sausages":
        return "chicken"

    elif q == "dadjoke":
        return "DO NOT TELL ME DAD JOKE"


def add_numbers(a, b):
    return a+b


@app.route("/solve_sudoku", methods=["POST"])
def solve_sudoku():
    uploaded_file = request.files['dat_file']
    dat_file_path = os.path.join("./temporary", "input.dat")
    dat_file_output_path = os.path.join("./temporary", "solution.dat")
    uploaded_file.save(dat_file_path)
    cplusplus_command = "./solver "
    +dat_file_path
    +" "
    +dat_file_output_path
    subprocess.run(cplusplus_command, shell=True)
    data = convert_file(dat_file_output_path)
    return render_template("solution.html", data=data)


def convert_file(datfile):
    data = []
    with open(datfile, 'r') as file:
        for row in range(9):
            row_data = []
            for col in range(9):
                content = file.read(1)
                row_data.append(content)
            file.read(1)
            data.append(row_data)
    return data
