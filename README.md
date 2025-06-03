# Flaggle
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-flaggle)
![PyPI - Version](https://img.shields.io/pypi/v/python-flaggle)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Flaggle/flaggle-python/python-package.yml)

## Overview

Flaggle is a robust and flexible Python library for managing feature flags in your applications. With Flaggle, you can enable or disable features dynamically, perform gradual rollouts, and control feature availability without redeploying your code. Designed for simplicity and extensibility, Flaggle supports a variety of flag types and operations, making it easy to adapt to any project or workflow.

Whether you're building a small script or a large-scale production system, Flaggle helps you ship faster, experiment safely, and deliver value to your users with confidence.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Operations](#supported-operations)
- [Contributing](#contributing)
- [License](#license)
- [TODO / Roadmap](#todo--roadmap)

---

## Features
- Simple API for defining and evaluating feature flags
- Supports boolean, string, numeric, array, and null flag types
- Rich set of comparison operations (EQ, NE, GT, LT, IN, etc.)
- JSON-based flag configuration
- Easy integration with any Python application
- Thread-safe and production-ready

---

## Installation

Install from PyPI:

```bash
pip install python-flaggle
```

Or with Poetry:

```bash
poetry add python-flaggle
```

---

## Usage

### Basic Example

```python
from flaggle import Flaggle

# Create a Flaggle instance that fetches flags from a remote endpoint
flaggle = Flaggle(url="https://api.example.com/flags", interval=60)

# Access a flag by name and check if it is enabled
if flaggle.flags["feature_a"].is_enabled():
    print("Feature A is enabled!")

# Use a flag with a value and operation
if flaggle.flags["min_version"].is_enabled(4):
    print("Version is supported!")

# Check a string flag
if flaggle.flags["env"].is_enabled("production"):
    print("Production environment!")
```

### Manual Flag Creation (Advanced)

You can also create flags manually if you want to bypass remote fetching:

```python
from flaggle import Flag, FlagOperation

flag = Flag(name="feature_x", value=True)
if flag.is_enabled():
    print("Feature X is enabled!")

flag = Flag(name="min_version", value=2, operation=FlagOperation.GE)
if flag.is_enabled(3):
    print("Version is supported!")
```

---

## Supported Operations

Flaggle supports a variety of operations for evaluating feature flags. These operations can be used to control feature availability based on different types of values. Below are the supported operations, their descriptions, and usage examples:

| Operation | Description                                 | Example Usage                                  |
|-----------|---------------------------------------------|------------------------------------------------|
| EQ        | Equal to                                    | `FlagOperation.EQ(5, 5)` → `True`              |
| NE        | Not equal to                                | `FlagOperation.NE("a", "b")` → `True`         |
| GT        | Greater than                                | `FlagOperation.GT(10, 5)` → `True`             |
| GE        | Greater than or equal to                    | `FlagOperation.GE(5, 5)` → `True`              |
| LT        | Less than                                   | `FlagOperation.LT(3, 5)` → `True`              |
| LE        | Less than or equal to                       | `FlagOperation.LE(3, 3)` → `True`              |
| IN        | Value is in a list/array                    | `FlagOperation.IN("BR", ["BR", "US"])` → `True` |
| NI        | Value is not in a list/array                | `FlagOperation.NI("FR", ["BR", "US"])` → `True` |

### Usage in Flag

You can specify an operation when creating a `Flag` to control how the flag is evaluated:

```python
from flaggle import Flag, FlagOperation

# Numeric equality
flag = Flag(name="feature_x", value=42, operation=FlagOperation.EQ)
flag.is_enabled(42)  # True
flag.is_enabled(10)  # False

# String not equal
flag = Flag(name="env", value="prod", operation=FlagOperation.NE)
flag.is_enabled("dev")  # True
flag.is_enabled("prod") # False

# Membership in array
flag = Flag(name="region", value=["US", "BR"], operation=FlagOperation.IN)
flag.is_enabled("US")  # True
flag.is_enabled("FR")  # False
```

You can also use the string representation of operations when loading flags from JSON:

```python
json_data = {
    "flags": [
        {"name": "feature_x", "value": 42, "operation": "eq"},
        {"name": "env", "value": "prod", "operation": "ne"},
        {"name": "region", "value": ["US", "BR"], "operation": "in"}
    ]
}
flags = Flag.from_json(json_data)
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes, new features, or improvements. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## TODO / Roadmap

- [ ] **Customizable API Call Logic:** Allow users to provide their own HTTP client or customize how flags are fetched, instead of always using `requests.get`.
- [ ] **Pluggable Storage Backends:** Support for loading flags from sources other than HTTP endpoints (e.g., local files, databases, environment variables).
- [ ] **Flag Change Listeners:** Add hooks or callbacks to notify the application when a flag value changes.
- [ ] **Admin/Management UI:** Provide a web interface for managing and toggling flags in real time.
- [ ] **Advanced Rollout Strategies:** Support for percentage rollouts, user targeting, and A/B testing.
- [ ] **Async Support:** Add async/await support for non-blocking flag fetching and updates.
- [ ] **Type Annotations & Validation:** Improve type safety and validation for flag values and operations.
- [ ] **Better Error Handling & Logging:** More granular error reporting and logging options.
- [ ] **Extensive Documentation & Examples:** Expand documentation with more real-world usage patterns and advanced scenarios.

Contributions and suggestions are welcome! Please open an issue or pull request if you have ideas for improvements.