"""Flaggle: Feature flag management for Python applications.

This module provides the Flaggle class, which fetches and manages feature flags
from a remote JSON endpoint, enabling dynamic feature toggling and gradual rollouts.

Classes:
    Flaggle: Main class for fetching, updating, and evaluating feature flags.
"""

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
    """
    Main class for managing and evaluating feature flags in Python applications.

    Periodically fetches flag definitions from a remote JSON endpoint and provides
    a simple API for evaluating those flags at runtime.

    Attributes:
        _url (str): The endpoint URL to fetch flags from.
        _interval (int): Polling interval in seconds.
        _timeout (int): HTTP request timeout in seconds.
        _verify_ssl (bool): Whether to verify SSL certificates.
        _flags (dict): Dictionary of flag name to Flag object.
        _last_update (datetime): Last time the flags were updated.
        _scheduler (scheduler): Scheduler for periodic updates.
        _scheduler_thread (Thread): Background thread for the scheduler.

    Example:
        ```python
        flaggle = Flaggle(url="https://api.example.com/flags", interval=60)
        if flaggle.flags["feature_a"].is_enabled():
            print("Feature A is enabled!")
        ```
    """
    def __init__(
        self,
        url: str,
        interval: int = 60,
        default_flags: Optional[dict] = None,
        timeout: int = 10,
        verify_ssl: bool = True,
    ) -> None:
        """
        Initialize a Flaggle instance.

        Args:
            url (str): The HTTP(S) endpoint to fetch the flags JSON from.
            interval (int): How often (in seconds) to poll for flag updates.
            default_flags (dict, optional): Fallback flags if remote fetch fails.
            timeout (int): HTTP request timeout in seconds (default: 10).
            verify_ssl (bool): Whether to verify SSL certificates (default: True).
        """
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
        """
        Returns the current flags.

        Returns:
            dict[str, list[dict[str, str]]]: Dictionary of flag name to Flag object.
        """
        return self._flags

    @property
    def last_update(self) -> datetime:
        """
        Returns the last update time of the flags.

        Returns:
            datetime: The last time the flags were updated.
        """
        return self._last_update

    @property
    def url(self) -> str:
        """
        Returns the URL from which flags are fetched.

        Returns:
            str: The endpoint URL.
        """
        return self._url

    @property
    def interval(self) -> int:
        """
        Returns the update interval in seconds.

        Returns:
            int: Polling interval in seconds.
        """
        return self._interval

    @property
    def timeout(self) -> int:
        """
        Returns the timeout for HTTP requests.

        Returns:
            int: HTTP request timeout in seconds.
        """
        return self._timeout

    @property
    def verify_ssl(self) -> bool:
        """
        Returns whether SSL verification is enabled for HTTP requests.

        Returns:
            bool: True if SSL verification is enabled, False otherwise.
        """
        return self._verify_ssl

    def _fetch_flags(self) -> dict[str, list[dict[str, str]]]:
        """
        Fetch flags from the configured remote endpoint.

        Returns:
            dict[str, list[dict[str, str]]]: Dictionary of flag name to Flag object.
        Raises:
            RequestException: If the HTTP request fails.
            ValueError: If the response format is invalid.
        """
        try:
            logger.info("Fetching flags from %s", self._url)
            response = get(self._url, timeout=self._timeout, verify=self._verify_ssl)
            response.raise_for_status()
            logger.info("Flags fetched successfully from %s", self._url)
            logger.debug("Response content: %s", response.text)
            logger.debug("Response[%i]: %r", response.status_code, response.json())
            return Flag.from_json(response.json())
        except RequestException as e:
            logger.error("Error fetching flags from %s: %s", self._url, e, exc_info=True)
            return {}
        except ValueError as e:
            logger.error("Invalid response format from %s: %s", self._url, e, exc_info=True)
            return {}
        except Exception as e:
            logger.critical("Unexpected error during flag fetch: %s", e, exc_info=True)
            return {}

    def _update(self) -> None:
        """
        Update the internal flag dictionary by fetching the latest flags.
        """
        try:
            flags_data = self._fetch_flags()
            if flags_data:
                self._flags = flags_data
                self._last_update = datetime.now(timezone.utc)
                logger.info("Flags updated successfully at %s", self._last_update)
                logger.debug("Current flags: %s", self._flags)
            else:
                logger.warning("No flags data received; keeping previous flags.")
        except Exception as e:
            logger.critical("Unexpected error during flag update: %s", e, exc_info=True)

    def _schedule_update(self) -> None:
        """
        Start the background scheduler for periodic flag updates.
        """
        def run_scheduler():
            try:
                self._scheduler.enter(self._interval, 1, self.recurring_update)
                self._scheduler.run()
            except Exception as e:
                logger.critical("Scheduler thread encountered an error: %s", e, exc_info=True)

        self._scheduler_thread = Thread(target=run_scheduler, daemon=True)
        self._scheduler_thread.start()
        logger.info("Flag update scheduler started (interval=%s seconds)", self._interval)

    def recurring_update(self) -> None:
        """
        Periodically update flags at the configured interval.
        """
        try:
            self._update()
        except Exception as e:
            logger.error("Error during recurring flag update: %s", e, exc_info=True)
        finally:
            try:
                self._scheduler.enter(self._interval, 1, self.recurring_update)
            except Exception as e:
                logger.critical("Failed to reschedule recurring update: %s", e, exc_info=True)
