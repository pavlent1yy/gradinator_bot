from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import DeptPick, GroupPage, GroupPick, MenuAction

PAGE_SIZE = 8


def departments_keyboard(departments: list[str]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=d.upper(), callback_data=DeptPick(name=d).pack())]
        for d in departments
    ]
    rows.append(
        [InlineKeyboardButton(text="◀️ В меню", callback_data=MenuAction(action="home").pack())]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def groups_keyboard(dept: str, groups: list[str], page: int) -> InlineKeyboardMarkup:
    start = page * PAGE_SIZE
    chunk = groups[start : start + PAGE_SIZE]

    rows = [
        [InlineKeyboardButton(text=g, callback_data=GroupPick(name=g).pack())]
        for g in chunk
    ]

    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton(
                text="⬅️", callback_data=GroupPage(dept=dept, page=page - 1).pack()
            )
        )
    if start + PAGE_SIZE < len(groups):
        nav.append(
            InlineKeyboardButton(
                text="➡️", callback_data=GroupPage(dept=dept, page=page + 1).pack()
            )
        )
    if nav:
        rows.append(nav)

    rows.append(
        [
            InlineKeyboardButton(
                text="◀️ Отделения", callback_data=MenuAction(action="pick_group").pack()
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)
