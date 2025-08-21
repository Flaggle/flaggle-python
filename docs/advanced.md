# Advanced Usage

This section covers advanced Flaggle features for power users and production deployments.

---

## Custom Flag Types

You can define custom flag types by subclassing `Flag` and registering them with `Flaggle`.

```python
from python_flaggle import Flag, Flaggle

class PercentageFlag(Flag):
    def is_enabled(self, context=None):
        # Enable for a percentage of users
        user_id = context.get("user_id")
        return hash(user_id) % 100 < self.value  # e.g., value=10 for 10%

flaggle = Flaggle()
flaggle.register_flag_type("percentage", PercentageFlag)
```

---

## Dynamic Flags

Flags can be loaded from a database, remote API, or environment variables.

```python
import os
from python_flaggle import Flaggle

flaggle = Flaggle()
flaggle.set_flag("new_ui", os.getenv("NEW_UI_FLAG", "off"))
```

---

## Environment-based Flags

Use environment variables or config files to control flag state per environment (dev, staging, prod).

```python
import os
flaggle.set_flag("beta", os.getenv("BETA_FLAG", "off"))
```

---

## User-based Flags

Pass user or request context to `is_enabled` for per-user or per-group toggles.

```python
flaggle.is_enabled("beta", context={"user_id": 123})
```

---

## Feature Rollouts & Experiments

- Use percentage or cohort-based flags for gradual rollouts.
- Combine multiple flag types for complex experiments.

---

## Best Practices
- Remove unused flags regularly.
- Document flag purpose and usage.
- Write tests for all flag logic.

---

See also:
- [API Reference](api/flaggle.md)
- [FAQ](faq.md)
