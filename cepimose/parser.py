import datetime

from .types import (
    VaccinationByDayRow,
    VaccinationByAgeRow,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationMunShare,
    VaccinationAgeGroupByRegionOnDayDose,
    VaccinationAgeGroupByRegionOnDay,
)


def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw) / 1000.0)


def _parse_vaccinations_timestamp(data):
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        # ? raise exception or return error obj
        return error
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    return resp[0]["M0"]


def _parse_vaccinations_by_day(data) -> "list[VaccinationByDayRow]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    date = None
    people_vaccinated = None
    people_fully_vaccinated = None
    for element in resp:
        C = element["C"]
        if len(C) == 3:
            date = parse_date(C[0])
            people_vaccinated = C[1]
            people_fully_vaccinated = C[2]
        elif len(C) == 2:
            date = parse_date(C[0])
            R = element["R"]
            if R == 2:
                people_fully_vaccinated = C[1]
            else:
                people_vaccinated = C[1]
        elif len(C) == 1:
            date = parse_date(C[0])
        else:
            raise Exception("Unknown item length!")

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


def _parse_vaccinations_by_age(data) -> "list[VaccinationByAgeRow]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        C = element["C"]
        age_group = str(C[0])
        share_second = float(C[1]) / 100.0
        share_first = float(C[2]) / 100.0
        count_first = int(C[3])
        count_second = int(C[4])

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
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        print(element)
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
        C = element["C"]
        region = str(C[0])
        count_first = int(C[3])
        count_second = int(C[4])
        share_first = float(C[1]) / 100.0
        share_second = float(C[2]) / 100.0

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

    if len(manufacturers) > 4:
        print(manufacturers)
        raise Exception("New manufacturer!")

    def get_manufacturer(num):
        manu_keys = ["pfizer", "moderna", "az", "janssen"]
        if num > 3 or num == None:
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

        manu_row = VaccinationByManufacturerRow(
            date=None, pfizer=None, moderna=None, az=None, janssen=None
        )

        if R == None:
            # all data
            date = parse_date(C[0])
            manufacturer = get_manufacturer((C[1]))
            value = int(C[2])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R == 1:
            # same date as previous
            manufacturer = get_manufacturer((C[0]))
            value = int(C[1])
            setattr(parsed_data[-1], manufacturer, value)

        if R == 2:
            # same manufacturer as previous
            date = parse_date(C[0])
            value = int(C[1])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R == 6:
            # same manufacturer and value as previous
            date = parse_date(C[0])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R != 1:
            parsed_data.append(manu_row)
    return parsed_data


def _parse_vaccines_supplied_by_manufacturer_cum(
    data,
) -> "list[VaccinationByManufacturerRow]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        elements = list(filter(lambda x: "M0" in x, element["X"]))

        date = parse_date(element["G0"])
        moderna = None
        pfizer = None
        az = None
        janssen = None

        for el in elements:
            if el.get("I", None) == 1:
                janssen = int(el["M0"])
            elif el.get("I", None) == 2:
                moderna = int(el["M0"])
            elif el.get("I", None) == 3:
                pfizer = int(el["M0"])
            else:
                az = int(el["M0"])

        parsed_data.append(
            VaccinationByManufacturerRow(
                date=date, pfizer=pfizer, moderna=moderna, az=az, janssen=janssen
            )
        )

    return parsed_data


def _parse_vaccinations_by_age_group(data) -> "list[vaccinations_by_age_group]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    date = None
    people_vaccinated = None
    people_fully_vaccinated = None
    for element in resp:
        C = element["C"]
        if len(C) == 3:
            date = parse_date(C[0])
            people_vaccinated = C[1]
            people_fully_vaccinated = C[2]
        elif len(C) == 2:
            date = parse_date(C[0])
            R = element["R"]
            if R == 2:
                people_fully_vaccinated = C[1]
            else:
                people_vaccinated = C[1]
        elif len(C) == 1:
            # R == 6
            date = parse_date(C[0])
        else:
            raise Exception("Unknown item length!")

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


# ? most likely we can refactor _parse_vaccinations_by_day
def _parse_vaccinations_by_region_by_day(data):

    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        # ? raise exception or return error obj
        return error

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    people_vaccinated = None
    people_fully_vaccinated = None
    for element in resp:
        C = element["C"]

        if len(C) == 3:
            date = parse_date(C[0])
            people_vaccinated = C[1]
            people_fully_vaccinated = C[2]
        elif len(C) == 2:
            date = parse_date(C[0])
            R = element["R"]
            if R == 2:
                people_fully_vaccinated = C[1]
            else:
                people_vaccinated = C[1]
        elif len(C) == 1:
            date = parse_date(C[0])
        else:
            raise Exception("Unknown item length!")

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


def _parse_vaccinations_by_municipalities_share(data) -> "list[VaccinationMunShare]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for el in resp:
        C = el["C"]
        R = el.get("R", None)
        if len(C) == 6:
            name, population, share2, share1, dose1, dose2 = el["C"]
            parsed_data.append(
                VaccinationMunShare(
                    name=name,
                    dose1=dose1,
                    share1=float(share1),
                    dose2=dose2,
                    share2=float(share2),
                    population=population,
                )
            )
        elif len(C) == 5:
            if R == 32:
                name, population, share2, share1, dose1 = el["C"]
                dose2 = int(population * float(share2))
                print(dose2)
                parsed_data.append(
                    VaccinationMunShare(
                        name=name,
                        dose1=dose1,
                        share1=float(share1),
                        dose2=dose2,
                        share2=float(share2),
                        population=population,
                    )
                )
            else:
                print(el)
                raise Exception(f"Unknown R: {R}")
        else:
            print(el)
            raise Exception(f"Unknown C length: {len(C)}")

    return parsed_data


def _parse_vaccinations_age_group_by_region_on_day(
    data,
) -> "list[VaccinationAgeGroupByRegionOnDay]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    def parse_resp_data(region, item):
        if len(item) == 4:
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                group_share=float(item[1]),
                total_count=item[2],
                group_count=item[3],
            )
        if len(item) == 3:
            print(3, item)
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                group_share=float(item[1]),
                total_count=item[2],
            )
        if len(item) == 2:
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                total_count=item[1],
            )
        raise Exception("Unknown item length!")

    parsed_data = []
    for el in resp:
        print(el)
        C = el["C"]
        region = C[0]
        first_dose_data = [C[1], C[2], C[5], C[6]]
        second_dose_data = [C[3], C[4], C[7], C[8]]
        first_dose = parse_resp_data(region, first_dose_data)
        second_dose = parse_resp_data(region, second_dose_data)
        parsed_data.append(
            VaccinationAgeGroupByRegionOnDay(
                region=region, dose1=first_dose, dose2=second_dose
            )
        )

    return parsed_data


def _parse_vaccinations_by_manufacturer_supplied_used(
    data,
) -> "list[VaccineSupplyUsage]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    parsed_data = []
    item = None
    for el in resp:
        C = el["C"]
        date = parse_date(C[0])
        if len(C) == 2:
            item = VaccineSupplyUsage(date=date, supplied=int(C[1]), used=0)
            parsed_data.append(item)
        elif len(C) == 3:
            item = VaccineSupplyUsage(date=date, supplied=int(C[2]), used=int(C[1]))
            parsed_data.append(item)
        else:
            raise Exception("Unknown [C] length")

    return parsed_data


def _parse_vaccinations_gender_by_date(data):
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    return resp[0].get("M0", None)