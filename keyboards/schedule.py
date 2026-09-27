from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import MenuAction, ScheduleOffset

OFFSET_LABELS = {"yesterday": "⬅️ Вчера", "today": "📅 Сегодня", "tomorrow": "Завтра ➡️"}


def schedule_nav(current: str) -> InlineKeyboardMarkup:
    row = [
        InlineKeyboardButton(
            text=label if key != current else f"• {label} •",
            callback_data=ScheduleOffset(offset=key).pack(),
        )
        for key, label in OFFSET_LABELS.items()
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            row,
            [
                InlineKeyboardButton(
                    text="🔄 Сменить группу",
                    callback_data=MenuAction(action="pick_group").pack(),
                ),
                InlineKeyboardButton(
                    text="◀️ В меню", callback_data=MenuAction(action="home").pack()
                ),
            ],
        ]
    )
