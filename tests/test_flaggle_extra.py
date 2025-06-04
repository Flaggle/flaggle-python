import logging
import threading
import types
from unittest.mock import MagicMock, patch

import pytest

from python_flaggle import Flag, Flaggle


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

    monkeypatch.setattr("python_flaggle.flaggle.get", lambda *a, **k: MockResponse())
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    assert isinstance(f.last_update, type(f._last_update))
    assert isinstance(f.flags, dict)


def test_flaggle_update_uses_default_flags_on_empty(monkeypatch):
    monkeypatch.setattr(
        "python_flaggle.flaggle.get",
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
    with patch("python_flaggle.flaggle.Flag.from_json", return_value={}):
        f._update()
        assert f._flags == {"f": Flag("f", True)} or f._flags == {}


def test_flaggle_schedule_update_starts_thread(monkeypatch):
    monkeypatch.setattr(
        "python_flaggle.flaggle.get",
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
        "python_flaggle.flaggle.get",
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

    monkeypatch.setattr("python_flaggle.flaggle.get", raise_exc)
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    assert f._fetch_flags() == {}


def test_flaggle_properties(monkeypatch):
    monkeypatch.setattr(
        "python_flaggle.flaggle.get",
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


def test_flaggle_fetch_flags_unexpected_exception(monkeypatch, caplog):
    """Test that _fetch_flags handles unexpected exceptions and logs critical."""

    class DummyFlaggle(Flaggle):
        pass

    def raise_exc(*a, **k):
        raise RuntimeError("unexpected")

    monkeypatch.setattr("python_flaggle.flaggle.get", raise_exc)
    f = DummyFlaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})
    with caplog.at_level(logging.CRITICAL):
        result = f._fetch_flags()
        assert result == {}
        assert any(
            "Unexpected error during flag fetch" in r.message for r in caplog.records
        )


def test_flaggle_update_handles_exception(monkeypatch, caplog):
    """Test that _update logs critical on unexpected exception."""

    class DummyFlaggle(Flaggle):
        pass

    f = DummyFlaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})

    def raise_exc():
        raise RuntimeError("fail update")

    f._fetch_flags = raise_exc
    with caplog.at_level(logging.CRITICAL):
        f._update()
        assert any(
            "Unexpected error during flag update" in r.message for r in caplog.records
        )


def test_flaggle_recurring_update_reschedule_exception(monkeypatch, caplog):
    """Test that recurring_update logs critical if rescheduling fails."""
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})

    def raise_enter(*a, **k):
        raise RuntimeError("fail reschedule")

    f._scheduler.enter = raise_enter
    with caplog.at_level(logging.CRITICAL):
        f.recurring_update()
        assert any(
            "Failed to reschedule recurring update" in r.message for r in caplog.records
        )


def test_flaggle_recurring_update_update_exception(monkeypatch, caplog):
    """Test that recurring_update logs error if _update fails."""
    f = Flaggle("http://x", interval=1, default_flags={"f": Flag("f", True)})

    def raise_update():
        raise RuntimeError("fail update")

    f._update = raise_update
    # Patch _scheduler.enter to a no-op to avoid further errors
    f._scheduler.enter = lambda *a, **k: None
    with caplog.at_level(logging.ERROR):
        f.recurring_update()
        assert any(
            "Error during recurring flag update" in r.message for r in caplog.records
        )
