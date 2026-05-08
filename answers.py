import json
from enum import Enum
from typing import Any, Dict


class DynamicEnumLoader:
    """Dynamicly makes enums from answers.json."""

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.enums: Dict[str, Enum] = self.load_enums()

    def load_enums(self) -> Dict[str, Enum]:
        """Fills dictionary with enums from answers.json."""
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
                    members['HAS'] = True
                    members['HASN\'T'] = False
                else:
                    for value in values:
                        members[f'VALUE_{value}'] = value
            else:
                members[key.upper()] = values
            if members:
                enum = Enum(key.upper(), members)
                enums[f'{key}Enum'] = enum
        return enums

    def get_enum(self, enum_name) -> Enum:
        """Returns Enum from dict."""
        return self.enums[enum_name]

    def get_all_enums(self) -> Dict[str, Enum]:
        """Returns dict with enums."""
        return self.enums


if __name__ == "__main__":
    loader = DynamicEnumLoader('answers.json')
    loader.load_enums()
    enums: Dict[str, Enum] = loader.get_all_enums()
    print(enums)
    print(loader.get_enum('colorEnum').__members__)
    for k, enum in enums.items():
        print(f'{k} : {enum.__members__}', end='\n_______\n')
