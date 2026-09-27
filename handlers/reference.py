from aiogram import F, Router
from aiogram.types import CallbackQuery

from api import GApiClient, GApiError
from keyboards.callbacks import MenuAction, RefPage
from keyboards.reference import REF_LABELS, reference_menu, reference_nav
from utils.formatting import format_string_list

router = Router(name="reference")

PAGE_SIZE = 15

FETCHERS = {
    "teachers": lambda api: api.get_teachers(),
    "subjects": lambda api: api.get_subjects(),
    "rooms": lambda api: api.get_rooms(),
}


@router.callback_query(MenuAction.filter(F.action == "reference"))
async def show_reference_menu(callback: CallbackQuery):
    await callback.message.edit_text("📚 Что показать?", reply_markup=reference_menu())
    await callback.answer()


@router.callback_query(RefPage.filter())
async def show_reference_page(callback: CallbackQuery, callback_data: RefPage, api: GApiClient):
    try:
        values = sorted(v for v in await FETCHERS[callback_data.kind](api) if v.strip())
    except GApiError as e:
        await callback.answer(str(e), show_alert=True)
        return

    start = callback_data.page * PAGE_SIZE
    chunk = values[start : start + PAGE_SIZE]
    has_more = start + PAGE_SIZE < len(values)

    label = REF_LABELS[callback_data.kind]
    page_info = f"{start + 1}–{start + len(chunk)} из {len(values)}"
    text = f"<b>{label}</b> ({page_info})\n\n{format_string_list(chunk)}"

    await callback.message.edit_text(
        text, reply_markup=reference_nav(callback_data.kind, callback_data.page, has_more)
    )
    await callback.answer()
