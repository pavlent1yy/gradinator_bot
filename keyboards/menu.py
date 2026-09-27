from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import MenuAction, ScheduleOffset


def main_menu(has_group: bool) -> InlineKeyboardMarkup:
    is_sunday = date.today().weekday() == 6

    actual_offset = "tomorrow" if is_sunday else "today"

    rows = [
        [
            InlineKeyboardButton(
                text="📅 Актуальное расписание",
                callback_data=ScheduleOffset(offset=actual_offset).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Вчера",
                callback_data=ScheduleOffset(offset="yesterday").pack(),
            ),
            InlineKeyboardButton(
                text="Завтра ➡️",
                callback_data=ScheduleOffset(offset="tomorrow").pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗓 Тип недели",
                callback_data=MenuAction(action="weektype").pack(),
            ),
            InlineKeyboardButton(
                text="📚 Справочники",
                callback_data=MenuAction(action="reference").pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔄 Сменить группу" if has_group else "🏫 Выбрать группу",
                callback_data=MenuAction(action="pick_group").pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="◀️ В меню",
                    callback_data=MenuAction(action="home").pack(),
                )
            ]
        ]
    )