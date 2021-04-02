import requests
from .data import _source, _headers, _vaccinations_by_day_req, _vaccinations_by_age_req
import datetime

from .types import VaccinationByDayRow, VaccinationByAgeRow

def _get_data(req, parse_response):
    resp = requests.post(_source, headers=_headers, json=req)
    resp.raise_for_status()
    return parse_response(resp.json())


def _parse_vaccinations_by_day(data) -> 'list[VaccinationByDayRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        date = datetime.datetime.fromtimestamp(float(element["G0"])/1000.0)
        people_vaccinated = element["X"][0]["M0"]
        people_fully_vaccinated = element["X"][1]["M0"] if len(element["X"]) > 1 else 0

        parsed_data.append(VaccinationByDayRow(
            date=date,
            first_dose=people_vaccinated,
            second_dose=people_fully_vaccinated
        ))

    return parsed_data

def _parse_vaccinations_by_age(data) -> 'list[VaccinationByDayRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        age_group = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0])/100.0
        share_second = float(element["X"][1]["C"][0])/100.0

        parsed_data.append(VaccinationByAgeRow(
            age_group=age_group,
            count_first=count_first,
            count_second=count_second,
            share_first=share_first,
            share_second=share_second
        ))

    return parsed_data

def vaccinations_by_day():
    return _get_data(_vaccinations_by_day_req, _parse_vaccinations_by_day)

def vaccinations_by_age():
    return _get_data(_vaccinations_by_age_req, _parse_vaccinations_by_age)