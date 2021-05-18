from cepimose.enums import Gender
from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class VaccinationByDayRow:
    """Represents on row of vaccinations by day table"""

    date: datetime.datetime
    first_dose: int
    second_dose: int = 0


@dataclass
class VaccinationByAgeRow:
    age_group: str
    count_first: int
    count_second: int
    share_first: float
    share_second: float


@dataclass
class VaccineSupplyUsage:
    date: datetime.datetime
    supplied: int
    used: int


@dataclass
class VaccinationByRegionRow:
    region: str
    count_first: int
    count_second: int
    share_first: float
    share_second: float


@dataclass
class VaccinationByManufacturerRow:
    date: datetime.datetime
    pfizer: Optional[int]
    moderna: Optional[int]
    az: Optional[int]
    janssen: Optional[int]


@dataclass
class VaccinationDose:
    date: datetime.datetime
    dose: int


@dataclass
class VaccinationMunShare:
    name: str
    dose1: int
    share1: float
    dose2: int
    share2: float
    population: int


@dataclass
class VaccinationAgeGroupByRegionOnDayDose:
    region: str
    total_count: int = 0
    group_count: int = 0
    total_share: float = 0.0
    group_share: float = 0.0


@dataclass
class VaccinationAgeGroupByRegionOnDay:
    region: str
    dose1: VaccinationAgeGroupByRegionOnDayDose
    dose2: VaccinationAgeGroupByRegionOnDayDose


@dataclass
class VaccinationsByGender:
    date: datetime.datetime
    female_first: int = 0
    female_second: int = 0
    male_first: int = 0
    male_second: int = 0
