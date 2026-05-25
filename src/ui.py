import tkinter as tk
from tkinter import ttk, Frame, Canvas, font
from typing import Any, Dict, Literal

from .question import Question, QuestionType, QuestionsLoader

body_parts = ['Голова', 'Спина', 'Брюхо', 'Лапы', 'Пальцы', 'Хвост']
questionloader = QuestionsLoader()
important_questions, feature_questions, \
    key_traits_questions = questionloader.get_questions()


class UI:
    def __init__(self, root):
        self.root = root
        self.answers = {
            'Голова': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            'Спина': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            'Лапы': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            'Пальцы': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            'Хвост': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            'Брюхо': {
                "pattern": [],
                "pattern_size": [],
                "color": [],
                "ridge": None,
                "fringe": None
            },
            "has_tail": 0,
            "size_cm": [0, 0],
            "has_gills": None,
            "teeth_type": None,
            "has_claws": None,
            "front_toe_count": None,
            "back_toe_count": None,
            "toe_tips_type": None,
            "has_grooves": None,
            "has_tympanum": None,
            "has_tubercles": None,
            "tarsal_fold": None,
            "has_dark_inguinal_loop": None,
            "has_dark_spot_under_eye": None,
            "has_longitudinal_ridges": None,
        }

        self.FONT = font.Font(family='Farabee', size=14, name='Farabee')
        self.FONT.configure(family='fonts/ofont.ru_Farabee.ttf')

        self.combobox_style = ttk.Style()
        self.combobox_style.theme_use('clam')
        self.combobox_style.configure(
            "Custom.TCombobox",
            borderwidth=3,
            relief='solid',
            fieldbackground='#90AB8B',
            foreground='black',
            background='#90AB8B'
        )
        self.combobox_style.map(
            "Custom.TCombobox",
            background=[('focus', '#3B4953')],
            fieldbackground=[('focus', '#90AB8B')]
        )
        self.root.option_add('*TCombobox*Listbox.font', self.FONT)
        self.root.option_add('*TCombobox*Listbox.background', '#90AB8B')
        self.root.option_add('*TCombobox*Listbox.foreground', 'black')
        self.root.option_add("*TCombobox*Listbox.selectBackground", '#3B4953')
        self.root.configure(bg='#3B4953')
        main_frame = Frame(self.root, bg='#3B4953')
        main_frame.pack(fill='both', expand=1)

        my_canvas = Canvas(main_frame, bg='#AFC4B7')
        my_canvas.pack(side='left', fill='both', expand=1)

        scrollbar = ttk.Scrollbar(
            main_frame, orient='vertical', command=my_canvas.yview)
        scrollbar.pack(side='right', fill='y')

        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox('all')))

        canvas_frame = Frame(my_canvas, bg='#AFC4B7')
        my_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        important_frame = Frame(canvas_frame, bg='#AFC4B7')
        important_frame.pack()

        for question in important_questions:
            if question.type == QuestionType.RADIO:
                self._make_radio_question(question, important_frame, 'int')
            else:
                self._make_range_question(question, important_frame)

        key_traits_frame = Frame(canvas_frame, bg='#AFC4B7')
        key_traits_frame.pack()
        for question in key_traits_questions:
            if question.type == QuestionType.RADIO:
                self._make_radio_question(
                    question,
                    key_traits_frame,
                    ('int' if isinstance(question.options[0].value, int)
                     else 'str'))
            elif question.type == QuestionType.RANGE:
                self._make_range_question(question, key_traits_frame)

        body_parts_frame = Frame(canvas_frame, bg='#AFC4B7')
        body_parts_frame.pack(pady=10)

        parts_label = self._make_label(body_parts_frame, 'Части тела')
        parts_label.grid(row=0, column=0)

        self.parts_box = ttk.Combobox(
            body_parts_frame,
            values=body_parts,
            font=self.FONT,
            style='Custom.TCombobox',
            background='#90AB8B')
        self.parts_box.grid(row=1, column=0, padx=20)
        self.parts_box.current(0)
        self.parts_box.bind('<<ComboboxSelected>>', self._on_part_change)

        feature_label = self._make_label(body_parts_frame, 'Характеристики')
        feature_label.grid(row=0, column=1)
        feature_values = [q.text for q in feature_questions]
        self.part_features_box = ttk.Combobox(
            body_parts_frame,
            values=feature_values,
            font=self.FONT,
            style='Custom.TCombobox',
            background='#90AB8B'
        )
        self.part_features_box.grid(row=1, column=1, padx=20)
        self.part_features_box.current(0)
        self.part_features_box.bind(
            '<<ComboboxSelected>>', self._on_feature_change)

        self.options_frame = tk.Frame(body_parts_frame, bg='#AFC4B7')
        self.options_frame.grid(row=3, column=0, pady=30, columnspan=3)
        self._on_feature_change()

    def _on_part_change(self, e):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def _on_feature_change(self, e=None):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        selected_feature = self.part_features_box.get()
        for question in feature_questions:
            if question.text == selected_feature:
                break
        else:
            return
        if question.type == QuestionType.RADIO:
            self._make_radio_question(question, self.options_frame, 'str')
        elif question.type == QuestionType.MULTI_CHOICES:
            self._make_multi_question(question, self.options_frame)

    def _make_radio_question(
            self,
            question: Question,
            frame: Frame | Canvas,
            value_type: Literal['str'] | Literal['int']
    ) -> None:
        if question.type != QuestionType.RADIO:
            raise ValueError('Question type is not radio!')
        question_container = Frame(frame, bg='#AFC4B7')
        question_container.pack(fill='x', padx=70, pady=20)

        label = self._make_label(question_container, question.text)
        label.pack(fill='x')

        radio_frame = tk.Frame(question_container, bg='#AFC4B7')
        radio_frame.pack(pady=10, padx=70)

        var = tk.IntVar(value=0) if value_type == 'int' else tk.StringVar()

        for i, option in enumerate(question.options):
            rd_button = tk.Radiobutton(
                radio_frame,
                value=option.value,
                text=option.text,
                variable=var,
                command=lambda: self._save_answer(
                    isBodyPart=False,
                    key=question.key,
                    value=var.get()
                ),
                bg='#90AB8B',
                highlightcolor='#3B4953',
                highlightbackground='#3B4953'
            )
            rd_button.grid(row=0, column=i)

    def _make_range_question(
            self,
            question: Question,
            frame: Frame | Canvas,
    ) -> None:
        if question.type != QuestionType.RANGE:
            raise ValueError('Question type is not range!')

        range_container = tk.Frame(frame, bg='#AFC4B7')
        range_container.pack(fill='x', pady=20)

        if question.key != 'size_cm':
            label = self._make_label(range_container, question.text)
            label.pack(fill='x', pady=20)
            slider = tk.Scale(
                range_container,
                from_=question.range_min,
                to=question.range_max,
                orient='horizontal',
                sliderrelief='flat',
                bg='#5A7863',
                highlightbackground='#3B4953',
                troughcolor='#90AB8B',
                fg='white',
                highlightthickness=3)
            slider.pack(fill='x')
            slider.bind('<ButtonRelease-1>',
                        lambda e: self._save_answer(question.key,
                                                    slider.get()))
            return
        else:
            label_min = self._make_label(range_container, 'Минимальный размер(см)')
            slider_min = tk.Scale(
                range_container,
                from_=question.range_min,
                to=question.range_max,
                orient='horizontal',
                sliderrelief='flat',
                bg='#5A7863',
                highlightbackground='#3B4953',
                troughcolor='#90AB8B',
                fg='white',
                highlightthickness=3

            )
            label_max = self._make_label(range_container, 'Максимальный размер(см)')
            slider_max = tk.Scale(
                range_container,
                from_=question.range_min,
                to=question.range_max,
                orient='horizontal',
                sliderrelief='flat',
                bg='#5A7863',
                highlightbackground='#3B4953',
                troughcolor='#90AB8B',
                fg='white'
            )
            label_min.pack(fill='x')
            slider_min.pack(fill='x')
            label_max.pack(fill='x')
            slider_max.pack(fill='x')

            def sync_scales(e):
                min_val = slider_min.get()
                max_val = slider_max.get()

                if max_val < min_val:
                    slider_max.set(min_val)
                    max_val = min_val

                slider_max.config(from_=min_val)
                self._save_answer(key=question.key, value=[min_val, max_val])

            slider_min.bind('<ButtonRelease-1>', sync_scales)
            slider_max.bind('<ButtonRelease-1>', sync_scales)

    def _make_multi_question(
        self,
        question: Question,
        frame: Frame | Canvas,
    ) -> None:
        if question.type != QuestionType.MULTI_CHOICES:
            raise ValueError('The question is not multi-choice!')

        label = self._make_label(frame, question.text)
        label.pack(padx=40)

        box_scrollbar = tk.Scrollbar(frame, orient='vertical')
        listbox = tk.Listbox(
            frame,
            selectmode='multiple',
            yscrollcommand=box_scrollbar.set,
            highlightbackground='#3B4953',
            highlightcolor='#3B4953',
            highlightthickness=3,
            bg='#90AB8B',
            font=self.FONT
        )
        box_scrollbar.config(command=listbox.yview)
        box_scrollbar.pack(side='right', fill='y')
        listbox.pack(padx=40)

        for option in question.options:
            listbox.insert('end', option.text)
        listbox.bind('<<ListboxSelect>>',
                     lambda e: self._save_answer(
                         isBodyPart=True,
                         key=question.key,
                         value=[listbox.get(i) for i in listbox.curselection()]))

    def _save_answer(self, key, value, isBodyPart=False):
        if isBodyPart:
            self.answers[self.parts_box.get()][key] = value
        else:
            self.answers[key] = value

    def _make_label(self, frame: Frame | Canvas, text: str) -> tk.Label:
        label = tk.Label(
            frame,
            text=text,
            font=self.FONT,
            bg='#90AB8B',
            highlightbackground='#3B4953',
            highlightcolor='#3B4953',
            highlightthickness=3)
        return label


def run_questionier():
    root = tk.Tk()
    root.title("Systematics")
    root.geometry("800x600")
    root.resizable(False, False)

    ui = UI(root)

    def on_submit():
        root.destroy()

    check_button = tk.Button(
        root,
        text="Найти амфибию",
        command=on_submit,
        bg='#90AB8B',
        font=ui.FONT
    )
    check_button.pack(pady=10)
    root.mainloop()

    return ui.answers


def show_result_window(top3, winner, winner_percentage):
    result_root = tk.Tk()
    result_root.title("Результат идентификации")
    result_root.geometry("600x500")
    result_root.resizable(True, True)

    # Основной фрейм с прокруткой
    main_frame = ttk.Frame(result_root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side='left', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(
        main_frame, orient='vertical', command=my_canvas.yview)
    scrollbar.pack(side='right', fill='y')

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox('all')))

    canvas_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    # Заголовок для топ‑3
    ttk.Label(
        canvas_frame,
        text="Топ‑3 возможных вида и их проценты совпадения:").pack(anchor="w", pady=(10, 5))

    for i, item in enumerate(top3, 1):
        species, percentage = item
        ttk.Label(
            canvas_frame,
            text=f"{i}. {species['common_name']} процент: {percentage:.2f}"
        ).pack(anchor="w", pady=2)

    ttk.Separator(canvas_frame, orient="horizontal").pack(
        fill="x", pady=15)

    ttk.Label(
        canvas_frame,
        text="Победитель:",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", pady=(10, 5))

    ttk.Label(
        canvas_frame,
        text=f"Вид: {winner['common_name']}",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=5)

    ttk.Label(
        canvas_frame,
        text=f"Латинское название: {winner['latin_name']}",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=5)

    ttk.Label(
        canvas_frame,
        text=f"Уверенность: {winner_percentage:.2f}%",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=5)

    ttk.Label(
        canvas_frame,
        text="Характерные особенности:",
        font=("Arial", 12, "underline")
    ).pack(anchor="w", pady=(15, 5))

    for feature in winner['unique_features']:
        ttk.Label(
            canvas_frame,
            text=feature,
            font=("Arial", 11),
            wraplength=550,
            justify="left"
        ).pack(anchor="w", pady=5)

    result_root.mainloop()


def show_failed_window():
    root = tk.Tk()
    root.title("Поиск...")
    root.geometry("600x200")
    root.resizable(True, True)
    tk.Label(root, text='Простите, подобных земноводных не найдено :С',
             font=('Arierl', 15, 'bold')).pack()
    root.mainloop()


if __name__ == '__main__':
    run_questionier()
