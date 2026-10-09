from storage import UserStorage


async def test_set_get_clear(tmp_path):
    storage = UserStorage(str(tmp_path / "test.sqlite3"))
    await storage.init()

    assert await storage.get_group(1) is None

    await storage.set_group(1, "ИС1-21")
    assert await storage.get_group(1) == "ИС1-21"

    await storage.set_group(1, "ИС1-23")
    assert await storage.get_group(1) == "ИС1-23"

    await storage.clear_group(1)
    assert await storage.get_group(1) is None
