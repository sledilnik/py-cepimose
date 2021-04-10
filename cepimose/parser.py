import datetime

from .types import (
    VaccinationByDayRow,
    VaccinationByAgeRow,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationByAgeRange,
)


def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw) / 1000.0)


def _parse_vaccinations_by_day(data) -> "list[VaccinationByDayRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        date = parse_date(element["G0"])
        people_vaccinated = element["X"][0]["M0"]
        people_fully_vaccinated = element["X"][1]["M0"] if len(element["X"]) > 1 else 0

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


def _parse_vaccinations_by_age(data) -> "list[VaccinationByAgeRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        age_group = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0]) / 100.0
        share_second = float(element["X"][1]["C"][0]) / 100.0

        parsed_data.append(
            VaccinationByAgeRow(
                age_group=age_group,
                count_first=count_first,
                count_second=count_second,
                share_first=share_first,
                share_second=share_second,
            )
        )

    return parsed_data


def _parse_vaccines_supplied_and_used(data) -> "list[VaccineSupplyUsage]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:

        date = parse_date(element["C"][0])

        if "Ø" in element:
            supplied = int(element["C"][1]) if len(element["C"]) > 1 else 0
            used = 0
        else:
            used = (
                int(element["C"][1]) if len(element["C"]) > 1 else parsed_data[-1].used
            )
            supplied = (
                int(element["C"][2])
                if len(element["C"]) > 2
                else parsed_data[-1].supplied
            )

        row = VaccineSupplyUsage(
            date=date,
            supplied=supplied,
            used=used,
        )
        parsed_data.append(row)

    return parsed_data


def _parse_vaccinations_by_region(data) -> "list[VaccinationByRegionRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        region = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0]) / 100.0
        share_second = float(element["X"][1]["C"][0]) / 100.0

        parsed_data.append(
            VaccinationByRegionRow(
                region=region,
                count_first=count_first,
                count_second=count_second,
                share_first=share_first,
                share_second=share_second,
            )
        )

    return parsed_data


def _parse_vaccines_supplied_by_manufacturer(
    data,
) -> "list[VaccinationByManufacturerRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]
    manufacturers = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["ValueDicts"][
        "D0"
    ]
    parsed_data = []

    if len(manufacturers) > 3:
        print(manufacturers)
        raise Exception("New manufacturer!")

    def create_obj(date):
        return {"date": date, "moderna": None, "pfizer": None, "az": None}

    def get_manufacturer(num):
        manu_keys = ["pfizer", "moderna", "az"]
        if num > 2 or num == None:
            print(num)
            raise Exception("Missing manufacturer!")
        return manu_keys[num]

    r_list = [None, 1, 2, 6]

    date = None
    manufacturer = None
    value = None

    for element in resp:
        R = element["R"] if "R" in element else None
        C = element["C"]

        if R not in r_list:
            print(R, C, sep="\t")
            raise Exception("Unknown R value!")

        obj = create_obj(None)

        if R == None:
            # all data
            date = parse_date(C[0])
            manufacturer = get_manufacturer((C[1]))
            value = C[2]
            obj = create_obj(date)
            obj[manufacturer] = value

        if R == 1:
            # same date as previous
            manufacturer = get_manufacturer((C[0]))
            value = C[1]
            obj = create_obj(date)
            obj[manufacturer] = value

        if R == 2:
            # same manufacturer as previous
            date = parse_date(C[0])
            value = C[1]
            obj = create_obj(date)
            obj[manufacturer] = value

        if R == 6:
            # same manufacturer and value as previous
            date = parse_date(C[0])
            obj = create_obj(date)
            obj[manufacturer] = value

        parsed_data.append(
            VaccinationByManufacturerRow(
                date=obj["date"],
                pfizer=obj["pfizer"],
                moderna=obj["moderna"],
                az=obj["az"],
            )
        )
    return parsed_data


def _parse_vaccines_supplied_by_manufacturer_cum(
    data,
) -> "list[VaccinationByManufacturerRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        elements = list(filter(lambda x: "M0" in x, element["X"]))

        date = parse_date(element["G0"])
        moderna = None
        pfizer = None
        az = None

        if len(elements) == 1:
            el = elements[0]
            if el.get("I", None) == 1:
                moderna = int(el["M0"])
            elif el.get("I", None) == 2:
                pfizer = int(el["M0"])
            else:
                az = int(el["M0"])

        # ? what if some other combination
        if len(elements) == 2:
            az = elements[0]["M0"]
            moderna = elements[1]["M0"]

        if len(elements) == 3:
            az = round(elements[0]["M0"])
            moderna = round(elements[1]["M0"])
            pfizer = round(elements[2]["M0"])

        parsed_data.append(
            VaccinationByManufacturerRow(
                date=date,
                pfizer=pfizer,
                moderna=moderna,
                az=az,
            )
        )

    return parsed_data


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