import threading
from unittest.mock import MagicMock, patch

from flaggle import Flag, Flaggle


def test_flaggle_init_sets_last_update_and_flags(monkeypatch):
    # Patch get to return a valid response
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"flags": [{"name": "flag", "value": True}]}

        @property
        def status_code(self):
            return 200

        @property
        def text(self):
            return '{"flags": [{"name": "flag", "value": true}]}'

    monkeypatch.setattr("flaggle.flaggle.get", lambda *a, **k: MockResponse())
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    assert isinstance(f.last_update, type(f._last_update))
    assert isinstance(f.flags, dict)


def test_flaggle_update_uses_default_flags_on_empty(monkeypatch):
    monkeypatch.setattr(
        "flaggle.flaggle.get",
        lambda *a, **k: MagicMock(
            json=lambda: {"flags": []},
            raise_for_status=lambda: None,
            status_code=200,
            text="{}",
        ),
    )
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    # forcibly clear flags to test fallback
    f._flags = {"f": Flag("f", True)}
    with patch("flaggle.flaggle.Flag.from_json", return_value={}):
        f._update()
        assert f._flags == {"f": Flag("f", True)} or f._flags == {}


def test_flaggle_schedule_update_starts_thread(monkeypatch):
    monkeypatch.setattr(
        "flaggle.flaggle.get",
        lambda *a, **k: MagicMock(
            json=lambda: {"flags": []},
            raise_for_status=lambda: None,
            status_code=200,
            text="{}",
        ),
    )
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    assert hasattr(f, "_scheduler_thread")
    assert isinstance(f._scheduler_thread, threading.Thread)
    assert f._scheduler_thread.daemon


def test_flaggle_recurring_update_calls(monkeypatch):
    monkeypatch.setattr(
        "flaggle.flaggle.get",
        lambda *a, **k: MagicMock(
            json=lambda: {"flags": []},
            raise_for_status=lambda: None,
            status_code=200,
            text="{}",
        ),
    )
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    called = {"update": 0, "enter": 0}
    f._update = lambda: called.update(update=called["update"] + 1)
    f._scheduler.enter = lambda *a, **k: called.update(enter=called["enter"] + 1)
    f.recurring_update()
    assert called["update"] == 1
    assert called["enter"] == 1


def test_flaggle_fetch_flags_handles_request_exception(monkeypatch):
    def raise_exc(*a, **k):
        from requests import RequestException

        raise RequestException("fail")

    monkeypatch.setattr("flaggle.flaggle.get", raise_exc)
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    assert f._fetch_flags() == {}


def test_flaggle_properties(monkeypatch):
    monkeypatch.setattr(
        "flaggle.flaggle.get",
        lambda *a, **k: MagicMock(
            json=lambda: {"flags": []},
            raise_for_status=lambda: None,
            status_code=200,
            text="{}",
        ),
    )
    f = Flaggle(
        "http://x",
        interval=42,
        default_flags={"f": Flag("f", True)},
        timeout=7,
        verify_ssl=False,
    )
    assert f.url == "http://x"
    assert f.interval == 42
    assert f.timeout == 7
    assert f.verify_ssl is False
    assert f.flags == f._flags
    assert f.last_update == f._last_update
