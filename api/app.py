from flask import Flask, render_template, request
import re
import math
import requests
import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    return render_template("hello.html", name=input_name, age=input_age)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/sudoku")
def sudoku():
    return render_template("portfolio.html")


@app.route("/query", methods=["GET"])
def get_query():
    q = request.args.get("q")
    result = process_query(q)
    return result


def process_query(q):
    if q == "dinosaurs":
        return render_template("dinosaur.html")

    elif q == "asteroids":
        return "Unknown"

    elif q == "sausages":
        return "chicken"

    elif q == "dadjoke":
        return "DO NOT TELL ME DAD JOKE"

    elif q == "What is your name?":
        return "DR"

    elif "largest" in q:
        request_string = q
        numbers = re.findall(r'\d+', request_string)
        numbers = [int(num) for num in numbers]
        return str(largest(numbers))

    elif "plus" in q:
        request_string = q
        numbers = re.findall(r'\d+', request_string)
        numbers = [int(num) for num in numbers]
        return str(add_numbers(numbers))

    elif "square" in q:
        request_string = q
        numbers = re.findall(r'\d+', request_string)
        numbers = [int(num) for num in numbers]
        return str(squareAndCube(numbers))

    elif "multiplied" in q:
        request_string = q
        numbers = re.findall(r'\d+', request_string)
        numbers = [int(num) for num in numbers]
        return str(multiply_numbers(numbers))

    else:
        return render_template("index.html")


def add_numbers(listOfNumber):
    return sum(listOfNumber)


def largest(listOfNumber):
    return max(listOfNumber)


def squareAndCube(listOfNumber):
    for number in listOfNumber:
        cube = round(math.pow(number, 1 / 3))
        square = round(math.pow(number, 1 / 2))
        if cube**3 == number and square**2 == number:
            return number


def multiply_numbers(listOfNumber):
    total = 1
    for number in listOfNumber:
        total *= number
    return total


# hello
@app.route("/solve_sudoku", methods=["POST"])
def solve_sudoku():
    grid_data = []
    for row in range(9):
        row_data = []
        for col in range(9):
            input_name = f'{row}.{col}'
            cell_value = request.form.get(input_name, ".")
            if (cell_value == ''):
                cell_value = '.'
            row_data.append(cell_value)
        grid_data.append(row_data)
    print(grid_data)
    if is_board_valid(grid_data):
        solved = solve_board(grid_data, 0)
        if solved:
            return render_template("solution.html", data=grid_data)
    print("No Solution Found")
    return render_template("no_solution.html")


def solve_board(board, depth):
    print(depth)
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                for num in map(str, range(1, 10)):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board, depth + 1):
                            return True
                        board[row][col] = '.'
                return False
    return True


def is_valid_move(board, row, col, num):
    # Check if the number is already in the same row or column
    if num in board[row] or num in [board[i][col] for i in range(9)]:
        return False
    # Check if the number is in the same 3x3 subgrid
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False
    return True


def is_board_valid(board):
    for row in board:
        for num in map(str, range(1, 10)):
            count_row = 0
            for pos1 in row:
                if num == pos1:
                    count_row += 1
            if count_row == 2:
                return False
    for col in range(9):
        for num in map(str, range(1, 10)):
            count_col = 0
            for pos2 in [board[i][col] for i in range(9)]:
                if num == pos2:
                    count_col += 1
            if count_col == 2:
                return False
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            for num in map(str, range(1, 10)):
                count_square = 0
                for i in range(row, row + 3):
                    for j in range(col, col + 3):
                        if board[i][j] == num:
                            count_square += 1
                        if count_square == 2:
                            return False
    return True


@app.route("/github_api", methods=["POST"])
def github_api():
    username = request.form.get("username")
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    name_length = len(username) + 1
    repo_name, repo_dates, repo_commit_table, repo_table = [], [], [], []
    print(response.status_code)
    if response.status_code == 200:
        repos = response.json()  # data returned is a list of 'repository' entities
        for repo in repos:
            repo_name.append(repo["full_name"][name_length:])
            repo_dates.append(repo["updated_at"][:10])
            reponame = repo["name"]
            repo_commit_info = []
            more_info = requests.get(f"https://api.github.com/repos/{username}/{reponame}/commits")
            more_info_JSON = more_info.json()
            try:
                repo_commit_info.append(more_info_JSON[0]["sha"])
                repo_commit_info.append(more_info_JSON[0]["commit"]["author"]["name"])
                repo_commit_info.append(more_info_JSON[0]["commit"]["author"]["date"][:10])
                repo_commit_info.append(more_info_JSON[0]["commit"]["message"])
                repo_commit_table.append(repo_commit_info)
            except KeyError:
                repo_commit_info.append("Private")
                repo_commit_info.append("Private")
                repo_commit_info.append("Private")
                repo_commit_info.append("Private")
                repo_commit_table.append(repo_commit_info)
        for n, d in zip(repo_name, repo_dates):
            repo_table.append([n, d])
    else:
        return "run out of rate limit"
    return render_template("githubresponse.html", name=username, repotable=repo_table, committable=repo_commit_table)


def get_trending_repositories(limit=10):
    base_url = "https://api.github.com/search/repositories"
    today = datetime.date.today()
    one_month = today - datetime.timedelta(days=30)
    query_params = {
        "q": f"created:{one_month}",
        "sort": "stars",
        "order": "desc"
    }
    headers = {
        "Accept": "application/vnd.github.preview"
    }

    response = requests.get(base_url, params=query_params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        repositories = data.get("items", [])[:limit]
        return repositories
    else:
        print(f"Failed to retrieve trending repositories. Status code: {response.status_code}")
        return []


@app.route("/github_form")
def github_form():
    return render_template("githubapi.html")


@app.route("/github_trending")
def github_trending():
    trending_repositories = get_trending_repositories()
    trend_repo = []
    for repo in trending_repositories:
        trend_repo.append([repo["name"], repo["description"], repo["html_url"]])
    print(trend_repo)
    return render_template("github_trending.html", trendrepo=trend_repo)
