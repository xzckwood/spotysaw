import os
import json
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex


Window.clearcolor = get_color_from_hex("#211713")
Window.size = (420, 780)

BG = "#211713"
PANEL = "#392820"
ACCENT = "#D2AD91"
TEXT = "#F5E9DF"
MUTED = "#C5AA98"
INPUT = "#30211B"

# Полупрозрачные оттенки
BUTTON_COLOR = (0.30, 0.20, 0.15, 0.78)
BUTTON_DOWN = (0.43, 0.29, 0.21, 0.92)
INPUT_COLOR = (0.17, 0.11, 0.08, 0.88)


class SpotySaw(App):

    def build(self):
        self.title = "spotysaw"
        self.data_file = "spotysaw_data.json"

        self.data = {
            "notes": [],
            "expenses": [],
            "events": [],
            "wishes": []
        }

        self.load_data()

        self.current_photo = None
        self.edited_photo = None
        self.photo_preview = None

        self.root = FloatLayout()
        self.show_home()

        return self.root

    # =====================================
    # ДАННЫЕ
    # =====================================

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    saved = json.load(file)

                for key in self.data:
                    self.data[key] = saved.get(key, [])

            except Exception:
                pass

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=4
            )

    # =====================================
    # ОБЩЕЕ ОФОРМЛЕНИЕ
    # =====================================

    def set_page(self, page):
        self.root.clear_widgets()
        self.root.add_widget(page)

    def label(
        self,
        text,
        size=16,
        color=TEXT,
        height=42,
        halign="left",
        font="Roboto"
    ):
        return Label(
            text=str(text),
            font_name=font,
            font_size=dp(size),
            color=get_color_from_hex(color),
            size_hint_y=None,
            height=dp(height),
            halign=halign,
            valign="middle",
            text_size=(Window.width - dp(65), None)
        )

    def make_button(self, text, callback, height=58, font_size=16):
        btn = Button(
            text=str(text),
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=get_color_from_hex(TEXT),
            font_name="Roboto",
            font_size=dp(font_size),
            halign="left",
            valign="middle",
            padding=(dp(19), dp(8))
        )

        with btn.canvas.before:
            Color(*BUTTON_COLOR)
            btn.bg = RoundedRectangle(
                pos=btn.pos,
                size=btn.size,
                radius=[dp(18)]
            )

        btn.bind(
            pos=lambda instance, value:
            setattr(instance.bg, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg, "size", value)
        )

        def change_color(instance, state):
            instance.canvas.before.clear()

            with instance.canvas.before:
                if state == "down":
                    Color(*BUTTON_DOWN)
                else:
                    Color(*BUTTON_COLOR)

                instance.bg = RoundedRectangle(
                    pos=instance.pos,
                    size=instance.size,
                    radius=[dp(18)]
                )

        btn.bind(state=change_color)
        btn.bind(on_release=callback)

        return btn

    def make_input(self, hint, multiline=False, height=52):
        field = TextInput(
            hint_text=hint,
            multiline=multiline,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            foreground_color=get_color_from_hex(TEXT),
            hint_text_color=get_color_from_hex(MUTED),
            cursor_color=get_color_from_hex(ACCENT),
            padding=[dp(15), dp(14)],
            font_size=dp(15),
            font_name="Roboto"
        )

        with field.canvas.before:
            Color(*INPUT_COLOR)
            field.bg = RoundedRectangle(
                pos=field.pos,
                size=field.size,
                radius=[dp(15)]
            )

        field.bind(
            pos=lambda instance, value:
            setattr(instance.bg, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg, "size", value)
        )

        return field

    def page_background(self):
        root = FloatLayout()

        with root.canvas.before:
            Color(*get_color_from_hex(BG))
            root.bg_rectangle = RoundedRectangle(
                pos=root.pos,
                size=root.size,
                radius=[0]
            )

        root.bind(
            pos=lambda instance, value:
            setattr(instance.bg_rectangle, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg_rectangle, "size", value)
        )

        if os.path.exists("home_bg.jpg"):
            wallpaper = Image(
                source="home_bg.jpg",
                size_hint=(1, 1),
                opacity=0.38,
                allow_stretch=True,
                keep_ratio=False
            )
            root.add_widget(wallpaper)

        return root

    def page_layout(self, title, subtitle=""):
        background = self.page_background()

        content = BoxLayout(
            orientation="vertical",
            padding=[dp(19), dp(18), dp(19), dp(18)],
            spacing=dp(11),
            size_hint=(1, 1)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(10)
        )

        back = self.make_button(
            "назад",
            lambda *_: self.show_home(),
            height=46,
            font_size=14
        )
        back.size_hint_x = None
        back.width = dp(83)

        header.add_widget(back)

        header.add_widget(
            self.label(
                title,
                23,
                ACCENT,
                50,
                font="Georgia"
            )
        )

        content.add_widget(header)

        if subtitle:
            content.add_widget(
                self.label(
                    subtitle,
                    13,
                    MUTED,
                    38
                )
            )

        background.add_widget(content)
        self.set_page(background)

        return content

    def add_section_title(self, layout, text):
        layout.add_widget(
            self.label(
                text,
                17,
                ACCENT,
                42,
                font="Georgia"
            )
        )

    def show_message(self, title, message):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )

        box.add_widget(
            Label(
                text=message,
                color=get_color_from_hex(TEXT),
                font_size=dp(15),
                font_name="Roboto"
            )
        )

        popup = Popup(
            title=title,
            content=box,
            size_hint=(0.85, 0.4),
            background_color=get_color_from_hex(PANEL),
            separator_color=get_color_from_hex(ACCENT),
            title_color=get_color_from_hex(ACCENT),
            title_size=dp(17)
        )

        box.add_widget(
            self.make_button(
                "закрыть",
                lambda *_: popup.dismiss(),
                45
            )
        )

        popup.open()

    def make_popup(self, title, box, size=(0.9, 0.7)):
        return Popup(
            title=title,
            content=box,
            size_hint=size,
            background_color=get_color_from_hex(PANEL),
            separator_color=get_color_from_hex(ACCENT),
            title_color=get_color_from_hex(ACCENT),
            title_size=dp(18)
        )

    # =====================================
    # ГЛАВНАЯ
    # =====================================

    def show_home(self):
        root = self.page_background()

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )

        content = BoxLayout(
            orientation="vertical",
            padding=[dp(23), dp(35), dp(23), dp(22)],
            spacing=dp(13),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(
            self.label(
                "spotysaw",
                39,
                ACCENT,
                65,
                "center",
                "Georgia"
            )
        )

        content.add_widget(
            self.label(
                "ТВОЁ ЛИЧНОЕ ПРОСТРАНСТВО",
                11,
                MUTED,
                30,
                "center"
            )
        )

        content.add_widget(
            self.label(
                "Место, где можно сохранить мысли,\n"
                "планы, мечты и важные моменты.",
                15,
                TEXT,
                65,
                "center"
            )
        )

        content.add_widget(
            self.label(
                "МОИ РАЗДЕЛЫ",
                13,
                ACCENT,
                38,
                font="Georgia"
            )
        )

        sections = [
            (
                "Заметки",
                "Мысли, идеи и личные записи",
                self.show_notes
            ),
            (
                "Расходы",
                "Доходы, покупки и баланс",
                self.show_expenses
            ),
            (
                "События",
                "Планы и важные даты",
                self.show_events
            ),
            (
                "Желания",
                "Всё, что хочется исполнить",
                self.show_wishes
            ),
            (
                "Фотостудия",
                "Обработка и сохранение фотографий",
                self.show_photo_studio
            )
        ]

        for title, description, action in sections:
            content.add_widget(
                self.make_button(
                    title + "\n" + description,
                    lambda _, a=action: a(),
                    75,
                    16
                )
            )

        content.add_widget(
            self.label(
                "СОХРАНЯЙ СВОИ МОМЕНТЫ",
                11,
                MUTED,
                42,
                "center"
            )
        )

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.set_page(root)

    # =====================================
    # ЗАМЕТКИ
    # =====================================

    def show_notes(self):
        layout = self.page_layout(
            "Мои заметки",
            "Все твои мысли и записи в одном месте."
        )

        layout.add_widget(
            self.make_button(
                "Создать новую заметку",
                self.add_note
            )
        )

        search = self.make_input("Поиск по заметкам")
        layout.add_widget(search)

        scroll = ScrollView()

        items = BoxLayout(
            orientation="vertical",
            spacing=dp(9),
            size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))

        def refresh(*args):
            items.clear_widgets()
            query = search.text.lower()

            for index, note in enumerate(self.data["notes"]):
                title = note.get("title", "Без названия")
                body = note.get("body", "")

                if query and query not in (
                    title + " " + body
                ).lower():
                    continue

                items.add_widget(
                    self.make_button(
                        title + "\n" + body[:90],
                        lambda _, i=index: self.open_note(i),
                        76
                    )
                )

            if not items.children:
                items.add_widget(
                    self.label(
                        "Здесь пока нет заметок.\n"
                        "Создай первую запись.",
                        14,
                        MUTED,
                        65
                    )
                )

        search.bind(text=refresh)

        scroll.add_widget(items)
        layout.add_widget(scroll)
        refresh()

    def add_note(self, *_):
        self.note_editor()

    def open_note(self, index):
        self.note_editor(index)

    def note_editor(self, index=None):
        editing = index is not None

        old = (
            self.data["notes"][index]
            if editing
            else {"title": "", "body": ""}
        )

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        title = self.make_input("Название заметки")
        title.text = old.get("title", "")

        body = self.make_input(
            "Напиши здесь свою заметку...",
            True,
            180
        )
        body.text = old.get("body", "")

        box.add_widget(title)
        box.add_widget(body)

        popup = self.make_popup(
            "Моя заметка",
            box,
            (0.92, 0.75)
        )

        def save_note():
            if not title.text.strip() and not body.text.strip():
                return

            item = {
                "title": title.text.strip() or "Без названия",
                "body": body.text.strip()
            }

            if editing:
                self.data["notes"][index] = item
            else:
                self.data["notes"].insert(0, item)

            self.save_data()
            popup.dismiss()
            self.show_notes()

        box.add_widget(
            self.make_button(
                "Сохранить заметку",
                lambda *_: save_note()
            )
        )

        if editing:
            def delete_note():
                self.data["notes"].pop(index)
                self.save_data()
                popup.dismiss()
                self.show_notes()

            box.add_widget(
                self.make_button(
                    "Удалить заметку",
                    lambda *_: delete_note()
                )
            )

        popup.open()

    # =====================================
    # РАСХОДЫ
    # =====================================

    def show_expenses(self):
        layout = self.page_layout(
            "Мои расходы",
            "Следи за своими деньгами и покупками."
        )

        income = sum(
            x["amount"]
            for x in self.data["expenses"]
            if x["kind"] == "доход"
        )

        expenses = sum(
            x["amount"]
            for x in self.data["expenses"]
            if x["kind"] == "расход"
        )

        balance = income - expenses

        layout.add_widget(
            self.label(
                "ТЕКУЩИЙ БАЛАНС",
                13,
                MUTED,
                30
            )
        )

        layout.add_widget(
            self.label(
                f"{balance:.2f}",
                31,
                ACCENT,
                58,
                font="Georgia"
            )
        )

        layout.add_widget(
            self.label(
                f"Доходы: {income:.2f}     Расходы: {expenses:.2f}",
                13,
                TEXT,
                40
            )
        )

        layout.add_widget(
            self.make_button(
                "Добавить операцию",
                self.add_expense
            )
        )

        self.add_section_title(layout, "История операций")

        scroll = ScrollView()

        items = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))

        for index, item in enumerate(self.data["expenses"]):
            text = (
                f'{item["kind"].capitalize()}: '
                f'{item["amount"]:.2f}\n'
                f'{item["title"]}\n'
                "Нажми, чтобы удалить"
            )

            items.add_widget(
                self.make_button(
                    text,
                    lambda _, i=index: self.delete_expense(i),
                    75
                )
            )

        if not items.children:
            items.add_widget(
                self.label(
                    "Операций пока нет.",
                    14,
                    MUTED,
                    45
                )
            )

        scroll.add_widget(items)
        layout.add_widget(scroll)

    def add_expense(self, *_):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        title = self.make_input("Название операции")
        amount = self.make_input("Сумма")

        kind = "расход"

        kind_label = self.label(
            "Выбранный тип: расход",
            14,
            ACCENT,
            35
        )

        def choose_kind(value):
            nonlocal kind
            kind = value
            kind_label.text = "Выбранный тип: " + value

        box.add_widget(title)
        box.add_widget(amount)
        box.add_widget(kind_label)

        box.add_widget(
            self.make_button(
                "Доход",
                lambda *_: choose_kind("доход"),
                45
            )
        )

        box.add_widget(
            self.make_button(
                "Расход",
                lambda *_: choose_kind("расход"),
                45
            )
        )

        popup = self.make_popup(
            "Новая операция",
            box,
            (0.9, 0.75)
        )

        def save():
            try:
                value = float(amount.text.replace(",", "."))
                if value <= 0:
                    raise ValueError
            except ValueError:
                self.show_message(
                    "Ошибка",
                    "Введи корректную сумму."
                )
                return

            self.data["expenses"].insert(0, {
                "title": title.text.strip() or "Операция",
                "amount": value,
                "kind": kind
            })

            self.save_data()
            popup.dismiss()
            self.show_expenses()

        box.add_widget(
            self.make_button(
                "Сохранить",
                lambda *_: save()
            )
        )

        popup.open()

    def delete_expense(self, index):
        self.data["expenses"].pop(index)
        self.save_data()
        self.show_expenses()

    # =====================================
    # СОБЫТИЯ
    # =====================================

    def show_events(self):
        layout = self.page_layout(
            "Мои события",
            "Записывай важные даты и планы."
        )

        layout.add_widget(
            self.make_button(
                "Добавить событие",
                self.add_event
            )
        )

        scroll = ScrollView()

        items = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))

        for index, event in enumerate(self.data["events"]):
            text = (
                f'{event["title"]}\n'
                f'{event["date"]}\n'
                f'{event["details"]}\n'
                "Нажми, чтобы удалить"
            )

            items.add_widget(
                self.make_button(
                    text,
                    lambda _, i=index: self.delete_event(i),
                    90
                )
            )

        if not items.children:
            items.add_widget(
                self.label(
                    "Событий пока нет.\n"
                    "Добавь первое событие.",
                    14,
                    MUTED,
                    60
                )
            )

        scroll.add_widget(items)
        layout.add_widget(scroll)

    def add_event(self, *_):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        title = self.make_input("Название события")
        date = self.make_input("Дата и время")
        details = self.make_input(
            "Подробности",
            True,
            110
        )

        box.add_widget(title)
        box.add_widget(date)
        box.add_widget(details)

        popup = self.make_popup(
            "Новое событие",
            box,
            (0.9, 0.8)
        )

        def save():
            if not title.text.strip():
                self.show_message(
                    "Ошибка",
                    "Введи название события."
                )
                return

            self.data["events"].insert(0, {
                "title": title.text.strip(),
                "date": date.text.strip(),
                "details": details.text.strip()
            })

            self.save_data()
            popup.dismiss()
            self.show_events()

        box.add_widget(
            self.make_button(
                "Сохранить событие",
                lambda *_: save()
            )
        )

        popup.open()

    def delete_event(self, index):
        self.data["events"].pop(index)
        self.save_data()
        self.show_events()

    # =====================================
    # ЖЕЛАНИЯ
    # =====================================

    def show_wishes(self):
        layout = self.page_layout(
            "Мои желания",
            "Собирай идеи и мечты в одном списке."
        )

        layout.add_widget(
            self.make_button(
                "Добавить желание",
                self.add_wish
            )
        )

        scroll = ScrollView()

        items = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))

        for index, wish in enumerate(self.data["wishes"]):
            items.add_widget(
                self.make_button(
                    wish + "\nНажми, чтобы удалить",
                    lambda _, i=index: self.delete_wish(i),
                    65
                )
            )

        if not items.children:
            items.add_widget(
                self.label(
                    "Список пока пуст.\n"
                    "Добавь то, о чём мечтаешь.",
                    14,
                    MUTED,
                    65
                )
            )

        scroll.add_widget(items)
        layout.add_widget(scroll)

    def add_wish(self, *_):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        wish = self.make_input("Моё желание")
        box.add_widget(wish)

        popup = self.make_popup(
            "Новое желание",
            box,
            (0.88, 0.4)
        )

        def save():
            if wish.text.strip():
                self.data["wishes"].append(wish.text.strip())
                self.save_data()
                popup.dismiss()
                self.show_wishes()

        box.add_widget(
            self.make_button(
                "Сохранить",
                lambda *_: save()
            )
        )

        popup.open()

    def delete_wish(self, index):
        self.data["wishes"].pop(index)
        self.save_data()
        self.show_wishes()

    # =====================================
    # ФОТОСТУДИЯ
    # =====================================

    def show_photo_studio(self):
        layout = self.page_layout(
            "Фотостудия",
            "Редактируй фотографии и сохраняй результат."
        )

        layout.add_widget(
            self.make_button(
                "Выбрать фотографию",
                self.choose_photo
            )
        )

        layout.add_widget(
            self.make_button(
                "Сделать светлее",
                lambda *_: self.edit_photo("bright"),
                48
            )
        )

        layout.add_widget(
            self.make_button(
                "Увеличить контраст",
                lambda *_: self.edit_photo("contrast"),
                48
            )
        )

        layout.add_widget(
            self.make_button(
                "Эффект сепия",
                lambda *_: self.edit_photo("sepia"),
                48
            )
        )

        layout.add_widget(
            self.make_button(
                "Повернуть фотографию",
                lambda *_: self.edit_photo("rotate"),
                48
            )
        )

        layout.add_widget(
            self.make_button(
                "Сохранить фотографию",
                self.save_photo
            )
        )

        self.photo_preview = Image(
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )

        layout.add_widget(self.photo_preview)

    def choose_photo(self, *_):
        chooser = FileChooserListView(
            filters=["*.png", "*.jpg", "*.jpeg", "*.webp"],
            path=os.path.expanduser("~")
        )

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8)
        )

        box.add_widget(chooser)

        popup = self.make_popup(
            "Выбор фотографии",
            box,
            (0.95, 0.9)
        )

        def select():
            if chooser.selection:
                self.current_photo = chooser.selection[0]
                self.edited_photo = self.current_photo

                self.photo_preview.source = self.current_photo
                self.photo_preview.reload()

                popup.dismiss()

        box.add_widget(
            self.make_button(
                "Выбрать",
                lambda *_: select()
            )
        )

        popup.open()

    def edit_photo(self, effect):
        if not self.current_photo:
            self.show_message(
                "Фотостудия",
                "Сначала выбери фотографию."
            )
            return

        try:
            from PIL import Image as PILImage
            from PIL import ImageEnhance

            img = PILImage.open(
                self.edited_photo or self.current_photo
            ).convert("RGB")

            if effect == "bright":
                img = ImageEnhance.Brightness(img).enhance(1.2)

            elif effect == "contrast":
                img = ImageEnhance.Contrast(img).enhance(1.25)

            elif effect == "sepia":
                pixels = img.load()

                for y in range(img.height):
                    for x in range(img.width):
                        r, g, b = pixels[x, y]

                        pixels[x, y] = (
                            min(255, int(
                                r * 0.393 + g * 0.769 + b * 0.189
                            )),
                            min(255, int(
                                r * 0.349 + g * 0.686 + b * 0.168
                            )),
                            min(255, int(
                                r * 0.272 + g * 0.534 + b * 0.131
                            ))
                        )

            elif effect == "rotate":
                img = img.rotate(90, expand=True)

            os.makedirs("edited_photos", exist_ok=True)

            path = os.path.join(
                "edited_photos",
                "current_edit.jpg"
            )

            img.save(path, quality=95)

            self.edited_photo = path
            self.photo_preview.source = path
            self.photo_preview.reload()

        except ImportError:
            self.show_message(
                "Ошибка",
                "Установи Pillow командой:\n"
                "python -m pip install pillow"
            )

        except Exception as error:
            self.show_message("Ошибка", str(error))

    def save_photo(self, *_):
        if not self.edited_photo:
            self.show_message(
                "Фотостудия",
                "Сначала выбери фотографию."
            )
            return

        try:
            from PIL import Image as PILImage

            os.makedirs("edited_photos", exist_ok=True)

            img = PILImage.open(self.edited_photo)

            filename = datetime.now().strftime(
                "photo_%Y%m%d_%H%M%S.jpg"
            )

            path = os.path.join("edited_photos", filename)

            img.save(path, quality=95)

            self.show_message(
                "Готово",
                "Фотография сохранена в папке edited_photos."
            )

        except Exception as error:
            self.show_message("Ошибка", str(error))


if __name__ == "__main__":
    SpotySaw().run()