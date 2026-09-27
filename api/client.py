from __future__ import annotations

import aiohttp

from .exceptions import GApiBadRequest, GApiForbidden, GApiNotFound, GApiUnavailable
from .models import DaySchedule, HeartbeatLog, WeekType


class GApiClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> GApiClient:
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def close(self):
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def _get(self, path: str, params: dict | None = None):
        if self._session is None:
            self._session = aiohttp.ClientSession()

        params = {k: v for k, v in (params or {}).items() if v is not None}

        try:
            async with self._session.get(
                f"{self._base_url}{path}", params=params
            ) as response:
                if response.status in (401, 403):
                    raise GApiForbidden(f"Доступ к {path} закрыт")

                if response.status == 429:
                    raise GApiUnavailable("Превышен лимит запросов, попробуй чуть позже")

                if response.status == 404:
                    body = await self._safe_json(response)
                    raise GApiNotFound(self._error_message(body, "Ничего не найдено"))

                if response.status == 400:
                    body = await self._safe_json(response)
                    raise GApiBadRequest(self._error_message(body, "Некорректный запрос"))

                if response.status >= 500:
                    raise GApiUnavailable("G-API сейчас недоступен")

                return await response.json()
        except aiohttp.ClientError as e:
            raise GApiUnavailable("Не удалось связаться с G-API") from e

    @staticmethod
    async def _safe_json(response: aiohttp.ClientResponse):
        try:
            return await response.json()
        except (aiohttp.ContentTypeError, ValueError):
            return {}

    @staticmethod
    def _error_message(body: dict, fallback: str) -> str:
        if isinstance(body, dict) and "error" in body:
            return body["error"]
        return fallback

    async def get_groups(self) -> list[str]:
        return await self._get("/api/groups")

    async def get_groups_by_department(self) -> dict[str, list[str]]:
        return await self._get("/api/groups/departments")

    async def find_department(self, group: str) -> str:
        return await self._get("/api/groups/find-department", {"group": group})

    async def get_department_names(self) -> list[str]:
        return await self._get("/api/groups/department-names")

    async def get_teachers(self) -> list[str]:
        return await self._get("/api/teachers")

    async def get_subjects(self) -> list[str]:
        return await self._get("/api/subjects")

    async def get_rooms(self) -> list[str]:
        return await self._get("/api/rooms")

    async def get_current_week_type(self) -> WeekType:
        data = await self._get("/api/schedule/current-weektype")
        return WeekType(data["weekType"])

    async def get_schedule(
        self, group: str | None = None, date: str | None = None
    ) -> dict[str, DaySchedule]:
        data = await self._get("/api/schedule", {"group": group, "date": date})
        if group:
            return {group: DaySchedule.from_json(data)}
        return {g: DaySchedule.from_json(v) for g, v in data.items()}

    async def get_schedule_for_group(self, group: str, offset: str) -> DaySchedule:
        data = await self._get(f"/api/schedule/{offset}", {"group": group})
        return DaySchedule.from_json(data)

    async def get_admin_snapshots(self) -> list[dict]:
        return await self._get("/api/admin/snapshots")

    async def get_admin_snapshot(self, snapshot_id: int) -> dict:
        return await self._get(f"/api/admin/snapshots/{snapshot_id}")

    async def get_heartbeat_latest(self) -> HeartbeatLog:
        data = await self._get("/api/admin/heartbeat/latest")
        return HeartbeatLog.from_json(data)

    async def get_heartbeat_logs(self, limit: int = 20) -> list[HeartbeatLog]:
        data = await self._get("/api/admin/heartbeat/logs", {"limit": limit})
        return [HeartbeatLog.from_json(item) for item in data]

    async def get_heartbeat_dates(self) -> list[str]:
        return await self._get("/api/admin/heartbeat/dates")

    async def get_parser_change_date(self) -> str:
        return await self._get("/api/admin/parser/change-date")
