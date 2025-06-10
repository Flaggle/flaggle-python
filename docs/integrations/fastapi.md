# FastAPI Integration

Flaggle is designed for seamless integration with FastAPI, making it easy to manage feature flags in your API endpoints. Below you'll find a quickstart, advanced usage, and tips for production deployments.

---

## Quickstart

```python
from fastapi import FastAPI
from python_flaggle import Flaggle

app = FastAPI()
flaggle = Flaggle()

@app.get("/feature-status")
def feature_status():
    return {"new_ui": flaggle.is_enabled("new_ui")}
```

---

## Advanced Usage

- **Dynamic flags**: Load flags from a database or remote service.
- **User-based flags**: Pass user context to `is_enabled` for per-user toggles.
- **Environment flags**: Use environment variables to control flag state.

### Example: User-based flag
```python
@app.get("/beta-access")
def beta_access(user_id: int):
    return {"beta": flaggle.is_enabled("beta", context={"user_id": user_id})}
```

---

## Example: Dependency Injection

For larger FastAPI projects, use dependency injection to share your `Flaggle` instance across routes:

```python
from fastapi import Depends, FastAPI
from python_flaggle import Flaggle

def get_flaggle():
    return flaggle

app = FastAPI()
flaggle = Flaggle()

@app.get("/feature-status")
def feature_status(flaggle: Flaggle = Depends(get_flaggle)):
    return {"new_ui": flaggle.is_enabled("new_ui")}
```

---

## Example: Exposing a Flags Endpoint

Expose a `/flags` endpoint to return all current flag states (useful for debugging or frontends):

```python
@app.get("/flags")
def all_flags():
    return flaggle.to_dict()  # Or your preferred serialization
```

---

## Example: Testing with TestClient

Write tests for your flag logic using FastAPI's `TestClient` and `pytest`:

```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_feature_status():
    response = client.get("/feature-status")
    assert response.status_code == 200
    assert "new_ui" in response.json()
```

---

## Example: Async Flags (Advanced)

If your flag source is async (e.g., database or remote API), you can use FastAPI's async support:

```python
from fastapi import FastAPI
from python_flaggle import Flaggle

app = FastAPI()
flaggle = Flaggle()

@app.get("/async-feature-status")
async def async_feature_status():
    # Example: await an async flag check (if implemented)
    return {"new_ui": await flaggle.is_enabled_async("new_ui")}
```

_Note: Only use async if your flag source requires it. The default Flaggle API is synchronous._

---

## Example: OpenAPI Docs for Flags

Document your flag endpoints for automatic FastAPI docs:

```python
@app.get("/flags", response_model=dict, summary="Get all feature flags", tags=["Flags"])
def all_flags():
    """Return the current state of all feature flags."""
    return flaggle.to_dict()
```

---

## Example: JSON Schema Endpoint

Expose a JSON schema for your flags (useful for frontends or validation):

```python
@app.get("/flags/schema", response_model=dict, summary="Get flags JSON schema", tags=["Flags"])
def flags_schema():
    return flaggle.json_schema()  # Implement this method as needed
```

---

## Security Considerations
- Protect sensitive flag endpoints (e.g., `/flags`, `/flags/schema`) with authentication in production.
- Avoid exposing internal-only flags to public APIs.

---

## Pro Tips
- Use [Pydantic settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) for environment-based flag configuration.
- Document your flags and endpoints for your team.
- Use [FastAPI's dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/) for scalable, testable code.

---

## See Also
- [API Reference](../api/flaggle.md)
- [Advanced Usage](../advanced.md)
- [FAQ](../faq.md)

<!-- ...existing code... -->
