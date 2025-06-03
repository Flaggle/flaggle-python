import threading
from unittest.mock import Mock, patch


from python_flaggle import Flag, Flaggle


class TestFlaggle:
    def test_init(self):
        with patch("python_flaggle.flaggle.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "flags": [{"name": "test_flag", "value": True}]
            }
            mock_get.return_value = mock_response

            flaggle = Flaggle(
                url="http://example.com/flags",
                interval=60,
                default_flags={"default_flag": Flag(name="default_flag", value=True)},
            )

            assert flaggle._url == "http://example.com/flags"
            assert flaggle._interval == 60

            mock_get.assert_called_once_with(
                "http://example.com/flags",
                timeout=10,
                verify=True,
            )
            assert flaggle.flags == {"test_flag": Flag(name="test_flag", value=True)}
            assert flaggle.last_update is not None
            assert flaggle.url == "http://example.com/flags"
            assert flaggle.interval == 60
            assert flaggle.timeout == 10
            assert flaggle.verify_ssl is True

            assert flaggle._scheduler is not None
            assert flaggle._scheduler.thread is None


class TestFlaggleComprehensive:
    def setup_method(self):
        self.default_flags = {"default_flag": Flag(name="default_flag", value=True)}
        self.url = "http://example.com/flags"
        self.flaggle = Flaggle(
            url=self.url,
            interval=1,
            default_flags=self.default_flags,
            timeout=5,
            verify_ssl=False,
        )

    def test_properties(self):
        assert self.flaggle.flags == self.flaggle._flags
        assert self.flaggle.last_update == self.flaggle._last_update
        assert self.flaggle.url == self.url
        assert self.flaggle.interval == 1
        assert self.flaggle.timeout == 5
        assert self.flaggle.verify_ssl is False

    def test_fetch_flags_success(self, monkeypatch):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"flags": [{"name": "flag1", "value": True}]}

            @property
            def status_code(self):
                return 200

            @property
            def text(self):
                return '{"flags": [{"name": "flag1", "value": true}]}'

        monkeypatch.setattr("python_flaggle.flaggle.get", lambda *a, **k: MockResponse())
        flags = self.flaggle._fetch_flags()
        assert "flag1" in flags

    def test_fetch_flags_http_error(self, monkeypatch):
        def raise_exc(*a, **k):
            from requests import RequestException

            raise RequestException("fail")

        monkeypatch.setattr("python_flaggle.flaggle.get", raise_exc)
        assert self.flaggle._fetch_flags() == {}

    def test_fetch_flags_key_error(self, monkeypatch):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"not_flags": []}

            @property
            def status_code(self):
                return 200

            @property
            def text(self):
                return "{}"

        monkeypatch.setattr("python_flaggle.flaggle.get", lambda *a, **k: MockResponse())
        assert self.flaggle._fetch_flags() == {}

    def test_update_with_data(self, monkeypatch):
        called = {}

        def mock_fetch():
            called["ok"] = True
            return {"flagx": Flag(name="flagx", value=True)}

        self.flaggle._fetch_flags = mock_fetch
        self.flaggle._update()
        assert called["ok"]
        assert "flagx" in self.flaggle.flags

    def test_update_no_data(self, monkeypatch):
        self.flaggle._fetch_flags = lambda: {}
        old_flags = self.flaggle._flags.copy()
        self.flaggle._update()
        assert self.flaggle._flags == old_flags

    def test_schedule_update_starts_thread(self):
        f = Flaggle(self.url, interval=1, default_flags=self.default_flags)
        assert hasattr(f, "_scheduler_thread")
        assert isinstance(f._scheduler_thread, threading.Thread)
        assert f._scheduler_thread.daemon

    def test_recurring_update_calls_update_and_schedules(self, monkeypatch):
        called = {"update": 0, "enter": 0}

        def fake_update():
            called["update"] += 1

        def fake_enter(*a, **k):
            called["enter"] += 1

        self.flaggle._update = fake_update
        self.flaggle._scheduler.enter = fake_enter
        self.flaggle.recurring_update()
        assert called["update"] == 1
        assert called["enter"] == 1

    def test_scheduler_thread_attribute(self):
        # _scheduler.thread is set to None in __init__, test it remains None
        assert self.flaggle._scheduler.thread is None
