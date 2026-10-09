import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from api import GApiClient
from api.exceptions import (
    GApiBadRequest,
    GApiForbidden,
    GApiNotFound,
    GApiUnavailable,
)


async def make_api(handler):
    app = web.Application()
    app.router.add_get("/api/groups", handler)
    app.router.add_get("/api/groups/find-department", handler)

    server = TestServer(app)
    await server.start_server()

    return server, GApiClient(str(server.make_url("")))


@pytest.mark.parametrize(
    ("status", "exc"),
    [
        (400, GApiBadRequest),
        (401, GApiForbidden),
        (403, GApiForbidden),
        (404, GApiNotFound),
        (429, GApiUnavailable),
        (500, GApiUnavailable),
        (503, GApiUnavailable),
    ],
)
async def test_status_mapping(status, exc):
    async def handler(request):
        return web.Response(status=status)

    server, api = await make_api(handler)

    async with api:
        with pytest.raises(exc):
            await api.get_groups()

    await server.close()


async def test_error_message_from_body():
    async def handler(request):
        return web.json_response({"error": "Нет актуальных данных"}, status=404)

    server, api = await make_api(handler)

    async with api:
        with pytest.raises(GApiNotFound, match="Нет актуальных данных"):
            await api.get_groups()

    await server.close()


async def test_plain_text_response():
    async def handler(request):
        return web.Response(text="oit", content_type="text/html")

    server, api = await make_api(handler)

    async with api:
        assert await api.find_department("ИС1-21") == "oit"

    await server.close()


async def test_connection_error():
    api = GApiClient("http://127.0.0.1:1")

    async with api:
        with pytest.raises(GApiUnavailable):
            await api.get_groups()
