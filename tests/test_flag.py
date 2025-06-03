from unittest.mock import patch

from pytest import raises

from python_flaggle import Flag, FlagOperation, FlagType


class TestFlagType:
    def test_from_value_boolean(self):
        assert FlagType.from_value(True) == FlagType.BOOLEAN
        assert FlagType.from_value(False) == FlagType.BOOLEAN

    def test_from_value_string(self):
        assert FlagType.from_value("test") == FlagType.STRING
        assert FlagType.from_value("") == FlagType.EMPTY

    def test_from_value_numeric(self):
        assert FlagType.from_value(42) == FlagType.INTEGER
        assert FlagType.from_value(3.14) == FlagType.FLOAT

    def test_from_value_array(self):
        assert FlagType.from_value([42, 69]) == FlagType.ARRAY
        assert FlagType.from_value(["BR", "PT"]) == FlagType.ARRAY
        assert FlagType.from_value([]) == FlagType.ARRAY

    def test_from_value_null(self):
        assert FlagType.from_value(None) == FlagType.NULL

    def test_from_value_unsupported(self):
        with raises(TypeError):
            FlagType.from_value({})
            FlagType.from_value(set())

    def test_str_repr(self):
        assert str(FlagType.BOOLEAN) == "boolean"
        assert str(FlagType.STRING) == "string"
        assert str(FlagType.INTEGER) == "integer"
        assert str(FlagType.FLOAT) == "float"
        assert str(FlagType.NULL) == "null"
        assert str(FlagType.ARRAY) == "array"
        assert str(FlagType.EMPTY) == ""


class TestFlagOperation:
    def test_from_string_valid(self):
        assert FlagOperation.from_string("EQ") == FlagOperation.EQ
        assert FlagOperation.from_string("NE") == FlagOperation.NE
        assert FlagOperation.from_string("GT") == FlagOperation.GT
        assert FlagOperation.from_string("GE") == FlagOperation.GE
        assert FlagOperation.from_string("LT") == FlagOperation.LT
        assert FlagOperation.from_string("LE") == FlagOperation.LE
        assert FlagOperation.from_string("IN") == FlagOperation.IN
        assert FlagOperation.from_string("NI") == FlagOperation.NI
        assert FlagOperation.from_string("eq") == FlagOperation.EQ
        assert FlagOperation.from_string("ne") == FlagOperation.NE
        assert FlagOperation.from_string("gt") == FlagOperation.GT
        assert FlagOperation.from_string("ge") == FlagOperation.GE
        assert FlagOperation.from_string("lt") == FlagOperation.LT
        assert FlagOperation.from_string("le") == FlagOperation.LE
        assert FlagOperation.from_string("in") == FlagOperation.IN
        assert FlagOperation.from_string("ni") == FlagOperation.NI

    def test_from_string_invalid(self):
        with raises(ValueError):
            FlagOperation.from_string("invalid")
            FlagOperation.from_string("")

    def test_eq_ne_operations(self):
        assert FlagOperation.EQ(6, 6) is True
        assert FlagOperation.EQ(6, 6.0) is True
        assert FlagOperation.EQ(6, 9) is False
        assert FlagOperation.EQ("test", "test") is True
        assert FlagOperation.EQ("test", "") is False
        assert FlagOperation.EQ(["test", "test"], ["test", "test"]) is True
        assert FlagOperation.EQ(["test", "test"], ["test", ""]) is False

        assert FlagOperation.NE(6, 6) is False
        assert FlagOperation.NE(6, 6.0) is False
        assert FlagOperation.NE(6, 9) is True
        assert FlagOperation.NE("test", "test") is False
        assert FlagOperation.NE("test", "") is True
        assert FlagOperation.NE(["test", "test"], ["test", "test"]) is False
        assert FlagOperation.NE(["test", "test"], ["test", ""]) is True

    def test_gt_ge_lt_le_operations(self):
        assert FlagOperation.GT(6, 6) is False
        assert FlagOperation.GT(6, 9) is False
        assert FlagOperation.GT(9, 6) is True

        assert FlagOperation.GE(6, 6) is True
        assert FlagOperation.GE(6, 9) is False
        assert FlagOperation.GE(9, 6) is True

        assert FlagOperation.LT(6, 6) is False
        assert FlagOperation.LT(6, 9) is True
        assert FlagOperation.LT(9, 6) is False

        assert FlagOperation.LE(6, 6) is True
        assert FlagOperation.LE(6, 9) is True
        assert FlagOperation.LE(9, 6) is False

    def test_in_ni_operations(self):
        assert FlagOperation.IN(6, [6, 9]) is True
        assert FlagOperation.IN(9, [6]) is False
        assert FlagOperation.IN("foo", ["foo", "bar"]) is True
        assert FlagOperation.IN("bar", ["foo"]) is False

        assert FlagOperation.NI(6, [6, 9]) is False
        assert FlagOperation.NI(9, [6]) is True
        assert FlagOperation.NI("foo", ["foo", "bar"]) is False
        assert FlagOperation.NI("bar", ["foo"]) is True


class TestFlag:
    def test_init_boolean(self):
        flag = Flag(name="booleantest", description="a boolean test", value=True)

        assert flag.name == "booleantest"
        assert flag.description == "a boolean test"
        assert flag.value is True
        assert flag.status is True
        assert flag.is_enabled() is True

    def test_init_numeric(self):
        flag = Flag(
            name="numerictest",
            description="a numeric test",
            value=69,
            operation=FlagOperation.EQ,
        )

        assert flag.name == "numerictest"
        assert flag.description == "a numeric test"
        assert flag.value == 69
        assert flag.status is True
        assert flag.is_enabled(69) is True
        assert flag.is_enabled(42) is False

    def test_init_string(self):
        flag = Flag(
            name="stringtest",
            description="a string test",
            value="test",
            operation=FlagOperation.EQ,
        )

        assert flag.name == "stringtest"
        assert flag.description == "a string test"
        assert flag.value == "test"
        assert flag.status is True
        assert flag.is_enabled("test") is True
        assert flag.is_enabled("different_test") is False

    def test_init_array(self):
        flag = Flag(
            name="arraytest",
            description="a array test",
            value=["foo", "bar"],
            operation=FlagOperation.IN,
        )

        assert flag.name == "arraytest"
        assert flag.description == "a array test"
        assert flag.value == ["foo", "bar"]
        assert flag.status is True
        assert flag.is_enabled("foo") is True
        assert flag.is_enabled("baz") is False

    def test_flag_str_repr(self):
        flag = Flag(
            name="test",
            description="a test",
            value="test",
            operation=FlagOperation.EQ,
        )

        assert str(flag) == 'Flag(name="test", description="a test", status="True")'

    def test_flag_equality(self):
        flag1 = Flag(
            name="test",
            description="a test",
            value="test",
            operation=FlagOperation.EQ,
        )
        flag2 = Flag(
            name="test",
            description="a test",
            value="test",
            operation=FlagOperation.EQ,
        )
        flag3 = Flag(
            name="differenttest",
            description="a different test",
            value="test",
            operation=FlagOperation.NE,
        )

        assert flag1 == flag2
        assert flag1 != flag3

        assert flag1.__eq__(42) is NotImplemented

    def test_status_boolean(self):
        assert Flag("test", True).status is True
        assert Flag("test", False).status is False

    def test_status_numeric(self):
        assert Flag("test", 1).status is True
        assert Flag("test", 0.1).status is True
        assert Flag("test", 0).status is False
        assert Flag("test", 0.0).status is False

    def test_status_string(self):
        assert Flag("test", "active").status is True
        assert Flag("test", "").status is False
        assert Flag("test", None).status is False

    def test_is_enabled_no_operation(self):
        assert Flag("test", "active").is_enabled("anything") is True

    def test_is_enable_positives(self):
        assert Flag("testint", 1).is_enabled() is True
        assert (
            Flag("testintoperation", 1, operation=FlagOperation.EQ).is_enabled(1)
            is True
        )

        assert Flag("testfloat", 1.1).is_enabled() is True
        assert (
            Flag("testfloatoperation", 3.14, operation=FlagOperation.LE).is_enabled(
                2.72
            )
            is True
        )

        assert Flag("teststr", "test").is_enabled() is True
        assert (
            Flag("teststroperation", "test", operation=FlagOperation.NE).is_enabled(
                "anothertest"
            )
            is True
        )

        assert Flag("testarray", ["test"]).is_enabled() is True
        assert (
            Flag("testarrayoperation", ["test"], operation=FlagOperation.IN).is_enabled(
                "test"
            )
            is True
        )

    def test_is_enable_negatives(self):
        assert Flag("testint", 0).is_enabled() is False

        assert Flag("testfloat", 0.0).is_enabled() is False

        assert Flag("teststr", "").is_enabled() is False

        assert Flag("testnull", None).is_enabled() is False

        assert Flag("testarray", []).is_enabled() is False

    def test_from_json(self):
        json_data = {
            "flags": [
                {
                    "name": "test",
                    "description": "a test",
                    "value": "testflag",
                    "operation": "eq",
                }
            ]
        }

        flags = Flag.from_json(json_data)
        assert flags["test"].name == "test"
        assert flags["test"].description == "a test"
        assert flags["test"].value == "testflag"
        assert flags["test"].status is True
        assert flags["test"].is_enabled("testflag") is True
        assert flags["test"].is_enabled("different_test") is False

    def test_from_json_invalid(self):
        json_data = {
            "flags": {
                "name": "test",
                "description": "a test",
                "value": "testflag",
                "operation": "eq",
            }
        }

        with raises(ValueError):
            Flag.from_json(json_data)

    def test_from_json_empty(self):
        json_data = {}

        with raises(ValueError):
            Flag.from_json(json_data)

    def test_from_json_no_flag_name(self):
        json_data = {
            "flags": [
                {
                    "description": "a test",
                    "value": "testflag",
                    "operation": "eq",
                }
            ]
        }

        with patch("python_flaggle.flag.logger.warning") as mock_warning:
            flag = Flag.from_json(json_data)
            assert flag == {}
            mock_warning.assert_called_once_with("Found flag without name, skipping")

    def test_from_json_invalid_json_data(self):
        json_data = {
            "flags": [
                {
                    "name": "test",
                    "description": "a test",
                    "value": "testflag",
                    "operation": 123,
                }
            ]
        }

        with raises(ValueError) as exc_info:
            Flag.from_json(json_data)
        assert "Invalid JSON data" in str(exc_info)

    def test_is_enabled_else_branch(self):
        class DummyFlag(Flag):
            def __init__(self):
                # Set a fake type to trigger the 'else' branch
                self._flag_type = "UNKNOWN_TYPE"
                self._name = "dummy"
                self._value = "irrelevant"
                self._description = None
                self._operation = None

        flag = DummyFlag()
        assert flag.is_enabled() is False
