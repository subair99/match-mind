import json
from pathlib import Path

from .models import EventTimeline


def load(path: str | Path) -> EventTimeline:
    return EventTimeline.model_validate(json.loads(Path(path).read_text()))


def dump(timeline: EventTimeline, path: str | Path) -> None:
    Path(path).write_text(timeline.model_dump_json(indent=2))
