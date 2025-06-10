# Typer Integration

Flaggle can be used in Typer-based CLI applications to control feature flags for command-line tools. This guide provides a quickstart, advanced usage, and best practices for Typer projects.

---

## Quickstart

```python
import typer
from python_flaggle import Flaggle

app = typer.Typer()
flaggle = Flaggle()

@app.command()
def feature_status():
    typer.echo(f"new_ui: {flaggle.is_enabled('new_ui')}")

if __name__ == "__main__":
    app()
```

---

## Advanced Usage

- **Dynamic flags**: Load flags from a database or remote service.
- **User-based flags**: Pass user context to `is_enabled` for per-user toggles.
- **Environment flags**: Use environment variables to control flag state.

### Example: User-based flag
```python
@app.command()
def beta_access(user_id: int):
    typer.echo(f"beta: {flaggle.is_enabled('beta', context={'user_id': user_id})}")
```

---

## Tips for Typer
- Use a shared `Flaggle` instance for all commands.
- Add tests for flag logic using Typer's test runner and pytest.

---

## See Also
- [API Reference](../api/flaggle.md)
- [Advanced Usage](../advanced.md)
- [FAQ](../faq.md)

<!-- ...existing code... -->
