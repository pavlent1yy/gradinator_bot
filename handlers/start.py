from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.callbacks import MenuAction
from keyboards.menu import main_menu
from storage import UserStorage

router = Router(name="start")

WELCOME = (
    "👋 <b>GradInator</b> — мой неофициальный бот расписания ЯГК.\n\n"
    "📅 Я сделал его, чтобы тебе было проще смотреть актуальное расписание, "
    "тип недели и справочники по преподавателям, предметам и аудиториям.\n\n"
    "🌐 Если хочешь, можешь также заглянуть на мой сайт:\n"
    "<a href='https://gradinator.itsyoraaa.su'>gradinator.itsyoraaa.su</a>\n\n"
    "💻 А если интересно, то можешь глянуть, как я всё это дело реализовал:\n"
    "<b><a href='https://github.com/pavlent1yy/Gradinator'>сайт и система gradinator</a></b>\n"
    "<b><a href='https://github.com/pavlent1yy/gradinator_bot'>telegram-клиент для api</a></b>\n\n"
    "📦 Исходники моих проектов лежат на GitHub."
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
