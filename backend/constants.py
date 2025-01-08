# Locations
# 0 - All
# 1 - Tallinn
# 2 - Tartu
# 3 - Pärnu
# 4 - Haapsalu
# 5 - Jõgeva
# 6 - Narva
# 7 - Rakvere
# 8 - Viimsi
# 9 - Viljandi
# 10 - Võru
from enum import Enum

MAX_REQUESTS_PER_MIN_BY_IP = 10

LOCALHOST_IP = '127.0.0.1'

CACHE_LIFESPAN = 1800

ADS_LIMIT = 30


class LOCATIONS(Enum):
    ALL = 0
    TALLINN = 1
    TARTU = 2
    PÄRNU = 3
    HAAPSALU = 4
    JÕGEVA = 5
    NARVA = 6
    RAKVERE = 7
    VIIMSI = 8
    VILJANDI = 9
    VÕRU = 10


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

# Categories
# 0 - All
# 1 - Information technology

CATEGORIES_AVAILABLE = (0, 1)

CATEGORIES_CV = {
    0: 0,
    1: 'INFORMATION_TECHNOLOGY'
}

CATEGORIES_CVK = {
    0: 0,
    1: 8
}
