from app import app, process_query, add_numbers, render_template


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


def test_add_number():
    result = add_numbers(2, 3)
    assert result == 5
