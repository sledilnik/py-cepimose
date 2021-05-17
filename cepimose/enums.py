from enum import Enum, unique


@unique
class Region(Enum):
    GORISKA = "Goriška"
    ZASAVSKA = "Zasavska"
    KOROSKA = "Koroška"
    GORENJSKA = "Gorenjska"
    OSREDNJESLOVENSKA = "Osrednjeslovenska"
    POSAVSKA = "Posavska"
    PODRAVSKA = "Podravska"
    SAVINJSKA = "Savinjska"
    JUGOVZHODNASLOVENIJA = "Jugovzhodna Slovenija"
    PRIMORSKONOTRANJSKA = "Primorsko-notranjska"
    OBALNOKRASKA = "Obalno-kraška"
    POMURSKA = "Pomurska"


@unique
class AgeGroup(Enum):
    GROUP_0_17 = "0-17"
    GROUP_18_24 = "18-24"
    GROUP_25_29 = "25-29"
    GROUP_30_34 = "30-34"
    GROUP_35_39 = "35-39"
    GROUP_40_44 = "40-44"
    GROUP_45_49 = "45-49"
    GROUP_50_54 = "50-54"
    GROUP_55_59 = "55-59"
    GROUP_60_64 = "60-64"
    GROUP_65_69 = "65-69"
    GROUP_70_74 = "70-74"
    GROUP_75_79 = "75-79"
    GROUP_80_84 = "80-84"
    GROUP_85_89 = "85-89"
    GROUP_90 = "90+"


@unique
class Manufacturer(Enum):
    AZ = "Astra Zeneca"
    MODERNA = "Moderna"
    PFIZER = "Pfizer-BioNTech"
    JANSSEN = "Janssen"


@unique
class Gender(Enum):
    FEMALE = "Ženske"
    MALE = "Moški"