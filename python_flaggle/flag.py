from enum import Enum
from logging import getLogger
from traceback import format_exc
from typing import Any, Optional

logger = getLogger(__name__)


class FlagType(Enum):
    BOOLEAN: str = "boolean"
    STRING: str = "string"
    INTEGER: str = "integer"
    FLOAT: str = "float"
    NULL: str = "null"
    ARRAY: str = "array"
    EMPTY: str = ""

    def __str__(self):
        return self.value

    @classmethod
    def from_value(cls, value) -> "FlagType":
        if isinstance(value, bool):
            return cls.BOOLEAN
        elif isinstance(value, str):
            if value == "":
                return cls.EMPTY
            return cls.STRING
        elif isinstance(value, int):
            return cls.INTEGER
        elif isinstance(value, float):
            return cls.FLOAT
        elif isinstance(value, list):
            return cls.ARRAY
        elif value is None:
            return cls.NULL
        else:
            logger.error("Unsupported FlagType '%s'", type(value))
            logger.debug(format_exc())
            raise TypeError(f"Unsupported FlagType '{type(value)}'")


class FlagOperation(Enum):
    # fmt: off
    EQ = lambda first, second: first == second      # noqa: E731
    NE = lambda first, second: first != second      # noqa: E731
    GT = lambda first, second: first >  second      # noqa: E731
    GE = lambda first, second: first >= second      # noqa: E731
    LT = lambda first, second: first <  second      # noqa: E731
    LE = lambda first, second: first <= second      # noqa: E731
    IN = lambda first, second: first in second      # noqa: E731
    NI = lambda first, second: first not in second  # noqa: E731
    # fmt: on

    @classmethod
    def from_string(cls, operation: str) -> "FlagOperation":
        operation = operation.upper()

        try:
            return cls.__dict__[operation]
        except KeyError as exc:
            logger.error("Invalid Operation '%s'", operation)
            logger.debug(format_exc())
            raise ValueError(f"Invalid Operation '{operation}'") from exc


class Flag:
    def __init__(
        self,
        name: str,
        value,
        description: Optional[str] = None,
        operation: Optional[FlagOperation] = None,
    ):
        self._name: str = name
        self._value = value
        self._description: Optional[str] = description
        self._operation: Optional[FlagOperation] = operation

        self._flag_type: FlagType = FlagType.from_value(value=value)

    def __str__(self):
        return f'Flag(name="{self._name}", description="{self._description}", status="{self.status}")'

    def __eq__(self, other: "Flag") -> bool:
        if isinstance(other, Flag):
            return self._name == other._name and self._value == other._value
        return NotImplemented

    def __ne__(self, other: "Flag") -> bool:
        return not self.__eq__(other)

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> str:
        if self._flag_type not in (FlagType.NULL, FlagType.EMPTY):
            return bool(self._value)
        return False

    def is_enabled(self, other_value: Optional[Any] = None) -> bool:
        logger.debug(f"Flag {self._name} is of type {self._flag_type}")
        if self._flag_type == FlagType.BOOLEAN:
            return self._value
        elif self._flag_type in (
            FlagType.STRING,
            FlagType.INTEGER,
            FlagType.FLOAT,
            FlagType.ARRAY,
        ):
            if other_value is None or self._operation is None:
                logger.debug("No value to compare or operator not defined")
                return bool(self._value)
            return self._operation(other_value, self._value)
        elif self._flag_type in (FlagType.NULL, FlagType.EMPTY):
            return False
        else:
            return False

    @classmethod
    def from_json(cls: "Flag", data: dict) -> dict[str, "Flag"]:
        try:
            flags_data = data.get("flags")
            if flags_data is None or not isinstance(flags_data, list):
                raise ValueError("No flags in the provided JSON data")

            result = {}
            for flag_data in flags_data:
                name = flag_data.get("name")
                if not name:
                    logger.warning("Found flag without name, skipping")
                    continue

                value = flag_data.get("value")
                description = flag_data.get("description")

                operation_str = flag_data.get("operation")
                operation = None
                if operation_str:
                    operation = FlagOperation.from_string(operation_str)

                result[name] = cls(name, value, description, operation)

            return result

        except (KeyError, AttributeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc
