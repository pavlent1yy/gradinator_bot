from aiogram import Router

from . import groups, reference, schedule, start

router = Router(name="root")
router.include_router(start.router)
router.include_router(groups.router)
router.include_router(schedule.router)
router.include_router(reference.router)
