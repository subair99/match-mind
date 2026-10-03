from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Event(BaseModel):
    event_id: str
    t_start: float = Field(ge=0)
    t_end: float = Field(ge=0)
    type: str
    player: int | None = None
    importance: float = Field(ge=0, le=1)
    what: str = ""
    why: str = ""
    next: list[str] = []
    confidence: Literal["low", "medium", "high"] = "medium"

    @model_validator(mode="after")
    def _check_range(self) -> "Event":
        if self.t_end < self.t_start:
            raise ValueError("t_end must be >= t_start")
        return self


class EventTimeline(BaseModel):
    match_id: str
    title: str = ""
    video_uri: str = ""
    events: list[Event]
