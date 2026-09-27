from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class WeekType(str, Enum):
    NUMERATOR = "NUMERATOR"
    DENOMINATOR = "DENOMINATOR"

    @property
    def label(self) -> str:
        return "Числитель" if self is WeekType.NUMERATOR else "Знаменатель"


@dataclass
class CellData:
    subjects: list[str] = field(default_factory=list)
    teachers: list[str] = field(default_factory=list)
    rooms: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not self.subjects and not self.teachers and not self.rooms

    @classmethod
    def from_json(cls, data: dict | None) -> CellData | None:
        if data is None:
            return None
        return cls(
            subjects=data.get("subjects", []),
            teachers=data.get("teachers", []),
            rooms=data.get("rooms", []),
        )


@dataclass
class PairResponse:
    pair_number: int
    numerator: CellData | None
    denominator: CellData | None
    has_changes: bool

    @classmethod
    def from_json(cls, data: dict) -> PairResponse:
        return cls(
            pair_number=data["pairNumber"],
            numerator=CellData.from_json(data.get("numerator")),
            denominator=CellData.from_json(data.get("denominator")),
            has_changes=data.get("hasChanges", False),
        )


@dataclass
class DaySchedule:
    group: str
    day: str
    week_type: WeekType
    date: str
    pairs: list[PairResponse]

    @classmethod
    def from_json(cls, data: dict) -> DaySchedule:
        return cls(
            group=data["group"],
            day=data["day"],
            week_type=WeekType(data["weekType"]),
            date=data["date"],
            pairs=[PairResponse.from_json(p) for p in data.get("pairs", [])],
        )


@dataclass
class HeartbeatLog:
    id: int
    started_at: str
    finished_at: str | None
    status: str
    message: str

    @classmethod
    def from_json(cls, data: dict) -> HeartbeatLog:
        return cls(
            id=data["id"],
            started_at=data["startedAt"],
            finished_at=data.get("finishedAt"),
            status=data["status"],
            message=data.get("message", ""),
        )
