# First Steps

# Getting Started

Welcome to Flaggle! This guide will help you get up and running quickly.

---

## Installation

Install Flaggle using pip:

```bash
pip install python-flaggle
```

Or with Poetry:

```bash
poetry add python-flaggle
```

---

## Minimal Example

```python
from python_flaggle import Flaggle

flaggle = Flaggle()
flaggle.set_flag("new_ui", True)

if flaggle.is_enabled("new_ui"):
    print("The new UI is enabled!")
```

---

## Next Steps
- [Configuration](configuration.md)
- [API Reference](api/flaggle.md)
- [Integrations](integrations/fastapi.md)
- [Tips & FAQ](faq.md)

---

For more advanced usage, see the [Advanced Usage](advanced.md) section.