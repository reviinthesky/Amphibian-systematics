import json
from typing import Any, Dict

from answers import DynamicEnumLoader

DEFAULT_ANSWERS: Dict[str, Any] = {
    "has_tail": None,
    "body_parts": [
        {
            "part": "Голова",
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Спина",
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Пальцы",
            "pattern": [],
            "pattern_size": [],
            "color": [],
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Хвост",
            "pattern": [],
            "pattern_size": [],
            "color": [],
            "ridge": None,
            "fringe": None
        }
    ],
    "size_cm": [],
    "key_traits": {
        "has_gills": 0,
        "teeth_type": None,
        "has_claws": 0,
        "front_toe_count": 0,
        "back_toe_count": 0,
        "toe_tips_type": None,
        "has_grooves": 0,
        "has_tympanum": 0,
        "has_tubercles": 0,
        "has_tarsal_fold": None,
        "has_dark_inguinal_loop": None,
        "has_dark_spot_under_eye": None,
        "longitudinal_ridges": None,
    }
}


class InputHandler:

    def __init__(self) -> None:
        self.enum_loader = DynamicEnumLoader()
        self.user_input: Dict[str, Any] = DEFAULT_ANSWERS
        self._load_questions()

    def _load_questions(self):
        with open('data/answers.json', 'r', encoding='UTF-8') as file:
            data = json.load(file)
        self.bool_questions = []
        self.single_choice_questions = []
        self.multiple_choices_questions = []
        for key in data.keys():
            if key.startswith('has_'):
                self.bool_questions.append(key)
            elif key.startswith('s_'):
                self.single_choice_questions.append(key)
            elif key.startswith('m_'):
                self.multiple_choices_questions.append(key)

    def get_questions(self):
        return self.bool_questions, \
            self.single_choice_questions, self.multiple_choices_questions
