from dataclasses import dataclass
import datetime

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