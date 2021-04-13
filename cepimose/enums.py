from enum import Enum, unique


@unique
class Region(Enum):
    GORISKA = "'Goriška'"
    ZASAVSKA = "'Zasavska'"
    KOROSKA = "'Koroška'"
    GORENJSKA = "'Gorenjska'"
    OSREDNJESLOVENSKA = "'Osrednjeslovenska'"
    POSAVSKA = "'Posavska'"
    PODRAVSKA = "'Podravska'"
    SAVINJSKA = "'Savinjska'"
    JUGOVZHODNASLOVENIJA = "'Jugovzhodna Slovenija'"
    PRIMORSKONOTRANJSKA = "'Primorsko-notranjska'"
    OBALNOKRASKA = "'Obalno-kraška'"
    POMURSKA = "'Pomurska'"
