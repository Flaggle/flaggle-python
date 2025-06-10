# Other Integrations

Flaggle is flexible and can be used in a variety of Python environments beyond FastAPI, Flask, Django, and Typer. Here are some additional integration ideas and tips.

---

## Generic Python Scripts

```python
from python_flaggle import Flaggle

flaggle = Flaggle()

if flaggle.is_enabled("new_ui"):
    print("New UI is enabled!")
```

---

## Celery Tasks

```python
from celery import shared_task
from python_flaggle import Flaggle

flaggle = Flaggle()

@shared_task
def my_task():
    if flaggle.is_enabled("background_feature"):
        # ...
```

---

## Jupyter Notebooks

```python
from python_flaggle import Flaggle
flaggle = Flaggle()
flaggle.is_enabled("notebook_feature")
```

---

## Tips for Other Environments
- Always use a single `Flaggle` instance per process when possible.
- For distributed systems, consider syncing flag state via a database or API.
- Add tests for flag logic in your environment's preferred test framework.

---

## See Also
- [API Reference](../api/flaggle.md)
- [Advanced Usage](../advanced.md)
- [FAQ](../faq.md)

<!-- ...existing code... -->
