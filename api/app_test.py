from app import process_query, add_numbers


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == "Dinosaurs ruled the Earth 200 milion years ago"


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
