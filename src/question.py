from enum import Enum


class QuestionType(Enum):
    BOOL = 'bool'
    RANGE = 'range'
    SINGLE_CHOICE = 'single_choice'
    MULTI_CHOICES = 'multiple_choices'


class Question:
    def __init__(
        self,
        id: str,
        type: QuestionType,
        text: str,
        options: list[str]
    ) -> None:
        self.id = id
        self.type = type
        self.text = text
        self.options = options
