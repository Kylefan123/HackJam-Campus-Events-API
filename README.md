# Campus Events API

A beginner-friendly FastAPI starter for the 2026 Society of Competitive Programmers HackJam workshop at USF. Use it to practice HTTP methods, JSON request and response bodies, and API integration through Swagger UI. The listings are fictional workshop examples based on plausible USF campus activities; some intentionally look like the same event listed by different sources.

## macOS setup (including Apple Silicon)

Install Python 3.10 or newer if needed. Open Terminal, navigate to the folder containing `main.py`, and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Windows 10/11 setup (PowerShell)

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/) if needed. Open PowerShell, navigate to the folder containing `main.py`, and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

These commands use the Python inside `.venv` directly, so you do not need to activate it or change PowerShell's script execution policy. If `py` is not recognized, install Python with the Windows Python launcher, then reopen PowerShell.

## Open Swagger UI

On either system, wait for the server to say it is running, then open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser. This is the interactive Swagger UI: it lists every endpoint and lets you send requests without writing another program. Keep Terminal or PowerShell open while using the API. Press `Control-C` to stop the server.

The same `requirements.txt` works on macOS and Windows: it contains only FastAPI and Uvicorn, with no operating-system-specific packages. `requirements-dev.txt` adds HTTPX only for automated tests. The data lives only in Python memory: **restarting the server restores the six sample events and removes any changes you made**. Uvicorn's `--reload` option also restarts the server when you edit a Python file.

## Five-step Swagger demo

In `/docs`, expand an endpoint, click **Try it out**, then **Execute**. Swagger shows both the JSON response and its HTTP status code.

1. **GET `/events/`** — See the six sample listings. Compare IDs 1 and 2: they describe the same HackJam at the same time but have different sources.
2. **POST `/events/`** — Paste the JSON below into the request body. Execute and note the new `id` in the **201** response (normally `7`). Do not include `id` in the request; the API creates it.
3. **GET `/events/{event_id}`** — Enter the ID returned by POST. The **200** response should show your new event.
4. **PUT `/events/{event_id}`** — Enter that same ID and paste the complete JSON body again, changing `title` to `Contest Prep Night`. The **200** response keeps the ID and shows the new title. PUT replaces the full event, so include every field.
5. **DELETE `/events/{event_id}`** — Delete that ID and see the removed event in the **200** response. Then run **GET `/events/{event_id}`** once more with the same ID to confirm **404** (`Event not found`).

JSON for steps 2 and 4:

```json
{
  "title": "Intro to Competitive Programming",
  "date_time": "2026-12-08T17:30:00-05:00",
  "location": "USF Tampa Library, Room 206",
  "source": "SCP Club Calendar",
  "description": "Learn how to approach programming contest problems."
}
```

`date_time` uses ISO 8601. The `-05:00` offset is Eastern Standard Time in December. FastAPI validates the JSON; missing fields or an invalid date/time produce **422**.

## Endpoints

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| GET | `/events/` | List all events | 200 |
| GET | `/events/{event_id}` | Read one event | 200 |
| POST | `/events/` | Create an event | 201 |
| PUT | `/events/{event_id}` | Replace an event | 200 |
| DELETE | `/events/{event_id}` | Delete an event | 200 |

Unknown IDs return **404**. Invalid IDs or JSON bodies return **422**. The response for an event includes `id`, `title`, `date_time`, `location`, `source`, and `description`.

## Project layout and next lesson

- `main.py` defines the FastAPI app and its five routes.
- `models.py` defines the Pydantic request and response models.
- `store.py` owns the sample listings and in-memory CRUD operations.
- `tests/test_api.py` checks the routes, status codes, validation, and Swagger schema.

The sample sources and duplicate-looking listings are ready for a later lesson on filtering recent events from multiple sources and removing duplicates. That lesson can add routes and helper functions while reusing the existing models and store. Asset-handling endpoints can be added separately. This starter does not yet filter, deduplicate, handle assets, call external APIs, or persist data.

To run the tests on macOS, open a second Terminal window in this folder, activate `.venv`, then install the test dependency and use Python's built-in test runner:

```bash
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

On Windows, open a second PowerShell window in this folder and run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
