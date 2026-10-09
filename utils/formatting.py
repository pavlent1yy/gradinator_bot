from __future__ import annotations

from html import escape

from api.models import CellData, DaySchedule, PairResponse, WeekType


REPLACEMENT_TEACHER = "в предмете"

WEEK_TYPE_EMOJI = {
    WeekType.NUMERATOR: "🔵",
    WeekType.DENOMINATOR: "🟠",
}


def _join(values: list[str]) -> str:
    return ", ".join(value for value in values if value) or "—"


def _active_cell(
    pair: PairResponse,
    week_type: WeekType,
) -> CellData | None:
    active = (
        pair.numerator
        if week_type is WeekType.NUMERATOR
        else pair.denominator
    )

    if pair.has_changes:
        if active is not None and not active.is_empty:
            return active

        alternative = (
            pair.denominator
            if week_type is WeekType.NUMERATOR
            else pair.numerator
        )

        if alternative is not None and not alternative.is_empty:
            return alternative

    return active


def format_day_header(schedule: DaySchedule) -> str:
    week_emoji = WEEK_TYPE_EMOJI[schedule.week_type]

    return (
        "<b>// SCHEDULE</b> · "
        f"<code>{escape(schedule.group)}</code>\n"
        f"{escape(schedule.day)}, {escape(schedule.date)} · "
        f"{week_emoji} <b>{schedule.week_type.label}</b>"
    )


def format_pair(
    pair: PairResponse,
    week_type: WeekType,
) -> str | None:
    cell = _active_cell(pair, week_type)

    if cell is None or cell.is_empty:
        return None

    subject = _join(cell.subjects)
    teachers = _join(cell.teachers)
    rooms = _join(cell.rooms)

    first_line = (
        f"<b>{pair.pair_number:02}</b> │ "
        f"📚 {escape(subject)}"
    )

    if REPLACEMENT_TEACHER in cell.teachers:
        if not any(cell.rooms):
            return first_line

        return f"{first_line}\n   └─ 🏫 {escape(rooms)}"

    second_line = (
        f"   └─ 👤 {escape(teachers)} · "
        f"🏫 {escape(rooms)}"
    )

    if pair.has_changes:
        second_line += " ❗️"

    return f"{first_line}\n{second_line}"


def format_day_schedule(schedule: DaySchedule) -> str:
    header = format_day_header(schedule)

    pairs = [
        formatted
        for pair in sorted(
            schedule.pairs,
            key=lambda pair: pair.pair_number,
        )
        if (formatted := format_pair(pair, schedule.week_type))
    ]

    if not pairs:
        return (
            f"{header}\n\n"
            "<i>Пар в этот день нет 🎉</i>"
        )

    return f"{header}\n\n" + "\n\n".join(pairs)


def format_string_list(values: list[str]) -> str:
    return "\n".join(
        f"• <code>{escape(value)}</code>"
        for value in values
    )