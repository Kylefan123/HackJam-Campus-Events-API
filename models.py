"""JSON shapes shared by the Campus Events API endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class EventInput(BaseModel):
    """Fields a client sends when creating or replacing an event."""

    title: str = Field(min_length=1, description="Name of the campus event")
    date_time: datetime = Field(description="Event start time in ISO 8601 format")
    location: str = Field(min_length=1, description="Where the event takes place")
    source: str = Field(min_length=1, description="Where this listing came from")
    description: str = Field(min_length=1, description="Short event description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Bulls Code Night",
                "date_time": "2026-11-20T18:00:00-05:00",
                "location": "USF Tampa Library, Room 206",
                "source": "SCP Club Calendar",
                "description": "Practice coding challenges with other USF students.",
            }
        }
    }


class Event(EventInput):
    """An event returned by the API, including its server-assigned ID."""

    id: int = Field(description="Unique ID assigned by this API")
