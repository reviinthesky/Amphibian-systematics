import pytest
from src.identifier import Identifier
MATCH_100PERCENT = {
    "common_name": "Сибирская лягушка",
    "latin_name": "Rana amurensis",
    "body_parts": [
        {
            "part": "Голова",
            "pattern": ["spots"],
            "pattern_size": ["мелкие"],
            "color": ["коричневый", "оливковый"],
            "ridge": "отсутствует",
            "fringe": "отсутствует",
            "size": ["небольшая"]
        },
        {
            "part": "Спина",
            "pattern": ["spots", "stripes"],
            "pattern_size": ["средние", "узкие"],
            "color": ["бурый", "оливковый", "серый"],
            "ridge": "слабовыраженный",
            "fringe": "отсутствует"
        },
        {
            "part": "Брюхо",
            "pattern": ["solid"],
            "pattern_size": None,
            "color": ["белый", "светлый", "розовый"],
            "ridge": "отсутствует",
            "fringe": "отсутствует",
        },
        {
            "part": "Лапы",
            "pattern": ["spots"],
            "pattern_size": ["мелкие"],
            "color": ["серый", "коричневый"],
            "ridge": "отсутствует",
            "fringe": "отсутствует",
        },
        {
            "part": "Пальцы",
            "pattern": None,
            "pattern_size": None,
            "color": ["светлый", "серый"],
            "ridge": "отсутствует",
            "fringe": "отсутствует",
        },
        {
            "part": "Хвост",
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
        }
    ],
    "size_cm": [5, 8],
    "key_traits": {
        "has_gills": 0,
        "teeth_type": "мелкие",
        "has_claws": 0,
        "front_toe_count": 4,
        "back_toe_count": 5,
        "toe_tips_type": "округлые",

        "has_grooves": 0,
        "has_tympanum": 1,
        "has_tubercles": 1,
        "tarsal_fold": "слабовыраженная",
        "has_dark_inguinal_loop": 0,
        "has_dark_spot_under_eye": 0,
        "has_longitudinal_ridges": 0
    }
}


def test_full_match():
    user_input = MATCH_100PERCENT
    app = Identifier()
    top_3, result, percentage = app.find_matches(user_input)
    assert top_3 is not None
    assert result is not None
    assert percentage is not None
    assert result['common_name'] == MATCH_100PERCENT['common_name']
    assert percentage == 100.0
