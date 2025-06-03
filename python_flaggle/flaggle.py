from datetime import datetime, timedelta, timezone
from logging import getLogger
from sched import scheduler
from threading import Thread
from time import sleep, time
from typing import Optional

from requests import RequestException, get

from python_flaggle.flag import Flag

logger = getLogger(__name__)


class Flaggle:
    def __init__(
        self,
        url: str,
        interval: int = 60,
        default_flags: Optional[dict] = None,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> None:
        self._url: str = url
        self._interval: int = interval
        self._timeout: int = timeout
        self._verify_ssl: bool = verify_ssl

        self._flags = default_flags or {}
        self._last_update = datetime.now(timezone.utc) - timedelta(seconds=interval)
        self._scheduler = scheduler(time, sleep)
        self._scheduler.thread = None  # type: ignore

        self._update()
        self._schedule_update()

    @property
    def flags(self) -> dict[str, list[dict[str, str]]]:
        """Returns the current flags."""
        return self._flags

    @property
    def last_update(self) -> datetime:
        """Returns the last update time of the flags."""
        return self._last_update

    @property
    def url(self) -> str:
        """Returns the URL from which flags are fetched."""
        return self._url

    @property
    def interval(self) -> int:
        """Returns the update interval in seconds."""
        return self._interval

    @property
    def timeout(self) -> int:
        """Returns the timeout for HTTP requests."""
        return self._timeout

    @property
    def verify_ssl(self) -> bool:
        """Returns whether SSL verification is enabled for HTTP requests."""
        return self._verify_ssl

    def _fetch_flags(self) -> dict[str, list[dict[str, str]]]:
        try:
            logger.info("Fetching flags from %s", self._url)
            response = get(self._url, timeout=self._timeout, verify=self._verify_ssl)
            response.raise_for_status()

            logger.info("Flags fetched successfully")
            logger.debug("Response content: %s", response.text)
            logger.warning("Response[%i]: %r", response.status_code, response.json())

            return Flag.from_json(response.json())
        except RequestException as e:
            print(f"Error fetching flags: {e}")
            return {}
        except (KeyError, ValueError):
            logger.error("Invalid response format: 'flags' key not found")
            return {}

    def _update(self) -> None:
        flags_data = self._fetch_flags()
        if flags_data:
            self._flags = flags_data
            self._last_update = datetime.now(timezone.utc)
            logger.info("Flags updated successfully")
            logger.debug("Current flags: %s", self._flags)

    def _schedule_update(self) -> None:
        def run_scheduler():
            self._scheduler.enter(self._interval, 1, self.recurring_update)
            self._scheduler.run()

        self._scheduler_thread = Thread(target=run_scheduler, daemon=True)
        self._scheduler_thread.start()

    def recurring_update(self) -> None:
        self._update()
        self._scheduler.enter(self._interval, 1, self.recurring_update)
