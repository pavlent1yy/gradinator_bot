from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import MenuAction, RefPage

REF_LABELS = {"teachers": "👤 Преподаватели", "subjects": "📖 Предметы", "rooms": "🚪 Аудитории"}


def reference_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=RefPage(kind=kind, page=0).pack())]
        for kind, label in REF_LABELS.items()
    ]
    rows.append(
        [InlineKeyboardButton(text="◀️ В меню", callback_data=MenuAction(action="home").pack())]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def reference_nav(kind: str, page: int, has_more: bool) -> InlineKeyboardMarkup:
    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(text="⬅️", callback_data=RefPage(kind=kind, page=page - 1).pack())
        )
    if has_more:
        nav.append(
            InlineKeyboardButton(text="➡️", callback_data=RefPage(kind=kind, page=page + 1).pack())
        )

    rows = [nav] if nav else []
    rows.append(
        [InlineKeyboardButton(text="◀️ Справочники", callback_data=MenuAction(action="reference").pack())]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)
