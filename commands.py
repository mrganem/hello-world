from resolver import apply_travel_prefix, is_at_home, resolve_alias
from store import (
    get_all_current,
    get_canonical_home,
    get_history,
    get_travel_mode,
    record_location,
    set_canonical_home,
    set_travel_mode,
)


def cmd_set(args, data):
    item = resolve_alias(data, args.item)
    location = args.location.strip().title()

    tm = get_travel_mode(data)
    if tm["active"]:
        location = apply_travel_prefix(data, location)

    record_location(data, item, location)

    home = get_canonical_home(data, item)
    if home is None:
        answer = ""
        while not answer.strip():
            try:
                answer = input(f"Where does {item} belong? ").strip()
            except EOFError:
                break
        if answer.strip():
            home = answer.strip().title()
            set_canonical_home(data, item, home)
            print(f"{item} home set → {home} ✓")

    if not tm["active"] and not is_at_home(item, location, data):
        print(f"{item} → {location} ✓")
        try:
            answer = input(f"⚠  Away from {home}. Return it? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer in ("y", "yes"):
            record_location(data, item, home)
            print(f"{item} → {home} ✓")
        return

    print(f"{item} → {location} ✓")


def cmd_home(args, data):
    if not args.item:
        homes = data["canonical_homes"]
        if not homes:
            print("No canonical homes set.")
            return
        width = max(len(k) for k in homes)
        for item, home in sorted(homes.items()):
            print(f"  {item.ljust(width)}  {home}")
        return

    item = resolve_alias(data, args.item)
    if args.location:
        home = args.location.strip().title()
        set_canonical_home(data, item, home)
        print(f"{item} home → {home} ✓")
    else:
        home = get_canonical_home(data, item)
        if home:
            print(f"{item}: {home}")
        else:
            print(f"{item}: no home set")


def cmd_where(args, data):
    item = resolve_alias(data, args.item)
    current = data["current_locations"].get(item)
    if not current:
        print(f"{item}: location unknown")
        return
    loc = current["location"]
    ts = current["updated_at"]
    tag = "  [home]" if is_at_home(item, loc, data) else ""
    print(f"{item}: {loc}  (as of {ts}){tag}")


def cmd_list(args, data):
    tm = get_travel_mode(data)
    if tm["active"]:
        print(f"[Travel Mode: {tm['location']}]")

    current = get_all_current(data)
    if not current:
        print("No items tracked yet.")
        return

    width = max(len(k) for k in current)
    for item in sorted(current):
        loc = current[item]["location"]
        home = get_canonical_home(data, item)
        if not home:
            tag = ""
        elif is_at_home(item, loc, data):
            tag = "  [home]"
        else:
            tag = f"  ⚠ away from {home}"
        print(f"  {item.ljust(width)}  {loc}{tag}")


def cmd_history(args, data):
    item = resolve_alias(data, args.item)
    limit = args.limit if hasattr(args, "limit") and args.limit else 10
    entries = get_history(data, item, limit)
    if not entries:
        print(f"{item}: no history")
        return
    print(f"{item} (last {len(entries)}):")
    for e in entries:
        ts = e["recorded_at"]
        loc = e["location"]
        tag = "  [travel]" if e.get("travel_mode_active") else ""
        print(f"  {ts}  {loc}{tag}")


def cmd_travel(args, data):
    sub = args.travel_cmd
    if sub == "on":
        place = args.place.strip().title()
        set_travel_mode(data, True, place)
        print(f"Travel mode ON: {place} ✓")
    elif sub == "off":
        set_travel_mode(data, False, None)
        print("Travel mode OFF ✓")
    elif sub == "status":
        tm = get_travel_mode(data)
        if tm["active"]:
            print(f"Travel mode: ON ({tm['location']}, since {tm['activated_at']})")
        else:
            print("Travel mode: OFF")
