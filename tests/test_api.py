"""Run with `python -m unittest discover -s tests -v`."""

import unittest

from fastapi.testclient import TestClient

from main import app
from store import event_store


NEW_EVENT = {
    "title": "Intro to Competitive Programming",
    "date_time": "2026-12-08T17:30:00-05:00",
    "location": "USF Tampa Library, Room 206",
    "source": "SCP Club Calendar",
    "description": "Learn how to approach programming contest problems.",
}


class CampusEventsAPITests(unittest.TestCase):
    def setUp(self) -> None:
        event_store.reset()
        self.client = TestClient(app)

    def test_seed_events_include_cross_source_duplicates(self) -> None:
        response = self.client.get("/events/")
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertEqual(len(events), 6)
        self.assertEqual([event["id"] for event in events], [1, 2, 3, 4, 5, 6])
        self.assertEqual(events[0]["title"], events[1]["title"])
        self.assertNotEqual(events[0]["source"], events[1]["source"])

    def test_get_event_and_missing_event(self) -> None:
        self.assertEqual(self.client.get("/events/1").json()["id"], 1)
        response = self.client.get("/events/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Event not found"})

    def test_create_replace_delete_lifecycle(self) -> None:
        created = self.client.post("/events/", json=NEW_EVENT)
        self.assertEqual(created.status_code, 201)
        event_id = created.json()["id"]
        self.assertEqual(event_id, 7)
        self.assertEqual(self.client.get(f"/events/{event_id}").json()["title"], NEW_EVENT["title"])

        updated_data = {**NEW_EVENT, "title": "Contest Prep Night"}
        updated = self.client.put(f"/events/{event_id}", json=updated_data)
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["title"], "Contest Prep Night")
        self.assertEqual(updated.json()["id"], event_id)

        deleted = self.client.delete(f"/events/{event_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.json()["id"], event_id)
        self.assertEqual(self.client.get(f"/events/{event_id}").status_code, 404)

    def test_missing_put_and_delete_return_404(self) -> None:
        self.assertEqual(self.client.put("/events/999", json=NEW_EVENT).status_code, 404)
        self.assertEqual(self.client.delete("/events/999").status_code, 404)

    def test_invalid_json_body_returns_422(self) -> None:
        response = self.client.post("/events/", json={**NEW_EVENT, "date_time": "not-a-date"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(len(self.client.get("/events/").json()), 6)

    def test_swagger_schema_lists_all_methods(self) -> None:
        schema = self.client.get("/openapi.json").json()
        self.assertEqual(schema["info"]["title"], "Campus Events API")
        self.assertEqual(set(schema["paths"]["/events/"]), {"get", "post"})
        self.assertEqual(set(schema["paths"]["/events/{event_id}"]), {"get", "put", "delete"})


if __name__ == "__main__":
    unittest.main()
