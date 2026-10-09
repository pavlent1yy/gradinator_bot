from api.models import DaySchedule
from utils.formatting import format_day_schedule


def make_day(pairs, week_type="DENOMINATOR"):
    return DaySchedule.from_json(
        {
            "group": "ИС1-21",
            "day": "Пятница",
            "weekType": week_type,
            "date": "2026-10-09",
            "pairs": pairs,
        }
    )


def cell(subject, teacher="Груздев В.В.", room="Б204"):
    return {"subjects": [subject], "teachers": [teacher], "rooms": [room]}


def test_day_shows_active_week_only():
    text = format_day_schedule(
        make_day(
            [
                {
                    "pairNumber": 1,
                    "numerator": cell("Математика"),
                    "denominator": cell("Физика"),
                    "hasChanges": False,
                }
            ]
        )
    )

    assert "ИС1-21" in text
    assert "Знаменатель" in text
    assert "Физика" in text
    assert "Математика" not in text


def test_pairs_sorted_by_number():
    text = format_day_schedule(
        make_day(
            [
                {"pairNumber": 3, "denominator": cell("Третья"), "hasChanges": False},
                {"pairNumber": 1, "denominator": cell("Первая"), "hasChanges": False},
            ]
        )
    )

    assert text.index("Первая") < text.index("Третья")


def test_empty_day():
    text = format_day_schedule(make_day([]))

    assert "Пар в этот день нет" in text


def test_day_with_only_other_week_pairs_is_empty():
    text = format_day_schedule(
        make_day(
            [{"pairNumber": 2, "numerator": cell("Архитектура"), "hasChanges": False}]
        )
    )

    assert "Пар в этот день нет" in text


def test_change_from_other_week_cell_is_shown_and_marked():
    text = format_day_schedule(
        make_day(
            [
                {
                    "pairNumber": 1,
                    "numerator": cell("Замена"),
                    "denominator": None,
                    "hasChanges": True,
                }
            ]
        )
    )

    assert "Замена" in text
    assert "❗️" in text


def test_html_is_escaped():
    text = format_day_schedule(
        make_day(
            [{"pairNumber": 1, "denominator": cell("<b>x</b>"), "hasChanges": False}]
        )
    )

    assert "&lt;b&gt;x&lt;/b&gt;" in text


def test_replacement_without_room_shows_only_subject():
    text = format_day_schedule(
        make_day(
            [
                {
                    "pairNumber": 0,
                    "denominator": cell("❕ Снято", "в предмете", ""),
                    "hasChanges": True,
                }
            ]
        )
    )

    assert "❕ Снято" in text
    assert "в предмете" not in text
    assert "🏫" not in text


def test_replacement_with_room():
    text = format_day_schedule(
        make_day(
            [
                {
                    "pairNumber": 1,
                    "denominator": cell("❗ 1,2 п/гр. Зубковская А.Е.", "в предмете", "Б501"),
                    "hasChanges": True,
                }
            ]
        )
    )

    assert "Зубковская" in text
    assert "в предмете" not in text
    assert "🏫 Б501" in text
