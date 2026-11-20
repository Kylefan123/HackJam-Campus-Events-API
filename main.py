"""Campus Events API: run with `python -m uvicorn main:app --reload`."""

from fastapi import FastAPI, HTTPException, status

from models import Event, EventInput
from store import event_store


app = FastAPI(
    title="Campus Events API",
    description=(
        "A small, in-memory USF events API for the 2026 SCP HackJam workshop. "
        "Sample listings include duplicates from different sources for a later lesson. "
        "Restarting the server restores the sample events and removes your changes."
    ),
    version="1.0.0",
)


def find_event_or_404(event_id: int) -> Event:
    event = event_store.get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.get("/events/", response_model=list[Event], tags=["Events"], summary="List all events")
def list_events() -> list[Event]:
    """Return every listing, including duplicate-looking listings from other sources."""
    return event_store.list()


@app.get(
    "/events/{event_id}",
    response_model=Event,
    responses={404: {"description": "Event not found"}},
    tags=["Events"],
    summary="Get one event by ID",
)
def get_event(event_id: int) -> Event:
    """Look up the ID shown in the list or returned by POST."""
    return find_event_or_404(event_id)


@app.post(
    "/events/",
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
    tags=["Events"],
    summary="Create an event",
)
def create_event(data: EventInput) -> Event:
    """Send event details as JSON; the server assigns a unique ID."""
    return event_store.create(data)


@app.put(
    "/events/{event_id}",
    response_model=Event,
    responses={404: {"description": "Event not found"}},
    tags=["Events"],
    summary="Replace an event",
)
def replace_event(event_id: int, data: EventInput) -> Event:
    """Send all event fields as JSON to replace the listing with this ID."""
    find_event_or_404(event_id)
    return event_store.replace(event_id, data)


@app.delete(
    "/events/{event_id}",
    response_model=Event,
    responses={404: {"description": "Event not found"}},
    tags=["Events"],
    summary="Delete an event",
)
def delete_event(event_id: int) -> Event:
    """Remove the listing and return the event that was deleted."""
    find_event_or_404(event_id)
    return event_store.delete(event_id)
