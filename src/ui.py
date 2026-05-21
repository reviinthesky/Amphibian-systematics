import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, Y, ttk, Frame, \
    BOTH, Canvas, LEFT, RIGHT, X, MULTIPLE
from copy import deepcopy
from typing import Any, Dict
from input_handler import InputHandler
from identifier import Identifier


def save_body_parts_values():
    global cur_widget, cur_var
    part_name = body_parts_box.get()
    key_name = body_parts_keys_box.get()

    if isinstance(cur_widget, tk.Listbox):
        selected = cur_widget.curselection()
        value = [cur_widget.get(i) for i in selected]
    else:
        value = cur_var.get()

    for part_dict in answers_dict['body_parts']:
        if part_dict['part'] == part_name:
            part_dict[key_name] = value
            break


def print_answers():
    """Функция для вывода ответов в терминал."""
    print("\n" + "=" * 50)
    print("ТЕКУЩИЕ ОТВЕТЫ:")
    print("=" * 50)
    for key, value in answers_dict.items():
        print(f"{key}: {value}")
    print("=" * 50)


def make_bool_question(text: str):

    question_container = Frame(canvas_frame)
    question_container.pack(fill=X, padx=70, pady=20)

    label = tk.Label(question_container, text=text, font=FONT)
    label.pack(pady=20)

    radio_frame = tk.Frame(question_container)
    radio_frame.pack(pady=10)

    var = tk.IntVar(value=-1)

    def update_answers():
        answers_dict[text] = var.get()

    no_radio = tk.Radiobutton(
        radio_frame,
        text='Нет',
        variable=var,
        value=0,
        font=FONT,
        command=update_answers
    )
    yes_radio = tk.Radiobutton(
        radio_frame,
        text='Да',
        variable=var,
        value=1,
        font=FONT,
        command=update_answers
    )
    no_radio.pack(side=tk.LEFT, padx=40)
    yes_radio.pack(side=tk.RIGHT, padx=40)


def update_answer_widget(e=None):
    global cur_widget, cur_var

    if cur_widget:
        cur_widget.destroy()

    selected_key = body_parts_keys_box.get()
    options = answers_pair.get(selected_key, [])
    if selected_key in ('fringe', 'ridge', 'pattern_size'):
        cur_var = tk.StringVar(value='')
        cur_widget = tk.Frame(answer_frame)
        for option in options:
            rb = tk.Radiobutton(
                cur_widget,
                text=option,
                variable=cur_var,
                value=option
            )
            rb.pack(anchor='w')
    else:
        cur_widget = tk.Listbox(answer_frame, selectmode=MULTIPLE)
        for option in options:
            cur_widget.insert('end', option)
    cur_widget.pack()


def sync_scales(e):
    min_val = size_min.get()
    max_val = size_max.get()

    if max_val < min_val:
        size_max.set(min_val)
        max_val = min_val

    size_max.config(from_=min_val)


DEFAULT_ANSWERS: Dict[str, Any] = {
    "has_tail": None,
    "body_parts": [
        {
            "part": "Голова",
            "pattern": [],
            "pattern_size": [],
            "color": [],
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Спина",
            "pattern": [],
            "pattern_size": [],
            "color": [],
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Брюхо",
            "pattern": [],
            "pattern_size": [],
            "color": [],
            "ridge": None,
            "fringe": None
        },
        {
            "part": "Лапы",
            "pattern": [],
            "pattern_size": [],
            "color": [],
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
    "has_gills": 0,
    "teeth_type": None,
    "has_claws": 0,
    "front_toe_count": 0,
    "back_toe_count": 0,
    "toe_tips_type": None,
    "has_grooves": 0,
    "has_tympanum": 0,
    "has_tubercles": 0,
    "tarsal_fold": None,
    "has_dark_inguinal_loop": 0,
    "has_dark_spot_under_eye": 0,
    "has_longitudinal_ridges": 0,
    "has_temporal_stripe": 0
}
FONT = ('Arial', 12)
input_handler = InputHandler()
bool_questions, sc_questions, mc_questions = input_handler.get_questions()
body_parts = ['Голова', 'Спина', 'Брюхо', 'Лапы', 'Пальцы', 'Хвост']
body_parts_keys = ['pattern', 'pattern_size', 'color', 'fringe', 'ridge']
pattern_answers = ['mosaic', 'solid', 'stripes']
color_answers = ["коричневый", "серый", "белый",
                 "светлый", "бурый", "оливковый", "жёлтый", "розовый"]
pattern_size_answers = ['small', 'medium', 'large']
ridge_answers = [
    "отсутствует",
    "слабовыраженный",
    "зубчатый"
]
fringe_answers = ["отсутствует", "кожистая оторочка"]
answers = [pattern_answers, pattern_size_answers,
           color_answers, fringe_answers, ridge_answers]
answers_pair = dict(zip(body_parts_keys, answers))
answers_dict = deepcopy(DEFAULT_ANSWERS)


def run_ui():
    root = tk.Tk()
    root.title("Systematics")
    root.geometry("800x600")
    root.resizable(False, False)

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = ttk.Scrollbar(
        main_frame, orient=VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox('all')))

    canvas_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    for question in bool_questions:
        make_bool_question(question)

    body_parts_frame = Frame(canvas_frame)
    body_parts_frame.pack(pady=10)

    body_parts_box = ttk.Combobox(body_parts_frame, values=body_parts)
    body_parts_keys_box = ttk.Combobox(
        body_parts_frame, values=body_parts_keys)
    body_parts_box.current(0)
    body_parts_keys_box.current(0)
    body_parts_box.grid(row=0, column=0)
    body_parts_keys_box.grid(row=0, column=1, padx=20)

    answer_frame = tk.Frame(body_parts_frame)
    answer_frame.grid(row=1, column=0, columnspan=3, pady=10)

    cur_widget, cur_var = None, None

    update_answer_widget()
    body_parts_keys_box.bind('<<ComboboxSelected>>', update_answer_widget)
    save_btn = tk.Button(body_parts_frame, text='Сохранить',
                         command=save_body_parts_values)
    save_btn.grid(row=2, column=0, columnspan=3, pady=10)

    # slider section
    slider_frame = tk.Frame(canvas_frame)
    slider_frame.pack()

    min_label = tk.Label(slider_frame, text='Минимальный размер(см)')
    min_label.pack()
    size_min = tk.Scale(slider_frame, from_=1, to=20, orient=HORIZONTAL)
    size_min.pack()

    max_label = tk.Label(slider_frame, text='Максимальный размер(см)')
    max_label.pack()
    size_max = tk.Scale(slider_frame, from_=1, to=20, orient=HORIZONTAL)
    size_max.pack()
    size_min.bind('<ButtonRelease-1>', sync_scales)
    size_max.bind('<ButtonRelease-1>', sync_scales)

    toe_count_front = tk.Scale(slider_frame, from_=3, to=5, orient=HORIZONTAL)
    toe_count_back = tk.Scale(slider_frame, from_=3, to=5, orient=HORIZONTAL)
    toe_count_front.pack()
    toe_count_back.pack()
    check_button = tk.Button(
        root,
        text="Найти амфибию",
        command=print_answers,
        font=('Arial', 10)
    )
    check_button.pack(pady=10)
    root.mainloop()


if __name__ == '__main__':
    run_ui()
