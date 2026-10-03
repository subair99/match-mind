from pathlib import Path

from event_timeline_kit import find_moments, player_timeline
from event_timeline_kit.schema import load

SAMPLE = Path(__file__).parents[3] / "data" / "sample" / "hero_match_events.json"


def test_sample_loads_and_ranks():
    tl = load(SAMPLE)
    assert find_moments(tl)[0].type == "goal"
    assert [e.event_id for e in player_timeline(tl, 7)] == ["e1", "e2"]
