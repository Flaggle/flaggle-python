"""Flag and flag operation definitions for the Flaggle library.

This module provides the Flag, FlagType, and FlagOperation classes for defining and evaluating feature flags.

Classes:
    FlagType: Enum representing supported flag value types.
    FlagOperation: Enum of supported flag comparison operations.
    Flag: Represents a single feature flag and its evaluation logic.
"""

from enum import Enum
from logging import getLogger
from traceback import format_exc
from typing import Any, Optional

logger = getLogger(__name__)


class FlagType(Enum):
    """Enumeration of supported flag value types.

    Attributes:
        BOOLEAN (str): Boolean flag type.
        STRING (str): String flag type.
        INTEGER (str): Integer flag type.
        FLOAT (str): Float flag type.
        NULL (str): Null flag type.
        ARRAY (str): Array/list flag type.
        EMPTY (str): Empty string flag type.
    """
    BOOLEAN: str = "boolean"
    STRING: str = "string"
    INTEGER: str = "integer"
    FLOAT: str = "float"
    NULL: str = "null"
    ARRAY: str = "array"
    EMPTY: str = ""

    def __str__(self) -> str:
        """Return the string value of the flag type."""
        return self.value

    @classmethod
    def from_value(cls, value: Any) -> "FlagType":
        """Infer the FlagType from a Python value.

        Args:
            value (Any): The value to infer the type from.

        Returns:
            FlagType: The inferred flag type.

        Raises:
            TypeError: If the value type is not supported.
        """
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
    """Enumeration of supported flag comparison operations.

    Each operation is a callable that takes two arguments and returns a boolean.

    Supported operations:
        EQ: Equal to
        NE: Not equal to
        GT: Greater than
        GE: Greater than or equal to
        LT: Less than
        LE: Less than or equal to
        IN: Value is in a list/array
        NI: Value is not in a list/array
    """
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
        """Get a FlagOperation from a string name (case-insensitive).

        Args:
            operation (str): The operation name (e.g., 'eq', 'gt').

        Returns:
            FlagOperation: The corresponding operation.

        Raises:
            ValueError: If the operation name is invalid.
        """
        operation = operation.upper()
        try:
            return cls.__dict__[operation]
        except KeyError as exc:
            logger.error("Invalid Operation '%s'", operation)
            logger.debug(format_exc())
            raise ValueError(f"Invalid Operation '{operation}'") from exc
        except Exception as exc:
            logger.critical("Unexpected error in FlagOperation.from_string: %s", exc, exc_info=True)
            raise


class Flag:
    """Represents a single feature flag and its evaluation logic.

    Attributes:
        name (str): The unique name of the flag.
        value (Any): The value of the flag (bool, str, int, float, list, or None).
        description (Optional[str]): Optional human-readable description.
        operation (Optional[FlagOperation]): Optional operation for evaluation.
        flag_type (FlagType): The inferred type of the flag value.
    """
    def __init__(
        self,
        name: str,
        value: Any,
        description: Optional[str] = None,
        operation: Optional[FlagOperation] = None,
    ):
        """Initialize a Flag instance.

        Args:
            name (str): The unique name of the flag.
            value (Any): The value of the flag.
            description (Optional[str]): Optional description.
            operation (Optional[FlagOperation]): Optional operation for evaluation.
        """
        self._name: str = name
        self._value = value
        self._description: Optional[str] = description
        self._operation: Optional[FlagOperation] = operation
        self._flag_type: FlagType = FlagType.from_value(value=value)

    def __str__(self) -> str:
        """Return a string representation of the flag."""
        return f'Flag(name="{self._name}", description="{self._description}", status="{self.status}")'

    def __eq__(self, other: "Flag") -> bool:
        """Check equality with another Flag instance."""
        if isinstance(other, Flag):
            return self._name == other._name and self._value == other._value
        return NotImplemented

    def __ne__(self, other: "Flag") -> bool:
        """Check inequality with another Flag instance."""
        return not self.__eq__(other)

    @property
    def name(self) -> str:
        """The unique name of the flag."""
        return self._name

    @property
    def value(self) -> Any:
        """The value of the flag."""
        return self._value

    @property
    def description(self) -> Optional[str]:
        """The human-readable description of the flag, if any."""
        return self._description

    @property
    def status(self) -> bool:
        """Whether the flag is considered enabled (truthy value).

        Returns:
            bool: True if the flag is enabled, False otherwise.
        """
        if self._flag_type not in (FlagType.NULL, FlagType.EMPTY):
            return bool(self._value)
        return False

    def is_enabled(self, other_value: Optional[Any] = None) -> bool:
        """Evaluate whether the flag is enabled, optionally comparing to another value.

        Args:
            other_value (Optional[Any]): Value to compare against the flag's value (for non-boolean flags).

        Returns:
            bool: True if the flag is enabled for the given value, False otherwise.

        Example:
            >>> flag = Flag(name="min_version", value=3, operation=FlagOperation.GE)
            >>> flag.is_enabled(4)
            True
        """
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
        """Create a dictionary of Flag objects from a JSON-like dictionary.

        Args:
            data (dict): The JSON data containing a 'flags' key with a list of flag definitions.

        Returns:
            dict[str, Flag]: A dictionary mapping flag names to Flag objects.

        Raises:
            ValueError: If the JSON data is invalid or missing required fields.

        Example:
            >>> json_data = {"flags": [{"name": "feature_x", "value": True}]}
            >>> flags = Flag.from_json(json_data)
            >>> flags["feature_x"].is_enabled()
            True
        """
        try:
            flags_data = data.get("flags")
            if flags_data is None or not isinstance(flags_data, list):
                logger.error("No flags in the provided JSON data: %r", data)
                raise ValueError("No flags in the provided JSON data")

            result = {}
            for flag_data in flags_data:
                name = flag_data.get("name")
                if not name:
                    logger.warning("Found flag without name, skipping: %r", flag_data)
                    continue

                value = flag_data.get("value")
                description = flag_data.get("description")

                operation_str = flag_data.get("operation")
                operation = None
                if operation_str:
                    try:
                        operation = FlagOperation.from_string(operation_str)
                    except Exception as exc:
                        logger.error("Invalid operation '%s' for flag '%s': %s", operation_str, name, exc, exc_info=True)
                        raise ValueError("Invalid JSON data: invalid operation") from exc

                result[name] = cls(name, value, description, operation)

            return result

        except (KeyError, AttributeError) as exc:
            logger.error("Invalid JSON data: %s", exc, exc_info=True)
            raise ValueError(f"Invalid JSON data: {exc}") from exc
        except Exception as exc:
            logger.critical("Unexpected error in Flag.from_json: %s", exc, exc_info=True)
            raise ValueError(f"Invalid JSON data: {exc}") from exc
