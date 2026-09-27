from aiogram.filters.callback_data import CallbackData


class MenuAction(CallbackData, prefix="menu"):
    action: str


class ScheduleOffset(CallbackData, prefix="sch"):
    offset: str


class DeptPick(CallbackData, prefix="dept"):
    name: str


class GroupPage(CallbackData, prefix="gpage"):
    dept: str
    page: int


class GroupPick(CallbackData, prefix="grp"):
    name: str


class RefPage(CallbackData, prefix="refpage"):
    kind: str
    page: int
