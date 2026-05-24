# Sorry i was too tired to make it smarter way. Gimme a slack will ya?

def normalize_input(user_input):
    final_dict = {
        'has_tail': user_input['has_tail'],
        'size_cm': user_input['size_cm'],
        'body_parts': [
            {
                "part": "Голова",
                "pattern": user_input['Голова']['pattern'],
                "pattern_size": user_input['Голова']['pattern_size'],
                "color": user_input['Голова']['color'],
                        "ridge": user_input['Голова']['ridge'],
                        "fringe": user_input['Голова']['fringe']
            },
            {
                "part": "Спина",
                "pattern": user_input['Спина']['pattern'],
                "pattern_size": user_input['Спина']['pattern_size'],
                "color": user_input['Спина']['color'],
                "ridge": user_input['Спина']['ridge'],
                "fringe": user_input['Спина']['fringe']
            },
            {
                "part": "Брюхо",
                "pattern": user_input['Брюхо']['pattern'],
                "pattern_size": user_input['Брюхо']['pattern_size'],
                "color": user_input['Брюхо']['color'],
                "ridge": user_input['Брюхо']['ridge'],
                "fringe": user_input['Брюхо']['fringe']
            },
            {
                "part": "Лапы",
                "pattern": user_input['Лапы']['pattern'],
                "pattern_size": user_input['Лапы']['pattern_size'],
                "color": user_input['Лапы']['color'],
                "ridge": user_input['Лапы']['ridge'],
                "fringe": user_input['Лапы']['fringe']
            },
            {
                "part": "Пальцы",
                "pattern": user_input['Пальцы']['pattern'],
                "pattern_size": user_input['Пальцы']['pattern_size'],
                "color": user_input['Пальцы']['color'],
                "ridge": user_input['Пальцы']['ridge'],
                "fringe": user_input['Пальцы']['fringe']
            },
            {
                "part": "Хвост",
                "pattern": user_input['Хвост']['pattern'],
                "pattern_size": user_input['Хвост']['pattern_size'],
                "color": user_input['Хвост']['color'],
                "ridge": user_input['Хвост']['ridge'],
                "fringe": user_input['Хвост']['fringe']
            }
        ],
        'key_traits': {
            "has_gills": user_input['has_gills'],
            "teeth_type": user_input['teeth_type'],
            "has_claws": user_input['has_claws'],
            "front_toe_count": user_input['front_toe_count'],
            "back_toe_count": user_input['back_toe_count'],
            "toe_tips_type": user_input['toe_tips_type'],
            "has_grooves": user_input['has_grooves'],
            "has_tympanum": user_input['has_tympanum'],
            "has_tubercles": user_input['has_tubercles'],
            "tarsal_fold": user_input['tarsal_fold'],
            "has_dark_inguinal_loop": user_input['has_dark_inguinal_loop'],
            "has_dark_spot_under_eye": user_input['has_dark_spot_under_eye'],
            "has_longitudinal_ridges": user_input['has_longitudinal_ridges'],
        }
    }
    return final_dict
