from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import MenuAction, ScheduleOffset


from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import MenuAction, ScheduleOffset


OFFSET_LABELS = {
    "yesterday": "⬅️ Вчера",
    "today": "📅 Сегодня",
    "tomorrow": "Завтра ➡️",
}


def schedule_nav(current: str) -> InlineKeyboardMarkup:
    is_sunday = date.today().weekday() == 6

    row = []

    for key, label in OFFSET_LABELS.items():
        if is_sunday and key == "today":
            row.append(
                InlineKeyboardButton(
                    text="⚪ Сегодня",
                    disabled={
                        "text": "⚪ Сегодня",
                    },
                )
            )
        else:
            row.append(
                InlineKeyboardButton(
                    text=(
                        f"• {label} •"
                        if key == current
                        else label
                    ),
                    callback_data=ScheduleOffset(offset=key).pack(),
                )
            )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row,
            [
                InlineKeyboardButton(
                    text="🔄 Сменить группу",
                    callback_data=MenuAction(action="pick_group").pack(),
                ),
                InlineKeyboardButton(
                    text="◀️ В меню",
                    callback_data=MenuAction(action="home").pack(),
                ),
            ],
        ]
    )