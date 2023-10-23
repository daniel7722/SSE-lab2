from app import process_query


def test_knows_about_dinosaurs():
    assert process_query(
            "dinosaurs"
            ) == "Dinosaurs ruled the Earth 200 milion years ago"


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_knows_about_sausages():
    assert process_query("sausages") == "chicken"


def test_does_know_about_me():
    assert process_query("Me") == "you"
