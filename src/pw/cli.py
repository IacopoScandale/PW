from argparse import ArgumentParser, ArgumentTypeError, Namespace

from .__main__ import init_setup, show_infos
from .add_comm import add_comm
from .copy_comm import copy_comm
from .data.strings import (
    DESCRIPTION,
    FILE_CHECK_PW,
    PW_ADD_COMM_NAME,
    PW_ADD_HELP,
    PW_COPY_COMM_NAME,
    PW_COPY_HELP,
    PW_EDIT_COMM_NAME,
    PW_EDIT_HELP,
    PW_INFO_COMM_NAME,
    PW_INFO_HELP,
    PW_LIST_COMM_NAME,
    PW_LIST_HELP,
    PW_REMOVE_COMM_NAME,
    PW_REMOVE_HELP,
)
from .edit_comm import edit_comm
from .info_comm import info_comm
from .list_comm import list_comm
from .remove_comm import remove_comm


def type_positive_int(num: str) -> int:
    try:
        num = int(num)
    except ValueError:
        raise ArgumentTypeError("Value must be a positive integer > 0")
    if not (num > 0):
        raise ArgumentTypeError(f"Value '{num}' must be a positive integer > 0")
    return num


def is_pw_set_up() -> bool:
    """
    If file CHECK_PW exists, then the project is set up, otherwise
    setup is required
    """
    return FILE_CHECK_PW.exists()


def parse_arguments() -> Namespace:
    """
    get pw command arguments
    """
    parser = ArgumentParser(description=DESCRIPTION)
    subparsers = parser.add_subparsers(dest="command")

    # add subcommand
    add_parser = subparsers.add_parser(  # noqa: F841
        PW_ADD_COMM_NAME,
        help=PW_ADD_HELP,
    )

    # info subcommand
    info_parser = subparsers.add_parser(
        PW_INFO_COMM_NAME,
        help=PW_INFO_HELP,
    )
    info_parser.add_argument(
        "site_query",
        help="substring of the site we are looking for e.g. 'hub' for 'github.com'",
    )
    info_parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all site infos (requires main PW password)"
    )

    # copy subcommand
    copy_parser = subparsers.add_parser(
        PW_COPY_COMM_NAME,
        help=PW_COPY_HELP,
    )
    copy_parser.add_argument(
        "site_query",
        help="substring of the site we are looking for e.g. 'hub' for 'github.com'",
    )
    copy_parser.add_argument(
        "-k","--keep",
        type=type_positive_int,
        default=15,
        help=(
            "Time in seconds (default=15) that the password remains in the "
            + "clipboard before it is cleared"
        )
    )

    # list subcommand
    list_parser = subparsers.add_parser(
        PW_LIST_COMM_NAME,
        help=PW_LIST_HELP,
    )
    list_parser.add_argument(
        "site_query",
        nargs="?",
        default="",
        help="substring of the site we are looking for e.g. 'hub' for 'github.com'",
    )
    list_parser.add_argument(
        "--raw",
        action="store_true",
        help="Raw plain text output (useful to pipe with sort)"
    )

    # edit subcommand
    edit_parser = subparsers.add_parser(PW_EDIT_COMM_NAME, help=PW_EDIT_HELP)
    edit_parser.add_argument(
        "site_query",
        help="substring of the site we are looking for e.g. 'hub' for 'github.com'",
    )
    edit_parser.add_argument(
        "-s",
        "--site",
        help="new site name",
        nargs="?",
        default=None,
    )
    edit_parser.add_argument(
        "-e",
        "--email",
        help="new email",
        nargs="?",
        default=None,
    )
    edit_parser.add_argument(
        "-u",
        "--username",
        help="new username",
        nargs="?",
        default=None,
    )
    edit_parser.add_argument(
        "-p",
        "--change-pw",
        help="interactive mode to change site password",
        action="store_true",
    )
    edit_parser.add_argument(
        "-o",
        "--change-other",
        help="interactive mode to change other info",
        action="store_true",
    )

    # remove subcommand
    remove_parser = subparsers.add_parser(
        PW_REMOVE_COMM_NAME,
        help=PW_REMOVE_HELP,
    )
    remove_parser.add_argument(
        "site_query",
        help="substring of the site we are looking for e.g. 'hub' for 'github.com'",
    )

    args = parser.parse_args()
    return args


def main() -> None:
    """
    pw line command
    """
    # start setup if pw is not set up
    # if not is_pw_set_up:
    init_setup()

    args: Namespace = parse_arguments()

    # execute appropriate function based on the command
    if args.command is None:
        show_infos()
    elif args.command == PW_ADD_COMM_NAME:
        add_comm()
    elif args.command == PW_INFO_COMM_NAME:
        info_comm(args.site_query, args.all)
    elif args.command == PW_COPY_COMM_NAME:
        copy_comm(args.site_query, args.keep)
    elif args.command == PW_LIST_COMM_NAME:
        list_comm(args.site_query, args.raw)
    elif args.command == PW_EDIT_COMM_NAME:
        kwargs = {
            "new_site": args.site,
            "new_email": args.email,
            "new_username": args.username,
            "change_pw": args.change_pw,
            "edit_other": args.change_other,
        }
        edit_comm(args.site_query, **kwargs)
    elif args.command == PW_REMOVE_COMM_NAME:
        remove_comm(args.site_query)
