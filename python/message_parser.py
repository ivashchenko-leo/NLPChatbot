import argparse


def build_argparse():
    parser = argparse.ArgumentParser(prog="/exec")
    parser.add_argument("--debug", dest="debug", action="store_true")

    subparsers = parser.add_subparsers(dest="command")

    add_group_parser = subparsers.add_parser("add_group")
    add_group_parser.add_argument("name", nargs="+")

    add_pattern_parser = subparsers.add_parser("add_pattern")
    add_pattern_parser.add_argument("-p", "--pattern", nargs="+", required=True, dest="pattern")
    add_pattern_parser.add_argument("-g", "--group", nargs="+", required=True, dest="group_tag")

    add_response_parser = subparsers.add_parser("add_response")
    add_response_parser.add_argument("-r", "--response", nargs="+", required=True, dest="response")
    add_response_parser.add_argument("-g", "--group", nargs="+", required=True, dest="group_tag")

    return parser
