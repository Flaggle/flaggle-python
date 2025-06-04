# Flaggle
![PyPI - Version](https://img.shields.io/pypi/v/python-flaggle)
[![PyPI Downloads](https://static.pepy.tech/badge/python-flaggle)](https://pepy.tech/projects/python-flaggle)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Flaggle/flaggle-python/python-package.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-flaggle)

## Overview

Flaggle is a robust and flexible Python library for managing feature flags in your applications. Feature flags (also known as feature toggles) are a software development technique that allows you to enable or disable features dynamically, perform gradual rollouts, and control feature availability without redeploying your code. Designed for simplicity and extensibility, Flaggle supports a variety of flag types and operations, making it easy to adapt to any project or workflow.

Whether you're building a small script or a large-scale production system, Flaggle helps you ship faster, experiment safely, and deliver value to your users with confidence.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Flaggle Class: Configuration & Usage](#flaggle-class-configuration--usage)
- [Supported Operations](#supported-operations)
- [Advanced Usage: The Flag Class](#advanced-usage-the-flag-class)
- [JSON Schema for Flags Endpoint](#json-schema-for-flags-endpoint)
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

## Getting Started

The easiest way to use Flaggle is to create a `Flaggle` instance that fetches feature flags from a remote JSON endpoint. This is the recommended and most common usage pattern.

```python
from python_flaggle import Flaggle

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

---

## Flaggle Class: Configuration & Usage

The `Flaggle` class is the main entry point for using feature flags in your application. It is designed to periodically fetch flag definitions from a remote JSON endpoint and provide a simple API for evaluating those flags at runtime.

### Initialization

```python
from python_flaggle import Flaggle

flaggle = Flaggle(
    url="https://api.example.com/flags",   # Endpoint returning flag JSON
    interval=60,                            # Polling interval in seconds (default: 60)
    default_flags=None,                     # Optional: fallback flags if fetch fails
    timeout=10,                             # HTTP timeout in seconds (default: 10)
    verify_ssl=True                         # Verify SSL certificates (default: True)
)
```

#### Parameters
| Parameter       | Type    | Description                                                      |
|-----------------|---------|------------------------------------------------------------------|
| `url`           | str     | The HTTP(S) endpoint to fetch the flags JSON from                |
| `interval`      | int     | How often (in seconds) to poll for flag updates                  |
| `default_flags` | dict    | (Optional) Fallback flags if remote fetch fails                  |
| `timeout`       | int     | (Optional) HTTP request timeout in seconds (default: 10)         |
| `verify_ssl`    | bool    | (Optional) Whether to verify SSL certificates (default: True)     |

#### Properties
- `flags`: A dictionary of flag name to `Flag` object, always up-to-date with the latest fetched values.
- `last_update`: The last time the flags were updated.
- `url`, `interval`, `timeout`, `verify_ssl`: The configuration values used.

#### Example Usage

```python
# Check if a feature is enabled
if flaggle.flags["feature_a"].is_enabled():
    ...

# Evaluate a flag with a custom value (e.g., for numeric or string flags)
if flaggle.flags["min_version"].is_enabled(5):
    ...
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

---

## Advanced Usage: The Flag Class

For advanced scenarios, you can create and evaluate `Flag` objects directly, or load them from a JSON structure. This is useful for testing, custom flag sources, or when you want to bypass remote fetching.

### Manual Flag Creation

```python
from python_flaggle import Flag, FlagOperation

flag = Flag(name="feature_x", value=True)
if flag.is_enabled():
    print("Feature X is enabled!")

flag = Flag(name="min_version", value=2, operation=FlagOperation.GE)
if flag.is_enabled(3):
    print("Version is supported!")
```

### Loading Flags from JSON

```python
from python_flaggle import Flag

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

## JSON Schema for Flags Endpoint

The endpoint provided to `Flaggle` must return a JSON object with a top-level `flags` key, which is a list of flag definitions. Each flag definition should have the following structure:

```json
{
  "flags": [
    {
      "name": "feature_a",                // (string, required) Unique flag name
      "description": "Enable feature A",   // (string, optional) Human-readable description
      "value": true,                        // (any, required) The flag value (bool, str, int, float, list, or null)
      "operation": "eq"                    // (string, optional) Operation for evaluation (see below)
    },
    ...
  ]
}
```

### Supported Operations
- `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `in`, `ni`
- If `operation` is omitted, the flag is evaluated as a simple boolean/truthy value.

#### Example JSON
```json
{
  "flags": [
    {"name": "feature_a", "value": true},
    {"name": "min_version", "value": 3, "operation": "ge"},
    {"name": "region", "value": ["US", "BR"], "operation": "in"}
  ]
}
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
- [x] **Better Error Handling & Logging:** More granular error reporting and logging options.
- [x] **Extensive Documentation & Examples:** Expand documentation with more real-world usage patterns and advanced scenarios.

Contributions and suggestions are welcome! Please open an issue or pull request if you have ideas for improvements.