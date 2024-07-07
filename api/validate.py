import re

from babel import Locale, UnknownLocaleError
from flask.wrappers import Request

from .exceptions import ValidationError


def validate_int(req: Request, field: str, default: int = 0) -> int:
    """Validate an integer, returns the integer if valid, otherwise the default."""
    value = req.args.get(field, "")
    try:
        return int(value)
    except ValueError:
        return default


def validate_color(req: Request, field: str, default: str = "#ffffff") -> str:
    """Validate a color, returns the color if it's a valid hex code (3, 4, 6, or 8 characters), otherwise the default."""
    value = req.args.get(field, "")
    hex_digits = re.sub(r"[^a-fA-F0-9]", "", value)
    if len(hex_digits) not in (3, 4, 6, 8):
        return default
    return f"#{hex_digits}"


def validate_string(req: Request, field: str, default: str = "") -> str:
    """Validate a string, returns the string if valid, otherwise the default."""
    return req.args.get(field, default)


def validate_lang(req: Request, field: str, *, default: str = "en") -> str:
    """Validate a string with a locale lang, returns the string if the locale
    is known by Babel, otherwise the default.
    """
    value = req.args.get(field, default)
    try:
        Locale.parse(value)
    except UnknownLocaleError:
        value = default
    return value
