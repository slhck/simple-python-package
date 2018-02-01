import argparse
import textwrap
import logging

from .__version__ import __version__
from ._logger import setup_custom_logger
logger = setup_custom_logger('{{ cookiecutter.app_name }}')

def create_parser():
    parser = argparse.ArgumentParser(
        prog="{{ cookiecutter.cli_script }}",
        description=textwrap.dedent("""\
            {{ cookiecutter.app_name }} v{} -- {{ cookiecutter.app_short_description }}
            """.format(__version__)),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=""
    )

    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help="Force overwrite existing files"
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help="Print debugging output"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Print verbose output"
    )
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help="Do not run, only print what would be done"
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s v{}'.format(__version__),
        help="Print version and exit"
    )
    return parser


def main():
    cli_args = create_parser().parse_args()

    if cli_args.debug:
        logger.setLevel(logging.DEBUG)
    elif cli_args.verbose:
        logger.setLevel(logging.INFO)

    # ENTRY POINT FOR STUFF


if __name__ == '__main__':
    try:
        status = main()
    except:
        logger.criticalr("Fatal error")
        raise
    else:
        raise SystemExit(status)
