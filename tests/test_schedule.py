from datetime import date

import pytest

from handlers import schedule


class FakeApi:
    def __init__(self):
        self.calls = []

    async def get_schedule(self, group, date=None):
        self.calls.append(("date", date))

    async def get_schedule_for_group(self, group, offset):
        self.calls.append(("offset", offset))


def freeze_today(monkeypatch, today):
    class FakeDate(date):
        @classmethod
        def today(cls):
            return today

    monkeypatch.setattr(schedule, "date", FakeDate)


@pytest.mark.parametrize(
    ("today", "offset", "expected"),
    [
        (date(2026, 10, 11), "today", ("date", "2026-10-12")),
        (date(2026, 10, 10), "tomorrow", ("date", "2026-10-12")),
        (date(2026, 10, 12), "yesterday", ("date", "2026-10-10")),
        (date(2026, 10, 9), "today", ("offset", "today")),
    ],
)
async def test_sunday_is_skipped(monkeypatch, today, offset, expected):
    freeze_today(monkeypatch, today)
    api = FakeApi()

    await schedule._get_schedule(api, "ИС1-21", offset)

    assert api.calls == [expected]
