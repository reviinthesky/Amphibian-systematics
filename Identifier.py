import json
from typing import Any, Dict, List


DEFAULT_ANSWERS: Dict[str, Any] = {
    "body_parts": [
        {
            "part": "Голова",
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        },
        {
            "part": "Спина",
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        },
        {
            "pattern": None,
            "pattern_size": None,
            "color": None,
            "ridge": None,
            "fringe": None,
            "size": None
        }
    ],
    "has_gills": None,
    "teeth_type": None,
    "has_claws": None,
    "front_toe_count": None,
    "back_toe_count": None,
    "toe_tips_type": None,
    "size_cm": None,
    "has_grooves": None,
    "has_tympanum": None,
    "has_tubercles": None,
    "tarsal_fold": None,
    "dark_inguinal_loop": None,
    "dark_spot_under_eye": None,
    "longitudinal_ridges": None,
    "inner_metatarsal_tubercle_to_toe_ratio": None,
    "inner_metatarsal_tubercle_to_shin_ratio": None
}


class Identifier:
    def __init__(self):
        self.load_data()

    def load_data(self):
        with open('data.json') as file:
            data = json.load(file)
            self.tailed = data['amphibians']['Хвостатые']
            self.tailles = data['amphibians']['Безхвостые']

    def calculate_similiarity():
        pass

    def compare_body_parts(self, input_parts, species_parts) -> float:
        score = 0.0
        total_checks = 0
        for input_part in input_parts:
            for species_part in species_parts:
                if input_part['part'] == species_part['part']:
                    part_score = 0.0
                    checks = 0

                    if input_part['pattern'] and species_part['pattern']:
                        part_score += self._compare_patterns(
                            input_part['pattern'], species_part['pattern'])
                        checks += 1
                    if input_part['pattern_size'] and species_part['pattern_size']:
                        part_score += self._compare_pattern_size(
                            input_part['pattern_size'], species_part['pattern_size'])
                        checks += 1
                    if input_part['color'] and species_part['color']:
                        part_score += self._compare_colors(
                            input_part['color'], species_part['color'])
                        checks += 1
                    if input_part['ridge'] and species_part['ridge']:
                        part_score += 1.0 if input_part['ridge'] == species_part['ridge'] else 0.0
                        checks += 1
                    if input_part['fringe'] and species_part['fringe']:
                        part_score += 1.0 if input_part['fringe'] == species_part['fringe'] else 0.0
                        checks += 1
                    if input_part['size'] and species_part['size']:
                        part_score += self._compare_size(
                            input_part['size'], species_part['size'])
                        checks += 1
            if checks > 0:
                score += part_score / checks
                total_checks += 1
        return score / total_checks if total_checks > 0 else 0.0

    def _compare_colors(self, input_color: list[str], other_color: list[str]) -> float:
        user_colors = set(input_color)
        other_colors = set(other_color)

        intersection_length = len(user_colors.intersection(other_colors))
        max_possible = min(len(user_colors), len(other_colors))
        return intersection_length / max_possible

    def _compare_patterns(self, user_pattern: list[str], other_pattern: list[str]) -> float:
        user_patterns = set(user_pattern)
        other_patterns = set(other_pattern)

        intersection_length = len(user_patterns.intersection(other_patterns))
        max_possible = min(len(user_patterns), len(other_patterns))

        return intersection_length / max_possible

    def _compare_pattern_size(self, size1: str, size2: str) -> float:
        return 1.0 if size1 == size2 else 0.0

    def _compare_size(self, input_size: tuple[int, int], other_size: tuple[int, int]) -> float:
        input_min, input_max = input_size
        other_min, other_max = other_size

        min_match = self._check_value_match(input_min, other_min)
        max_match = self._check_value_match(input_max, other_max)

        return (min_match + max_match) / 2

    def _check_value_match(self, value1: int, value2: int) -> float:
        if value1 == value2:
            return 1.0

        if abs(value1 - value2) == 1:
            return 0.7

        if abs(value1 - value2) == 2:
            return 0.4

        if (value1 <= value2 <= value1 + 2) or (value2 <= value1 <= value2 + 2):
            return 0.3

        return 0.0

    def find_matches(self, user_input):
        if user_input.get('has_tail', False):
            species_list = self.tailed
        else:
            species_list = self.tailles
