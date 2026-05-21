import json
from enum import Enum
from typing import Any, Dict


class DynamicEnumLoader:
    """Dynamically makes enums from answers.json."""

    def __init__(self, config_path: str = 'data/data.json') -> None:
        """Load enums."""
        self.config_path = config_path
        self.enums: Dict[str, Enum] = self.load_enums()

    def load_enums(self) -> Dict[str, Enum]:
        """Fill dictionary with enums from answers.json."""
        with open(self.config_path, 'r', encoding='utf-8') as file:
            data: Dict[str, Any] = json.load(file)
        enums: Dict[str, Enum] = {}
        for key, values in data.items():
            members: Dict[str, str | int] = {}
            if isinstance(values, list):
                if isinstance(values[0], str):
                    for value in values:
                        members[value.upper()] = value
                elif values[0] == 0:
                    members['HAS'] = 1
                    members['HASN\'T'] = 0
                else:
                    for value in values:
                        members[f'VALUE_{value}'] = value
            else:
                members[key.upper()] = values
            if members:
                enum = Enum(key.upper(), members)  # type: ignore
                enums[f'{key}Enum'] = enum  # type: ignore
        return enums

    def get_enum(self, enum_name) -> Enum:
        """Return Enum from dict."""
        return self.enums[enum_name]

    def get_all_enums(self) -> Dict[str, Enum]:
        """Return dict with enums."""
        return self.enums


if __name__ == "__main__":
    loader = DynamicEnumLoader('data/answers.json')
    loader.load_enums()
    enums: Dict[str, Enum] = loader.get_all_enums()
    for k, enum in enums.items():
        print(f'{k} : {enum.__members__}', end='\n_______\n')  # type: ignore
