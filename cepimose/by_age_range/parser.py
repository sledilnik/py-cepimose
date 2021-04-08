import datetime

from .types import VaccinationDose


def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw) / 1000.0)


def _parse_vaccinations_by_age_range(data) -> "list[VaccinationDose]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    date = None
    dose = None
    r_list = [None, 1]
    for element in resp:
        date = parse_date(element["G0"])
        R = R = element["X"][0]["R"] if "R" in element["X"][0] else None

        if R not in r_list:
            print(R)
            raise Exception("Unknown R value!")

        if R == None:
            dose = element["X"][0]["M0"]

        parsed_data.append(VaccinationDose(date=date, dose=dose))

    return parsed_data
