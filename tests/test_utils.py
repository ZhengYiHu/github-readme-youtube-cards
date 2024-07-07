import re
from datetime import datetime

from api.utils import (
    estimate_duration_width,
    format_views_value,
    parse_metric_value,
    seconds_to_duration,
    trim_lines,
)

def test_format_views_value():
    views_regex = re.compile(r"^\d+(?:\.\d)?[KMBT]? views$")
    assert format_views_value("1") == "1 view"
    assert views_regex.match(format_views_value("100"))
    assert views_regex.match(format_views_value("1k"))
    assert views_regex.match(format_views_value("1.5k"))
    assert views_regex.match(format_views_value("2M"))
    assert views_regex.match(format_views_value("1.5G"))


def test_format_views_value_i18n():
    views_regex = re.compile(r"^\d+(?:\,\d)?(?:\u00a0(?:k|M|Md|B))? vues$")
    assert format_views_value("1", "fr") == "1 vue"
    assert views_regex.match(format_views_value("100", "fr"))
    assert views_regex.match(format_views_value("1k", "fr"))
    assert views_regex.match(format_views_value("1.5k", "fr"))
    assert views_regex.match(format_views_value("2M", "fr"))
    assert views_regex.match(format_views_value("1.5G", "fr"))


def test_parse_metric_value():
    assert parse_metric_value("1") == 1
    assert parse_metric_value("100") == 100
    assert parse_metric_value("1k") == 1000
    assert parse_metric_value("1.5k") == 1500
    assert parse_metric_value("1.5M") == 1500000
    assert parse_metric_value("1.5G") == 1500000000


def test_trim_lines():
    assert trim_lines("abcdefghijklmnopqrstuvwxyz", 100, 1) == ["abcdefghijklmnopqrstuvwxyz"]
    assert trim_lines("abcdefghijklmnopqrstuvwxyz", 10, 1) == ["abcdefghi…"]
    assert trim_lines("abcdefghij", 10, 1) == ["abcdefghij"]
    assert trim_lines("abcdefghijklmnopqrstuvwxyz", 10, 2) == ["abcdefghij", "klmnopqrs…"]
    assert trim_lines("abcdefghij", 10, 2) == ["abcdefghij"]


def test_seconds_to_duration():
    assert seconds_to_duration(0) == "0:00"
    assert seconds_to_duration(1) == "0:01"
    assert seconds_to_duration(60) == "1:00"
    assert seconds_to_duration(61) == "1:01"
    assert seconds_to_duration(3600) == "1:00:00"
    assert seconds_to_duration(3601) == "1:00:01"
    assert seconds_to_duration(3661) == "1:01:01"


def test_estimate_duration_width():
    assert estimate_duration_width("1:00") == 34
    assert estimate_duration_width("10:00") == 41
    assert estimate_duration_width("1:00:00") == 53
    assert estimate_duration_width("10:00:00") == 60
