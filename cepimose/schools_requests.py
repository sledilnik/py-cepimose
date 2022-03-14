from .schools_commands import (
    _schools_age_group_command,
    _schools_age_group_confirmed_weekly_command,
    _schools_age_group_percent_per_capita_weekly_command,
    _schools_confirmed_and_active_cases_command,
    _schools_age_groups_triada_command,
    _schools_date_range_timestamps_command,
    _schools_age_groups_percent_triada_weekly_command,
    _schools_age_group_percent_weekly_command,
    _schools_timestamp_command,
)

from .data import _create_req

_schools_timestamp_req = _create_req("schools", [_schools_timestamp_command], True)

_schools_date_range_timestamps_req = _create_req(
    "schools", [_schools_date_range_timestamps_command], True
)

_schools_confirmed_and_active_cases_req = _create_req(
    "schools", [_schools_confirmed_and_active_cases_command], True
)

_schools_age_group_req = _create_req("schools", [_schools_age_group_command], True)

_schools_age_groups_triada_req = _create_req(
    "schools", [_schools_age_groups_triada_command], True
)

_schools_age_group_confirmed_weekly_req = _create_req(
    "schools", [_schools_age_group_confirmed_weekly_command], True
)

_schools_age_group_percent_per_capita_weekly_req = _create_req(
    "schools", [_schools_age_group_percent_per_capita_weekly_command], True
)

_schools_age_groups_percent_triada_weekly_req = _create_req(
    "schools", [_schools_age_groups_percent_triada_weekly_command], True
)

_schools_age_group_percent_weekly_req = _create_req(
    "schools", [_schools_age_group_percent_weekly_command], True
)
