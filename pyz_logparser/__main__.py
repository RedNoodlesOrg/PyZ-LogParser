"""__main__.py"""
import argparse
import sys
from pyz_logparser import file_parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format Project Zomboid Logs")
    parser.add_argument('format', type=str, choices=list(
                        file_parser.FACTORY.keys()),
                        help='Name of logfile')
    args = parser.parse_args()
    for line in sys.stdin:
        sys.stdout.write(f"{file_parser.parse_log_line(args.format, line)}\n")
