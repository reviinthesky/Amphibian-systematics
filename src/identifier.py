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

KEY_TRAITS_WEIGHT = 30.0
BODY_PARTS_WEIGHT = 45.0
SIZE_WEIGHT = 25.0

BODY_PARTS_TRAITS_WEIGHT: Dict[str, float] = {
    'pattern': 0.25 * BODY_PARTS_WEIGHT,
    'pattern_size': 0.15 * BODY_PARTS_WEIGHT,
    'color': 0.3 * BODY_PARTS_WEIGHT,
    'ridge': 0.1 * BODY_PARTS_WEIGHT,
    'fringe': 0.1 * BODY_PARTS_WEIGHT,
    'size': 0.1 * BODY_PARTS_WEIGHT
}


class Identifier:
    """Main class of the app."""

    def __init__(self):
        self._load_data()

    def _load_data(self):
        with open('data/data.json', 'r', encoding='UTF-8') as file:
            data = json.load(file)
            self.tailed = data['Tailed']
            self.tailles = data['Tailles']

    def _compare_body_parts(
            self,
            input_parts: List[Dict[str, Any]],
            species_parts: List[Dict[str, Any]],
            isTailles: bool) -> float:

        part_score: float = 0
        matched_parts_count = 0
        for body_part in input_parts:
            for species_body_part in species_parts:
                if body_part['part'] == 'Хвост' and isTailles:
                    continue
                if body_part['part'] == species_body_part['part']:
                    part_score += self._compare_list_trait(
                        body_part['pattern'],
                        species_body_part['pattern'],
                        BODY_PARTS_TRAITS_WEIGHT['pattern'])
                    part_score += self._compare_list_trait(
                        body_part['pattern_size'],
                        species_body_part['pattern_size'],
                        BODY_PARTS_TRAITS_WEIGHT['pattern_size'])
                    part_score += self._compare_list_trait(
                        body_part['color'],
                        species_body_part['color'],
                        BODY_PARTS_TRAITS_WEIGHT['color'])
                    part_score += self._compare_str_trait(
                        body_part['ridge'],
                        species_body_part['ridge'],
                        BODY_PARTS_TRAITS_WEIGHT['ridge'])
                    part_score += self._compare_str_trait(
                        body_part['fringe'],
                        species_body_part['fringe'],
                        BODY_PARTS_TRAITS_WEIGHT['fringe'])
                    matched_parts_count += 1
                    break
        if matched_parts_count == 0:
            return 0.0
        return part_score / matched_parts_count

    def _compare_key_traits(
            self,
            user_input: Dict[str, Any],
            species: Dict[str, Any]) -> float:
        matches = 0
        total_traits = len(species)
        if total_traits != len(user_input):
            print(total_traits, len(user_input))
            print(species)
            print('-'*10)
            print(user_input)
            raise ValueError(
                'Bad input, not enough key traits. Check input module')

        for trait in user_input:
            if user_input[trait] == species[trait]:
                matches += 1
        return (matches/total_traits) * KEY_TRAITS_WEIGHT

    def _compare_size(
            self,
            input_size: tuple[int, int],
            species_size: tuple[int, int]) -> float:
        input_min, input_max = input_size
        species_min, species_max = species_size

        min_diff = abs(input_min - species_min)
        max_diff = abs(input_max - species_max)
        avg_diff = (min_diff + max_diff) / 2

        if avg_diff > 2:
            return 0.0

        overlap_start = max(input_min, species_min)
        overlap_end = min(input_max, species_max)
        overlap = max(0, overlap_end - overlap_start)

        union_start = min(input_min, species_min)
        union_end = max(input_max, species_max)
        union = union_end - union_start

        if union == 0:
            return SIZE_WEIGHT

        base_overlap_score = overlap/union
        return base_overlap_score * SIZE_WEIGHT

    def find_matches(self, user_input: Dict[str, Any]):
        """
        Calls other functions to assign score and find
        species based on user input.
        """
        isTailles = False
        if user_input.get('has_tail', False):
            species_list = self.tailed
        else:
            species_list = self.tailles
            isTailles = True

        found_species: list[tuple[Dict, float]] = []

        for species in species_list:
            size_score = self._compare_size(
                tuple(user_input['size_cm']),
                tuple(species['characteristics']['size_cm'])
            )
            print(size_score)
            key_traits_score = self._compare_key_traits(
                user_input['key_traits'],
                species['characteristics']['key_traits'])
            print(key_traits_score)
            body_parts_score = self._compare_body_parts(
                user_input['body_parts'],
                species['characteristics']['body_parts'],
                isTailles
            )
            print(body_parts_score)
            total_score = size_score + key_traits_score + body_parts_score
            if total_score < 50:
                continue
            found_species.append((species, total_score))

        if not found_species:
            return None, None, None
        else:
            found_species.sort(key=lambda x: x[1], reverse=True)
            top_3 = found_species[:3]
            winner, percentage = top_3[0]
            print(top_3[0][1], top_3[1][1])
            return top_3, winner, percentage

    def _compare_list_trait(
            self,
            input_trait: List[str],
            species_trait: List[str],
            weight: float) -> float:

        if input_trait is None or species_trait is None:
            return 0.0

        input_set = set(input_trait)
        species_set = set(species_trait)
        matches = input_set & species_set
        max_possible_matches = max(len(input_set), len(species_set))
        match_score = len(matches) / max_possible_matches
        return match_score * weight

    def _compare_str_trait(self, input_trait, species_trait, weight) -> float:
        if input_trait is None or species_trait is None:
            return 0.0

        return weight if input_trait == species_trait else 0.0
