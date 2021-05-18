import datetime
import requests
import time
from .data import (
    _source,
    _headers,
    _vaccinations_by_day_req,
    _vaccinations_by_age_req,
    _vaccines_supplied_and_used_req,
    _vaccinations_by_region_req,
    _vaccines_supplied_by_manufacturer_req,
    _vaccines_supplied_by_manufacturer_cum_req,
    _vaccination_by_age_group_requests,
    _vaccinations_by_region_by_day_requests,
    _vaccinations_municipalities_share_req,
    _vaccinations_timestamp_req,
    _vaccinations_age_group_by_region_on_day_requests,
    _vaccination_by_manufacturer_supplied_used_requests,
    _vaccinations_gender_by_date_requests,
)
from .parser import (
    _parse_vaccinations_by_age,
    _parse_vaccinations_by_day,
    _parse_vaccines_supplied_and_used,
    _parse_vaccinations_by_region,
    _parse_vaccines_supplied_by_manufacturer,
    _parse_vaccines_supplied_by_manufacturer_cum,
    _parse_vaccinations_by_age_group,
    _parse_vaccinations_by_region_by_day,
    _parse_vaccinations_by_municipalities_share,
    _parse_vaccinations_timestamp,
    _parse_vaccinations_age_group_by_region_on_day,
    _parse_vaccinations_by_manufacturer_supplied_used,
    _parse_vaccinations_gender_by_date,
)

from .types import (
    VaccinationByAgeRow,
    VaccinationByDayRow,
    VaccinationsByGender,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationAgeGroupByRegionOnDayDose,
    VaccinationAgeGroupByRegionOnDay,
)

from .enums import Manufacturer, Region, AgeGroup, Gender


def _get_data(req, parse_response):
    resp = requests.post(_source, headers=_headers, json=req)
    resp.raise_for_status()
    return parse_response(resp.json())


def vaccinations_timestamp():
    return _get_data(_vaccinations_timestamp_req, _parse_vaccinations_timestamp)


def vaccinations_by_day() -> "list[VaccinationByDayRow]":
    return _get_data(_vaccinations_by_day_req, _parse_vaccinations_by_day)


def vaccinations_by_age() -> "list[VaccinationByAgeRow]":
    return _get_data(_vaccinations_by_age_req, _parse_vaccinations_by_age)


def vaccines_supplied_and_used() -> "list[VaccineSupplyUsage]":
    return _get_data(_vaccines_supplied_and_used_req, _parse_vaccines_supplied_and_used)


def vaccinations_by_region() -> "list[VaccinationByRegionRow]":
    return _get_data(_vaccinations_by_region_req, _parse_vaccinations_by_region)


def vaccines_supplied_by_manufacturer() -> "list[VaccinationByManufacturerRow]":
    return _get_data(
        _vaccines_supplied_by_manufacturer_req, _parse_vaccines_supplied_by_manufacturer
    )


def vaccines_supplied_by_manufacturer_cumulative() -> "list[VaccinationByManufacturerRow]":
    return _get_data(
        _vaccines_supplied_by_manufacturer_cum_req,
        _parse_vaccines_supplied_by_manufacturer_cum,
    )


# by age group
def vaccinations_by_age_group(
    group: AgeGroup = None,
) -> "dict[AgeGroup,list[VaccinationByDayRow]] or list[VaccinationByDayRow]":

    obj = {}
    if group == None:

        key_value = _vaccination_by_age_group_requests.items()
        for key, req_list in key_value:
            req = req_list[0]

            obj[key] = _get_data(req, _parse_vaccinations_by_age_group)
        return obj

    req = _vaccination_by_age_group_requests[group][0]
    return _get_data(req, _parse_vaccinations_by_age_group)


# by region by day
def vaccinations_by_region_by_day(
    region: Region = None,
) -> "dict[Region, list[VaccinationByDayRow]]":
    obj = {}
    if region == None:
        key_value = _vaccinations_by_region_by_day_requests.items()
        for key, req_list in key_value:
            req = req_list[0]
            doses = _get_data(req, _parse_vaccinations_by_region_by_day)
            obj[key] = doses
        return obj

    req = _vaccinations_by_region_by_day_requests[region][0]
    doses = _get_data(req, _parse_vaccinations_by_region_by_day)
    obj[region] = doses

    return obj


def vaccinations_age_group_by_region_on_day(
    group: Region = None,
) -> "dict[AgeGroup, list[VaccinationAgeGroupByRegionOnDay]] or list[VaccinationAgeGroupByRegionOnDay]":
    obj = {}

    if group == None:
        key_value = _vaccinations_age_group_by_region_on_day_requests.items()
        for key, req_list in key_value:
            req = req_list[0]
            doses = _get_data(req, _parse_vaccinations_age_group_by_region_on_day)
            obj[key] = doses
        return obj

    req = _vaccinations_age_group_by_region_on_day_requests[group][0]
    doses = _get_data(req, _parse_vaccinations_age_group_by_region_on_day)
    return doses


# PAGE 2
# municipalities
def vaccinations_by_municipalities_share():
    return _get_data(
        _vaccinations_municipalities_share_req,
        _parse_vaccinations_by_municipalities_share,
    )


# PAGE 3
# manufacturers
def vaccinations_by_manufacturer_supplied_used(
    group: Manufacturer = None,
) -> "dict[Manufacturer, list[VaccineSupplyUsage]] or list[VaccineSupplyUsage]":
    obj = {}

    if group == None:
        key_value = _vaccination_by_manufacturer_supplied_used_requests.items()
        for key, req_list in key_value:
            req = req_list[0]
            doses = _get_data(req, _parse_vaccinations_by_manufacturer_supplied_used)
            obj[key] = doses
        return obj

    req = _vaccination_by_manufacturer_supplied_used_requests[group][0]
    doses = _get_data(req, _parse_vaccinations_by_manufacturer_supplied_used)
    return doses


# PAGE 1
# gender
def vaccinations_gender_by_date(date: datetime.datetime = None):

    start = time.perf_counter()

    if date == None:
        result = []
        for day in _vaccinations_gender_by_date_requests:
            date = day["date"]
            female = day[Gender.FEMALE]
            male = day[Gender.MALE]
            female_first = _get_data(female[0], _parse_vaccinations_gender_by_date)
            female_second = _get_data(female[1], _parse_vaccinations_gender_by_date)
            male_first = _get_data(male[0], _parse_vaccinations_gender_by_date)
            male_second = _get_data(male[1], _parse_vaccinations_gender_by_date)
            result.append(
                VaccinationsByGender(
                    date=date,
                    female_first=female_first,
                    female_second=female_second,
                    male_first=male_first,
                    male_second=male_second,
                )
            )
        finish = time.perf_counter()
        print(f"Elapsed time: {finish - start}")
        return result

    filtered_days = list(
        filter(lambda item: item["date"] == date, _vaccinations_gender_by_date_requests)
    )

    if len(filtered_days) == 0:
        return None

    day = filtered_days[0]

    date = day["date"]
    female = day[Gender.FEMALE]
    male = day[Gender.MALE]
    female_first = _get_data(female[0], _parse_vaccinations_gender_by_date)
    female_second = _get_data(female[1], _parse_vaccinations_gender_by_date)
    male_first = _get_data(male[0], _parse_vaccinations_gender_by_date)
    male_second = _get_data(male[1], _parse_vaccinations_gender_by_date)
    finish = time.perf_counter()
    print(f"Elapsed time: {finish - start}")
    return VaccinationsByGender(
        date=date,
        female_first=female_first,
        female_second=female_second,
        male_first=male_first,
        male_second=male_second,
    )
