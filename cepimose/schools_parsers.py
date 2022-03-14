from cepimose.types import (
    SchoolCasesTriada,
    SchoolCasesWeek,
    SchoolConfirmedActive,
    SchoolRatioPopulation,
)
from cepimose.enums import SchoolGroups, SchoolTriadaGroups
import datetime


def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw) / 1000.0)


def _validate_response_data(data):
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")


SCHOOL_GROUPS = {
    SchoolGroups.A.value: SchoolGroups.A,
    SchoolGroups.B.value: SchoolGroups.B,
    SchoolGroups.C.value: SchoolGroups.C,
    SchoolGroups.D.value: SchoolGroups.D,
    SchoolGroups.E.value: SchoolGroups.E,
}


def _parse_schools_date_range_timestamps(data):
    _validate_response_data(data)
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM4"][0]["C"]
    return {"raw": resp, "datetime": [parse_date(ts) for ts in resp]}


def _parse_schools_confirmed_and_active_cases(data):
    _validate_response_data(data)

    resp_total = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"][
        0
    ]["C"]
    resp_data = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]

    result = {
        SchoolGroups.TOTAL: SchoolConfirmedActive(
            SchoolGroups.TOTAL,
            cases_last_week=int(resp_total[0]),
            cases_last_week_ratio=float(resp_total[1]),
            cases_school_year=int(resp_total[2]),
            cases_active=int(resp_total[3]),
            cases_school_year_ratio=float(resp_total[4]),
        )
    }

    for item in resp_data:
        item_data = item["C"]
        group = item_data[0]
        result[SCHOOL_GROUPS[group]] = SchoolConfirmedActive(
            SCHOOL_GROUPS[group],
            cases_last_week=int(item_data[1]),
            cases_last_week_ratio=float(item_data[2]),
            cases_school_year=int(item_data[3]),
            cases_active=int(item_data[4]),
            cases_school_year_ratio=float(item_data[5]),
        )

    return result


def _parse_schools_age_group(data):
    _validate_response_data(data)

    resp_total = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"][
        0
    ]["C"]
    resp_data = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]

    result = {
        SchoolGroups.TOTAL: SchoolRatioPopulation(
            SchoolGroups.TOTAL,
            cases=int(resp_total[2]),
            population=int(resp_total[0]),
            ratio=float(resp_total[1]),
        )
    }

    for item in resp_data:
        item_data = item["C"]
        group = item_data[0]
        result[SCHOOL_GROUPS[group]] = SchoolRatioPopulation(
            SCHOOL_GROUPS[group],
            cases=int(item_data[3]),
            population=int(item_data[1]),
            ratio=float(item_data[2]),
        )

    return result


def _parse_schools_age_group_confirmed_weekly(data):
    _validate_response_data(data)

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    result = {}
    for item in resp:
        item_data = item["X"]
        result[item["G0"]] = SchoolCasesWeek(
            week=item["G0"],
            A=int(item_data[0]["M0"]),
            B=int(item_data[1]["M0"]),
            C=int(item_data[2]["M0"]),
            D=int(item_data[3]["M0"]),
        )

    return result


SCHOOL_TRIADA_GROUPS = {
    SchoolTriadaGroups.A.value: SchoolTriadaGroups.A,
    SchoolTriadaGroups.B.value: SchoolTriadaGroups.B,
    SchoolTriadaGroups.C.value: SchoolTriadaGroups.C,
}


def _parse_schools_age_groups_triada(data):
    _validate_response_data(data)

    resp_total = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"][
        0
    ]["C"]
    resp_data = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]

    result = {
        SchoolTriadaGroups.TOTAL: SchoolRatioPopulation(
            SchoolTriadaGroups.TOTAL,
            cases=int(resp_total[2]),
            population=int(resp_total[0]),
            ratio=float(resp_total[1]),
        )
    }

    for item in resp_data:
        item_data = item["C"]
        group = item_data[0]
        result[SCHOOL_TRIADA_GROUPS[group]] = SchoolRatioPopulation(
            SCHOOL_TRIADA_GROUPS[group],
            cases=int(item_data[3]),
            population=int(item_data[1]),
            ratio=float(item_data[2]),
        )

    return result


def _parse_schools_age_group_percent_per_capita_weekly(data):
    _validate_response_data(data)

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    result = {}
    for item in resp:
        item_data = item["X"]
        result[item["G0"]] = SchoolCasesWeek(
            week=item["G0"],
            A=float(item_data[0]["M0"]),
            B=float(item_data[1]["M0"]),
            C=float(item_data[2]["M0"]),
            D=float(item_data[3]["M0"]),
        )

    return result


def _parse_schools_age_groups_percent_triada_weekly(data):
    _validate_response_data(data)

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    result = {}
    for item in resp:
        item_data = item["X"]
        result[item["G0"]] = SchoolCasesTriada(
            week=item["G0"],
            A=float(item_data[0]["M0"]),
            B=float(item_data[1]["M0"]),
            C=float(item_data[2]["M0"]),
        )

    return result


def _parse_schools_age_group_percent_weekly(data):
    _validate_response_data(data)

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    result = {}
    for item in resp:
        item_data = item["X"]
        result[item["G0"]] = SchoolCasesWeek(
            week=item["G0"],
            A=float(item_data[0]["M0"]),
            B=float(item_data[1]["M0"]),
            C=float(item_data[2]["M0"]),
            D=float(item_data[3]["M0"]),
        )

    return result
