from dataclasses import dataclass
import datetime


@dataclass
class VaccinationDose:
    date: datetime.datetime
    dose: int


@dataclass
class VaccinationByAgeRange:
    dose1: list[VaccinationDose]
    dose2: list[VaccinationDose]