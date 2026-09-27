from aiogram import F, Router
from aiogram.types import CallbackQuery

from api import GApiClient, GApiError, GApiNotFound
from keyboards.callbacks import MenuAction, ScheduleOffset
from keyboards.menu import back_to_menu
from keyboards.schedule import schedule_nav
from storage import UserStorage
from utils.formatting import format_day_schedule

router = Router(name="schedule")

NO_GROUP_TEXT = "Сначала выбери группу 🏫"


@router.callback_query(ScheduleOffset.filter())
async def show_schedule(
    callback: CallbackQuery, callback_data: ScheduleOffset, api: GApiClient, storage: UserStorage
):
    group = await storage.get_group(callback.from_user.id)
    if not group:
        await callback.answer(NO_GROUP_TEXT, show_alert=True)
        return

    try:
        day = await api.get_schedule_for_group(group, callback_data.offset)
    except GApiNotFound as e:
        await callback.answer(str(e), show_alert=True)
        return
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    await callback.message.edit_text(
        format_day_schedule(day), reply_markup=schedule_nav(callback_data.offset)
    )
    await callback.answer()


@router.callback_query(MenuAction.filter(F.action == "weektype"))
async def show_week_type(callback: CallbackQuery, api: GApiClient):
    try:
        week_type = await api.get_current_week_type()
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    await callback.message.edit_text(
        f"🗓 Сейчас идёт: <b>{week_type.label}</b>", reply_markup=back_to_menu()
    )
    await callback.answer()
