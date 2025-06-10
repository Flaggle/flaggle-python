# Flaggle: Feature Flag Management for Python

Flaggle is a modern, easy-to-use feature flag management library for Python, designed for seamless integration with FastAPI and other popular frameworks. It helps you control feature rollouts, run experiments, and manage toggles in production with confidence.

## Key Features
- **First-class FastAPI integration** (plus Flask, Django, Typer, and more)
- **Simple, explicit API** for defining and checking flags
- **JSON schema endpoint** for flag state
- **Environment and user-based flagging**
- **Extensive test coverage and type hints**
- **Modern Pythonic design**

## Why Flaggle?
- **Easy to learn**: Minimal setup, clear API, and great docs
- **Flexible**: Use in web apps, CLIs, scripts, or anywhere Python runs
- **Safe**: Test and roll out features gradually
- **Extensible**: Add custom flag types and logic

## Example: Minimal FastAPI Integration
```python
from fastapi import FastAPI
from python_flaggle import Flaggle

app = FastAPI()
flaggle = Flaggle()

@app.get("/feature-status")
def feature_status():
    return {"new_ui": flaggle.is_enabled("new_ui")}
```

## Next Steps
- [Getting Started](first-steps.md)
- [Configuration](configuration.md)
- [API Reference](api/flaggle.md)
- [Integrations](integrations/fastapi.md)
- [Tips & FAQ](faq.md)

---

> **Tip:** Use the search bar or navigation to quickly find guides, API docs, and integration examples.

---

## Community & Contributing
- [Contributing Guide](contributing.md)
- [Changelog](changelog.md)
- [License](license.md)

---

*Flaggle is open source and welcomes your feedback, issues, and pull requests!*
