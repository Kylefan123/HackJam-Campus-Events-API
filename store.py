"""Seed data and the small in-memory event store.

Other workshop lessons can add query or deduplication logic without changing
the CRUD routes in main.py.
"""

from models import Event, EventInput


SEED_EVENTS = [
    {
        "id": 1,
        "title": "HackJam: Build Your First API",
        "date_time": "2026-11-20T16:00:00-05:00",
        "location": "USF Tampa Library, Room 206",
        "source": "SCP Club Calendar",
        "description": "A beginner-friendly FastAPI workshop hosted by the Society of Competitive Programmers.",
    },
    {
        "id": 2,
        "title": "HackJam: Build Your First API",
        "date_time": "2026-11-20T16:00:00-05:00",
        "location": "USF Tampa Library, Room 206",
        "source": "USF BullsConnect",
        "description": "Join SCP for a hands-on workshop about building an API.",
    },
    {
        "id": 3,
        "title": "Bulls Code Night",
        "date_time": "2026-11-24T18:00:00-05:00",
        "location": "USF Tampa Library, Room 206",
        "source": "SCP Club Calendar",
        "description": "Solve beginner and intermediate programming problems together.",
    },
    {
        "id": 4,
        "title": "Bulls Code Night",
        "date_time": "2026-11-24T18:00:00-05:00",
        "location": "USF Tampa Library, Room 206",
        "source": "Student Newsletter",
        "description": "Weekly coding practice with the Society of Competitive Programmers.",
    },
    {
        "id": 5,
        "title": "USF Student Research Showcase",
        "date_time": "2026-12-02T13:00:00-05:00",
        "location": "Marshall Student Center Ballroom",
        "source": "USF Campus Calendar",
        "description": "Explore student research projects from across campus.",
    },
    {
        "id": 6,
        "title": "Bulls Volunteer Day",
        "date_time": "2026-12-05T09:00:00-05:00",
        "location": "Marshall Student Center Plaza",
        "source": "USF BullsConnect",
        "description": "Meet student organizations before heading to local service projects.",
    },
]


class EventStore:
    """Keep events in a dictionary for as long as this Python process runs."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Restore sample data; also keeps automated tests independent."""
        self._events = {item["id"]: Event(**item) for item in SEED_EVENTS}
        self._next_id = max(self._events, default=0) + 1

    def list(self) -> list[Event]:
        return [self._events[event_id] for event_id in sorted(self._events)]

    def get(self, event_id: int) -> Event | None:
        return self._events.get(event_id)

    def create(self, data: EventInput) -> Event:
        event = Event(id=self._next_id, **data.model_dump())
        self._events[event.id] = event
        self._next_id += 1
        return event

    def replace(self, event_id: int, data: EventInput) -> Event | None:
        if event_id not in self._events:
            return None
        event = Event(id=event_id, **data.model_dump())
        self._events[event_id] = event
        return event

    def delete(self, event_id: int) -> Event | None:
        return self._events.pop(event_id, None)


event_store = EventStore()
