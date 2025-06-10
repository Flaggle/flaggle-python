# Configuration

Flaggle can be configured in several ways to fit your project's needs. This page covers the most common configuration patterns.

---

## Basic Configuration

Create a `Flaggle` instance and set flags in your application code:

```python
from python_flaggle import Flaggle
flaggle = Flaggle()
flaggle.set_flag("new_ui", True)
```

---

## Environment Variable Configuration

Set flags using environment variables for different environments (dev, staging, prod):

```python
import os
flaggle.set_flag("beta", os.getenv("BETA_FLAG", "off"))
```

---

## Configuration File Example

You can load flags from a config file (e.g., JSON, YAML):

```python
import json
from python_flaggle import Flaggle

with open("flags.json") as f:
    flags = json.load(f)

flaggle = Flaggle()
for name, value in flags.items():
    flaggle.set_flag(name, value)
```

---

## Tips
- Use environment variables for deployment-specific flags.
- Document your configuration for your team.
- See [Advanced Usage](advanced.md) for custom flag types and dynamic loading.