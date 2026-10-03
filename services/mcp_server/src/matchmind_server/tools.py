"""Tool logic. Week 1 reads the hand-made sample; Phase 4 switches to DynamoDB."""
from pathlib import Path

import event_timeline_kit as kit
from event_timeline_kit.schema import load

SAMPLE = Path(__file__).resolve().parents[4] / "data" / "sample" / "hero_match_events.json"


def _timeline(match_id: str) -> kit.EventTimeline:
    return load(SAMPLE)  # TODO: read from index.py (DynamoDB)


def find_moments(match_id: str, after: float, limit: int) -> list[dict]:
    return [e.model_dump() for e in kit.find_moments(_timeline(match_id), after, limit)]


def player_timeline(match_id: str, player: int) -> list[dict]:
    return [e.model_dump() for e in kit.player_timeline(_timeline(match_id), player)]
