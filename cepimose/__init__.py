import requests
from .data import (
    _source,
    _headers,
    _vaccinations_by_day_req,
    _vaccinations_by_age_req,
    _vaccines_supplied_and_used_req,
    _vaccinations_by_region_req,
    _vaccines_supplied_by_manufacturer_req,
    _vaccines_supplied_by_manufacturer_cum_req,
    _vaccinations_by_age_range_90_dose1_req,
    _vaccinations_by_age_range_90_dose2_req,
    _vaccination_by_age_range_requests,
    _vaccinations_pomurska_by_day_req,
    _vaccinations_by_region_by_day_requests,
    _vaccinations_municipalities_share_req,
    _vaccinations_timestamp_req,
)
from .parser import (
    _parse_vaccinations_by_age,
    _parse_vaccinations_by_day,
    _parse_vaccines_supplied_and_used,
    _parse_vaccinations_by_region,
    _parse_vaccines_supplied_by_manufacturer,
    _parse_vaccines_supplied_by_manufacturer_cum,
    _parse_vaccinations_by_age_range,
    _parse_vaccinations_by_region_by_day,
    _parse_vaccinations_by_municipalities_share,
    _parse_vaccinations_timestamp,
)

from .types import (
    VaccinationByAgeRow,
    VaccinationByDayRow,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationByAgeRange,
)


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


# by age range
def vaccinations_by_age_range_90() -> "VaccinationByAgeRange":
    def vaccinations_by_age_range_90_dose1() -> "list[VaccinationDose]":
        return _get_data(
            _vaccinations_by_age_range_90_dose1_req, _parse_vaccinations_by_age_range
        )

    def vaccinations_by_age_range_90_dose2() -> "list[VaccinationDose]":
        return _get_data(
            _vaccinations_by_age_range_90_dose2_req, _parse_vaccinations_by_age_range
        )

    dose1 = vaccinations_by_age_range_90_dose1()
    dose2 = vaccinations_by_age_range_90_dose2()
    return VaccinationByAgeRange(dose1=dose1, dose2=dose2)


def vaccinations_by_age_range():
    key_value = _vaccination_by_age_range_requests.items()
    obj = {}
    for el in key_value:
        key = el[0]
        dose1_req = el[1][0]
        dose2_req = el[1][1]

        dose1 = _get_data(dose1_req, _parse_vaccinations_by_age_range)
        dose2 = _get_data(dose2_req, _parse_vaccinations_by_age_range)
        obj[key] = VaccinationByAgeRange(dose1=dose1, dose2=dose2)

    return obj


# by individual region
def vaccinations_pomurska_by_day() -> "list[VaccinationByDayRow]":
    return _get_data(
        _vaccinations_pomurska_by_day_req, _parse_vaccinations_by_region_by_day
    )


def vaccinations_by_region_by_day():
    key_value = _vaccinations_by_region_by_day_requests.items()
    obj = {}
    for el in key_value:
        key = el[0]
        doses_req = el[1][0]

        doses = _get_data(doses_req, _parse_vaccinations_by_region_by_day)
        obj[key] = doses

    return obj


# PAGE 2
# municipalities
def vaccinations_by_municipalities_share():
    return _get_data(
        _vaccinations_municipalities_share_req,
        _parse_vaccinations_by_municipalities_share,
    )
