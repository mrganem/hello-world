import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "locations.json"

DEFAULT_DATA = {
    "aliases": {"keys": "Rav4 keys", "my keys": "Rav4 keys"},
    "canonical_homes": {},
    "current_locations": {},
    "history": {},
    "travel_mode": {"active": False, "location": None, "activated_at": None},
}


def load() -> dict:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        data = json.loads(json.dumps(DEFAULT_DATA))
        save(data)
        return data
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)


def record_location(data: dict, item: str, location: str) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    data["current_locations"][item] = {"location": location, "updated_at": now}
    if item not in data["history"]:
        data["history"][item] = []
    data["history"][item].append({
        "location": location,
        "recorded_at": now,
        "travel_mode_active": data["travel_mode"]["active"],
    })


def get_canonical_home(data: dict, item: str) -> str | None:
    return data["canonical_homes"].get(item)


def set_canonical_home(data: dict, item: str, home: str) -> None:
    data["canonical_homes"][item] = home


def get_history(data: dict, item: str, limit: int = 10) -> list:
    entries = data["history"].get(item, [])
    return list(reversed(entries[-limit:]))


def get_all_current(data: dict) -> dict:
    return data["current_locations"]


def get_travel_mode(data: dict) -> dict:
    return data["travel_mode"]


def set_travel_mode(data: dict, active: bool, location: str | None) -> None:
    now = datetime.now().isoformat(timespec="seconds") if active else None
    data["travel_mode"] = {"active": active, "location": location, "activated_at": now}
