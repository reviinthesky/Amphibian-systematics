import json
from enum import Enum
from typing import Union, List
from .path import get_base_path


class QuestionType(Enum):
    RADIO = 'radio'
    RANGE = 'range'
    MULTI_CHOICES = 'multiple_choices'


class Option:
    def __init__(
            self,
            text: str,
            value: Union[str, int, None]
    ) -> None:
        self.text = text
        self.value = value


class Question:
    def __init__(
        self,
        type: QuestionType,
        text: str,
        key: str,
        options: List[Option],
        range_min=0,
        range_max=0
    ) -> None:
        self.type = type
        self.text = text
        self.key = key
        self.options = options
        self.range_min = range_min
        self.range_max = range_max


class QuestionsLoader:

    def __init__(self) -> None:
        self._load_questions()

    def _load_questions(self):
        with open(get_base_path('data/answers.json'), 'r', encoding='UTF-8') as file:
            options_data = json.load(file)
        with open(get_base_path('data/features_to_questions.json'), 'r', encoding='UTF-8') as file:
            questions_data = json.load(file)

        yes_no_unknown_options = [
            Option('Да', 1),
            Option('Нет', 0),
            Option('Не знаю', 2)
        ]
        # important questions
        size_question = Question(
            type=QuestionType.RANGE,
            text=questions_data['size_cm'],
            key='size_cm',
            options=[],
            range_min=1,
            range_max=20
        )
        tail_question = Question(
            type=QuestionType.RADIO,
            text=questions_data['has_tail'],
            key='has_tail',
            options=yes_no_unknown_options[:2])
        self.important_questions = [size_question, tail_question]
        self.feature_questions = []
        self.key_traits_questions = []
        for key, values in options_data['body_parts'].items():
            question = Question(
                type=(QuestionType.MULTI_CHOICES if key.startswith('m_')
                      else QuestionType.RADIO),
                text=questions_data[key.replace('m_', '')],
                key=key.replace('m_', ''),
                options=(
                    [Option(option, option) for option in values]
                )
            )
            self.feature_questions.append(question)
        for key, values in options_data['key_traits'].items():
            if key.startswith('r_'):
                question = Question(
                    type=QuestionType.RANGE,
                    text=questions_data[key.replace('r_', '')],
                    key=key.replace('r_', ''),
                    options=[],
                    range_min=values[0],
                    range_max=values[1]
                )
            else:
                question = Question(
                    type=QuestionType.RADIO,
                    text=questions_data[key],
                    key=key,
                    options=(yes_no_unknown_options if isinstance(values[0], int)
                             else [Option(option, option) for option in values])
                )
            self.key_traits_questions.append(question)

    def get_questions(self):
        return (self.important_questions,
                self.feature_questions,
                self.key_traits_questions)
