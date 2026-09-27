from __future__ import annotations

from html import escape

from api.models import CellData, DaySchedule, PairResponse, WeekType

WEEK_TYPE_EMOJI = {WeekType.NUMERATOR: "🔵", WeekType.DENOMINATOR: "🟠"}


def _truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text.ljust(width)
    return text[: width - 1].rstrip() + "…"


def _join(values: list[str]) -> str:
    return " / ".join(v for v in values if v) or "—"


def _active_cell(pair: PairResponse, week_type: WeekType) -> CellData | None:
    return pair.denominator if week_type is WeekType.DENOMINATOR else pair.numerator


def format_day_header(schedule: DaySchedule) -> str:
    emoji = WEEK_TYPE_EMOJI[schedule.week_type]
    return (
        f"<b>{escape(schedule.day)}, {escape(schedule.date)}</b>\n"
        f"{emoji} Неделя: <b>{schedule.week_type.label}</b> · Группа: <code>{escape(schedule.group)}</code>"
    )


def format_schedule_table(schedule: DaySchedule) -> str:
    rows = ["№  Предмет            Ауд   "]
    rows.append("─" * len(rows[0]))

    for pair in sorted(schedule.pairs, key=lambda p: p.pair_number):
        cell = _active_cell(pair, schedule.week_type)
        mark = "❗" if pair.has_changes else " "
        if cell is None or cell.is_empty:
            rows.append(f"{pair.pair_number:<2} {mark}окно")
            continue

        subject = _truncate(_join(cell.subjects), 18)
        room = _truncate(_join(cell.rooms), 5)
        rows.append(f"{pair.pair_number:<2}{mark}{subject} {room}")

    return "<pre>" + escape("\n".join(rows)) + "</pre>"


def format_teachers_line(schedule: DaySchedule) -> str:
    lines = []
    for pair in sorted(schedule.pairs, key=lambda p: p.pair_number):
        cell = _active_cell(pair, schedule.week_type)
        if cell is None or cell.is_empty or not cell.teachers:
            continue
        lines.append(f"<b>{pair.pair_number}.</b> {escape(_join(cell.teachers))}")

    if not lines:
        return ""

    return "\n".join(lines)


def format_day_schedule(schedule: DaySchedule) -> str:
    header = format_day_header(schedule)
    table = format_schedule_table(schedule)
    teachers = format_teachers_line(schedule)

    if not schedule.pairs:
        return f"{header}\n\n<i>Пар в этот день нет 🎉</i>"

    body = f"{header}\n\n{table}"

    if teachers:
        body += f"\n<blockquote expandable>👤 <b>Преподаватели</b>\n{teachers}</blockquote>"

    return body


def format_string_list(values: list[str]) -> str:
    return "\n".join(f"• <code>{escape(v)}</code>" for v in values)
