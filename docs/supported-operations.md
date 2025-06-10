# Supported Operations

Flaggle provides a simple, explicit API for managing and evaluating feature flags in Python applications. This section covers the main operations, usage patterns, and the JSON schema for the `/flags` endpoint.

---

## Defining Flags

Flags can be defined at runtime, via configuration files, environment variables, or directly in code:

```python
flaggle.set_flag("new_ui", True)
flaggle.set_flag("beta", False)
```

- Use clear, descriptive names for each flag.
- Flags can be boolean or custom types (see [Advanced Usage](advanced.md)).

---

## Checking Flags

Check if a flag is enabled:

```python
if flaggle.is_enabled("new_ui"):
    # Feature is enabled
```

With context (for user-based or environment-based flags):

```python
flaggle.is_enabled("beta", context={"user_id": 123})
```

- Context can include user IDs, environment, or any custom data.

---

## Updating Flags

Update flag values at runtime:

```python
flaggle.set_flag("new_ui", False)
```

- Useful for toggling features during experiments or rollouts.

---

## Removing Flags

Remove a flag when it is no longer needed:

```python
flaggle.remove_flag("beta")
```

- Regularly clean up unused flags to avoid tech debt.

---

## Listing All Flags

Get a dictionary of all current flags:

```python
flags = flaggle.to_dict()
```

- Useful for debugging, admin panels, or exposing a `/flags` endpoint.

---

## JSON Schema for Flags Endpoint

The `/flags` endpoint returns a JSON object with the current state of all flags. Example response:

```json
{
  "new_ui": true,
  "beta": false
}
```

### JSON Schema

```json
{
  "type": "object",
  "patternProperties": {
    "^[a-zA-Z_][a-zA-Z0-9_]*$": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

- The schema enforces that all flag names are valid Python identifiers and all values are boolean.
- Extend the schema if you use custom flag types.

---

## Best Practices
- Use environment variables or config files for environment-specific flags.
- Document each flag's purpose and expected usage.
- Write tests for all flag logic and edge cases.
- Remove deprecated flags regularly.

---

## See Also
- [API Reference](api/flaggle.md)
- [Advanced Usage](advanced.md)
- [FAQ](faq.md)
