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
class VaccinationByAgeGroup:
    dose1: "list[VaccinationDose]"
    dose2: "list[VaccinationDose]"

    def getBothDoses(self):
        date = None
        first_dose = None
        second_dose = None
        result = []
        for dose in self.dose1:
            date = dose.date
            first_dose = dose.dose
            second_doses = [dose for dose in self.dose2 if dose.date == date]
            second_dose = second_doses[0].dose if len(second_doses) > 0 else None
            result.append(
                VaccinationByDayRow(
                    date=date, first_dose=first_dose, second_dose=second_dose
                )
            )
        return result


@dataclass
class VaccinationMunShare:
    name: str
    dose1: int
    share1: float
    dose2: int
    share2: float
    population: int