#!/usr/bin/env python3
import argparse
import sys

import store
from commands import cmd_history, cmd_home, cmd_list, cmd_set, cmd_travel, cmd_where


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="Track where Mark keeps his belongings.",
    )
    sub = parser.add_subparsers(dest="command")

    # set
    p_set = sub.add_parser("set", help="Log item at a location")
    p_set.add_argument("item")
    p_set.add_argument("location")

    # home
    p_home = sub.add_parser("home", help="Set or view canonical home")
    p_home.add_argument("item", nargs="?", default=None)
    p_home.add_argument("location", nargs="?", default=None)

    # where
    p_where = sub.add_parser("where", help="Show current location of an item")
    p_where.add_argument("item")

    # list
    sub.add_parser("list", help="List all tracked items")

    # history
    p_hist = sub.add_parser("history", help="Show location history for an item")
    p_hist.add_argument("item")
    p_hist.add_argument("--limit", type=int, default=10)

    # travel
    p_travel = sub.add_parser("travel", help="Manage travel mode")
    travel_sub = p_travel.add_subparsers(dest="travel_cmd")
    p_on = travel_sub.add_parser("on")
    p_on.add_argument("place")
    travel_sub.add_parser("off")
    travel_sub.add_parser("status")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    data = store.load()

    dispatch = {
        "set": cmd_set,
        "home": cmd_home,
        "where": cmd_where,
        "list": cmd_list,
        "history": cmd_history,
        "travel": cmd_travel,
    }

    dispatch[args.command](args, data)
    store.save(data)


if __name__ == "__main__":
    main()
