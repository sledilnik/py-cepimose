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
    _vaccination_by_age_group_requests,
    _vaccinations_by_region_by_day_requests,
    _vaccinations_municipalities_share_req,
    _vaccinations_timestamp_req,
    _vaccinations_age_group_by_region_on_day_requests,
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
)

from .types import (
    VaccinationByAgeRow,
    VaccinationByDayRow,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationAgeGroupByRegionOnDayDose,
    VaccinationAgeGroupByRegionOnDay,
)

from .enums import Region, AgeGroup


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
    def getBothDoses(dose1, dose2):
        date = None
        first_dose = None
        second_dose = None
        result = []
        for dose in dose1:
            date = dose.date
            first_dose = dose.dose
            second_doses = [dose for dose in dose2 if dose.date == date]
            second_dose = second_doses[0].dose if len(second_doses) > 0 else None
            result.append(
                VaccinationByDayRow(
                    date=date, first_dose=first_dose, second_dose=second_dose
                )
            )
        return result

    obj = {}
    if group == None:

        key_value = _vaccination_by_age_group_requests.items()
        for key, req_list in key_value:
            dose1_req = req_list[0]
            dose2_req = req_list[1]
            dose1 = _get_data(dose1_req, _parse_vaccinations_by_age_group)
            dose2 = _get_data(dose2_req, _parse_vaccinations_by_age_group)
            both_doses = getBothDoses(dose1, dose2)
            obj[key] = both_doses
        return obj

    dose1_req = _vaccination_by_age_group_requests[group][0]
    dose2_req = _vaccination_by_age_group_requests[group][1]
    dose1 = _get_data(dose1_req, _parse_vaccinations_by_age_group)
    dose2 = _get_data(dose2_req, _parse_vaccinations_by_age_group)
    both_doses = getBothDoses(dose1, dose2)
    return both_doses


# by region by day
def vaccinations_by_region_by_day(
    region: Region = None,
) -> "dic[Region, list[VaccinationByDayRow]]":
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
