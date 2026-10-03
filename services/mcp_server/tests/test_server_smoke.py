from matchmind_server import tools


def test_find_moments_from_sample():
    assert tools.find_moments("hero-match", 0.0, 1)[0]["type"] == "goal"
