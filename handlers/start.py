from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.callbacks import MenuAction
from keyboards.menu import main_menu
from storage import UserStorage

router = Router(name="start")

WELCOME = (
    "👋 <b>Gradinator</b> - бот расписания колледжа.\n\n"
    "Тут актуальное расписание, тип недели и справочники по преподавателям, "
    "предметам и аудиториям."
)


@router.message(CommandStart())
async def cmd_start(message: Message, storage: UserStorage):
    group = await storage.get_group(message.from_user.id)
    await message.answer(WELCOME, reply_markup=main_menu(has_group=bool(group)))


@router.callback_query(MenuAction.filter(F.action == "home"))
async def go_home(callback: CallbackQuery, storage: UserStorage):
    group = await storage.get_group(callback.from_user.id)
    await callback.message.edit_text(WELCOME, reply_markup=main_menu(has_group=bool(group)))
    await callback.answer()
