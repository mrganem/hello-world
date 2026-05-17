import re


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()


def resolve_alias(data: dict, raw: str) -> str:
    key = normalize(raw)
    aliases = {normalize(k): v for k, v in data["aliases"].items()}
    if key in aliases:
        return aliases[key]
    return raw.strip().title()


def apply_travel_prefix(data: dict, location: str) -> str:
    tm = data["travel_mode"]
    if not tm["active"] or not tm["location"]:
        return location
    prefix = tm["location"] + " / "
    if location.lower().startswith(prefix.lower()):
        return location
    return prefix + location


def is_at_home(item: str, location: str, data: dict) -> bool:
    home = data["canonical_homes"].get(item)
    if home is None:
        return False
    return normalize(home) == normalize(location)
