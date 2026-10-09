from datetime import date, timedelta

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from api import GApiClient, GApiError
from api.models import WeekType
from keyboards.callbacks import MenuAction, ScheduleOffset
from keyboards.menu import back_to_menu
from keyboards.schedule import schedule_nav
from storage import UserStorage
from utils.formatting import format_day_schedule


router = Router(name="schedule")

NO_GROUP_TEXT = "Сначала выбери группу 🏫"


async def _get_schedule(
    api: GApiClient,
    group: str,
    offset: str,
):
    today = date.today()

    offset_days = {
        "yesterday": -1,
        "today": 0,
        "tomorrow": 1,
    }

    target_date = today + timedelta(days=offset_days[offset])

    if target_date.weekday() == 6:
        target_date += timedelta(days=-1 if offset == "yesterday" else 1)

        return await api.get_schedule(
            group=group,
            date=target_date.isoformat(),
        )

    return await api.get_schedule_for_group(
        group,
        offset,
    )

@router.callback_query(ScheduleOffset.filter())
async def show_schedule(
    callback: CallbackQuery,
    callback_data: ScheduleOffset,
    api: GApiClient,
    storage: UserStorage,
):
    if date.today().weekday() == 6 and callback_data.offset == "today":
        try:
            await callback.answer()
        except TelegramBadRequest:
            pass
        return

    try:
        await callback.answer("Загружаю…")
    except TelegramBadRequest as e:
        if "query is too old" not in str(e):
            raise

    group = await storage.get_group(callback.from_user.id)

    if not group:
        await callback.message.edit_text(
            NO_GROUP_TEXT,
            reply_markup=back_to_menu(),
        )
        return

    try:
        day = await _get_schedule(
            api,
            group,
            callback_data.offset,
        )
    except GApiError as e:
        await callback.message.answer(str(e))
        return

    try:
        await callback.message.edit_text(
            format_day_schedule(day),
            reply_markup=schedule_nav(callback_data.offset),
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(MenuAction.filter(F.action == "weektype"))
async def show_weektype(
    callback: CallbackQuery,
    api: GApiClient,
):
    try:
        week_type = await api.get_current_week_type()
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    emoji = "🔵" if week_type is WeekType.NUMERATOR else "🟠"

    await callback.message.edit_text(
        f"🗓 <b>Тип недели</b>\n\n"
        f"{emoji} Сейчас <b>{week_type.label}</b>.",
        reply_markup=back_to_menu(),
    )
    await callback.answer()
