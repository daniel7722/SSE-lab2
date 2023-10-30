import pytest
from app import app, process_query, render_template


@pytest.fixture
def client():
    return app.test_client()


def test_knows_about_dinosaurs():
    with app.test_request_context():
        assert render_template("dinosaur.html") in process_query("dinosaurs")


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_knows_about_sausages():
    assert process_query("sausages") == "chicken"


def test_can_deliver_dad_jokes():
    result = process_query("dadjoke")
    assert result == "DO NOT TELL ME DAD JOKE"


def test_knows_team_name():
    assert process_query("What is your name?") == "DR"


def test_knows_largest(client):
    response = client.get('/query?q=Which of the following numbers is the largest: 1, 35, 8?')
    assert response.data == b'35'

    response = client.get('/query?q=Which of the following numbers is the largest: 70, 35, 8?')
    assert response.data == b'70'

    response = client.get('/query?q=Which of the following numbers is the largest: 1, 35, 93?')
    assert response.data == b'93'


def test_knows_plus(client):
    response = client.get('/query?q=What is 84 plus 50?')
    assert response.data == b'134'

    response = client.get('/query?q=What is 77 plus 17?')
    assert response.data == b'94'

    response = client.get('/query?q=What is 95 plus 1?')
    assert response.data == b'96'


def test_knows_square_cube(client):
    response = client.get('/query?q=Which of the following numbers is both a square and a cube: 2197, 2602, 4096, 1991, 4, 100, 1193?')
    assert response.data == b'4096'

    response = client.get('/query?q=Which of the following numbers is both a square and a cube: 4518, 484, 3655, 1, 2197, 2746, 3473?')
    assert response.data == b'1'

    response = client.get('/query?q=Which of the following numbers is both a square and a cube: 3485, 4147, 3025, 64, 599, 3220, 1728?')
    assert response.data == b'64'


def test_knows_multiply(client):
    response = client.get('/query?q=What is 15 multiplied by 86?')
    assert response.data == b'1290'

    response = client.get('/query?q=What is 17 multiplied by 48?')
    assert response.data == b'816'

    response = client.get('/query?q=What is 8 multiplied by 3?')
    assert response.data == b'24'
