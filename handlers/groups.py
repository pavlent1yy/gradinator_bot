from aiogram import F, Router
from aiogram.types import CallbackQuery

from api import GApiClient, GApiError
from keyboards.callbacks import DeptPick, GroupPage, GroupPick, MenuAction
from keyboards.groups import departments_keyboard, groups_keyboard
from keyboards.menu import back_to_menu
from storage import UserStorage

router = Router(name="groups")


@router.callback_query(MenuAction.filter(F.action == "pick_group"))
async def show_departments(callback: CallbackQuery, api: GApiClient):
    try:
        departments = await api.get_department_names()
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    await callback.message.edit_text(
        "🏫 Выбери отделение:", reply_markup=departments_keyboard(departments)
    )
    await callback.answer()


@router.callback_query(DeptPick.filter())
async def show_groups(callback: CallbackQuery, callback_data: DeptPick, api: GApiClient):
    try:
        by_dept = await api.get_groups_by_department()
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    groups = sorted(by_dept.get(callback_data.name, []))
    if not groups:
        await callback.answer("В этом отделении пока нет групп", show_alert=True)
        return

    await callback.message.edit_text(
        f"👥 Группы отделения <b>{callback_data.name.upper()}</b>:",
        reply_markup=groups_keyboard(callback_data.name, groups, page=0),
    )
    await callback.answer()


@router.callback_query(GroupPage.filter())
async def paginate_groups(callback: CallbackQuery, callback_data: GroupPage, api: GApiClient):
    try:
        by_dept = await api.get_groups_by_department()
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    groups = sorted(by_dept.get(callback_data.dept, []))

    await callback.message.edit_reply_markup(
        reply_markup=groups_keyboard(callback_data.dept, groups, page=callback_data.page)
    )
    await callback.answer()


@router.callback_query(GroupPick.filter())
async def pick_group(callback: CallbackQuery, callback_data: GroupPick, storage: UserStorage):
    await storage.set_group(callback.from_user.id, callback_data.name)
    await callback.message.edit_text(
        f"✅ Группа <b>{callback_data.name}</b> сохранена.",
        reply_markup=back_to_menu(),
    )
    await callback.answer("Готово")
