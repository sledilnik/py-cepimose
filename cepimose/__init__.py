import requests
from .data import _source, _headers, _vaccinations_by_day_req, _vaccinations_by_age_req, _vaccines_supplied_and_used_req, _vaccinations_by_region_req, _vaccines_supplied_by_manufacturer_req, _vaccines_supplied_by_manufacturer_cum_req
from .parser import _parse_vaccinations_by_age, _parse_vaccinations_by_day, _parse_vaccines_supplued_and_used, _parse_vaccinations_by_region, _parse_vaccines_supplied_by_manufacturer, _parse_vaccines_supplied_by_manufacturer_cum

from .types import VaccinationByAgeRow, VaccinationByDayRow, VaccineSupplyUsage, VaccinationByRegionRow, VaccinationByManufacturerRow


def _get_data(req, parse_response):
    resp = requests.post(_source, headers=_headers, json=req)
    resp.raise_for_status()
    return parse_response(resp.json())


def vaccinations_by_day() -> 'list[VaccinationByDayRow]':
    return _get_data(_vaccinations_by_day_req, _parse_vaccinations_by_day)


def vaccinations_by_age() -> 'list[VaccinationByAgeRow]':
    return _get_data(_vaccinations_by_age_req, _parse_vaccinations_by_age)


def vaccines_supplied_and_used() -> 'list[VaccineSupplyUsage]':
    return _get_data(_vaccines_supplied_and_used_req, _parse_vaccines_supplued_and_used)


def vaccinations_by_region() -> 'list[VaccinationByRegionRow]':
    return _get_data(_vaccinations_by_region_req, _parse_vaccinations_by_region)


def vaccines_supplied_by_manufacturer() -> 'list[VaccinationByManufacturerRow]':
    return _get_data(_vaccines_supplied_by_manufacturer_req, _parse_vaccines_supplied_by_manufacturer)


def vaccines_supplied_by_manufacturer_cumulative() -> 'list[VaccinationByManufacturerRow]':
    return _get_data(_vaccines_supplied_by_manufacturer_cum_req, _parse_vaccines_supplied_by_manufacturer_cum)
