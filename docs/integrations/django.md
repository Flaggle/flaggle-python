# Django Integration

Flaggle can be integrated into Django projects to manage feature flags in your views and templates. This guide covers quickstart, advanced usage, and best practices for Django.

---

## Quickstart

```python
from django.http import JsonResponse
from python_flaggle import Flaggle

flaggle = Flaggle()

def feature_status(request):
    return JsonResponse({"new_ui": flaggle.is_enabled("new_ui")})
```

Add the view to your `urls.py`:
```python
from django.urls import path
from .views import feature_status

urlpatterns = [
    path("feature-status/", feature_status),
]
```

---

## Advanced Usage

- **Dynamic flags**: Load flags from a database or remote service.
- **User-based flags**: Pass user context to `is_enabled` for per-user toggles.
- **Environment flags**: Use environment variables to control flag state.

### Example: User-based flag
```python
def beta_access(request):
    user_id = request.user.id if request.user.is_authenticated else None
    return JsonResponse({"beta": flaggle.is_enabled("beta", context={"user_id": user_id})})
```

---

## Tips for Django
- Use Django settings or app config to share your `Flaggle` instance.
- Expose a `/flags/` endpoint to return the current flag state (see JSON schema docs).
- Add tests for flag logic using Django's test client and pytest.

---

## See Also
- [API Reference](../api/flaggle.md)
- [Advanced Usage](../advanced.md)
- [FAQ](../faq.md)

<!-- ...existing code... -->
