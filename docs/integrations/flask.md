# Flask Integration

Flaggle can be used with Flask to manage feature flags in your web applications. This guide provides a quickstart, advanced usage, and best practices for Flask projects.

---

## Quickstart

```python
from flask import Flask, jsonify
from python_flaggle import Flaggle

app = Flask(__name__)
flaggle = Flaggle()

@app.route("/feature-status")
def feature_status():
    return jsonify({"new_ui": flaggle.is_enabled("new_ui")})
```

---

## Advanced Usage

- **Dynamic flags**: Load flags from a database or remote service.
- **User-based flags**: Pass user context to `is_enabled` for per-user toggles.
- **Environment flags**: Use environment variables to control flag state.

### Example: User-based flag
```python
@app.route("/beta-access")
def beta_access():
    user_id = ...  # get user_id from request or session
    return jsonify({"beta": flaggle.is_enabled("beta", context={"user_id": user_id})})
```

---

## Tips for Flask
- Use application context or blueprints to share your `Flaggle` instance.
- Expose a `/flags` endpoint to return the current flag state (see JSON schema docs).
- Add tests for flag logic using Flask's test client and pytest.

---

## See Also
- [API Reference](../api/flaggle.md)
- [Advanced Usage](../advanced.md)
- [FAQ](../faq.md)

<!-- ...existing code... -->
