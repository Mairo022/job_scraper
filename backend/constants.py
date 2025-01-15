from enum import Enum

MAX_REQUESTS_PER_MIN_BY_IP = 10

LOCALHOST_IP = '127.0.0.1'

CACHE_LIFESPAN = 1800

ADS_LIMIT = 30


class LOCATIONS(Enum):
    ALL = 0
    TALLINN = 1
    TARTU = 2
    PARNU = 3
    HAAPSALU = 4
    JOGEVA = 5
    NARVA = 6
    RAKVERE = 7
    VIIMSI = 8
    VILJANDI = 9
    VORU = 10


LOCATIONS_AVAILABLE = tuple(location.value for location in LOCATIONS)

LOCATIONS_CV = {
    0: "",
    1: 312,
    2: 314,
    3: 303,
    4: 279,
    5: 280,
    6: 297,
    7: 305,
    8: 913,
    9: 318,
    10: 320
}

LOCATIONS_CVK = {
    0: "",
    1: 3,
    2: 4,
    3: 5,
    4: 7,
    5: 377,
    6: 6,
    7: 1191,
    8: 1296,
    9: 21,
    10: 22
}


class CATEGORIES(Enum):
    ALL = 0
    IT = 1


CATEGORIES_AVAILABLE = tuple(category.value for category in CATEGORIES)

CATEGORIES_CV = {
    0: 0,
    1: 'INFORMATION_TECHNOLOGY'
}

CATEGORIES_CVK = {
    0: 0,
    1: 8
}
