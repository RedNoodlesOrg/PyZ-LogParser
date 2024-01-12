"""file_parser.py"""

from pyz_logparser.models.log import FACTORY, LogVar


def parse_log_line(logtype: str, logline: str) -> LogVar | None:
    """Parse Log Line"""
    log_class = FACTORY.get(logtype)
    if log_class:
        pattern = log_class.PARSER
        pattern_match = pattern.match(logline)
        if pattern_match:
            return log_class.from_dict(log_class, pattern_match.groupdict())
    return None
