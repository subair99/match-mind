from .models import Event, EventTimeline


def find_moments(tl: EventTimeline, after: float = 0.0, limit: int = 3) -> list[Event]:
    """Most important events after a playback position (\"What did I miss?\")."""
    later = [e for e in tl.events if e.t_start >= after]
    return sorted(later, key=lambda e: e.importance, reverse=True)[:limit]


def player_timeline(tl: EventTimeline, player: int) -> list[Event]:
    """All events for one shirt number, in time order."""
    return sorted((e for e in tl.events if e.player == player), key=lambda e: e.t_start)
