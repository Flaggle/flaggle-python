# Frequently Asked Questions (FAQ) & Troubleshooting

Welcome to the Flaggle FAQ! Here you'll find answers to common questions, troubleshooting tips, and best practices for using Flaggle in your projects.

---

## General

### What is Flaggle?
Flaggle is a Python library for managing feature flags, supporting dynamic toggles, gradual rollouts, and safe experimentation. It integrates easily with FastAPI, Flask, Django, Typer, and more.

### Who should use Flaggle?
Anyone who wants to control feature availability in Python applications—web, CLI, or scripts. It's suitable for both beginners and advanced users.

---

## Installation & Setup

### How do I install Flaggle?
```bash
pip install python-flaggle
```
Or with Poetry:
```bash
poetry add python-flaggle
```

### What Python versions are supported?
Python 3.8 and above.

### How do I configure my first flag?
See [Getting Started](first-steps.md) for a step-by-step guide.

---

## Usage

### How do I check if a flag is enabled?
```python
from python_flaggle import Flaggle
flaggle = Flaggle()
if flaggle.is_enabled("my_flag"):
    # ...
```

### Can I use Flaggle with FastAPI/Flask/Django/Typer?
Yes! See the [Integrations](integrations/fastapi.md) section for detailed examples.

### How do I define environment-based or user-based flags?
Use the advanced configuration options. See [Advanced Usage](advanced.md).

---

## Troubleshooting

### My flag is not updating as expected
- Ensure your flag configuration is reloaded or refreshed if changed at runtime.
- Check for typos in flag names.
- Use the debug logging to trace flag evaluation.

### I get an ImportError or ModuleNotFoundError
- Make sure `python-flaggle` is installed in your environment.
- Check your virtual environment activation.

### Flags are not thread-safe in my app
- Flaggle is designed to be thread-safe. If you encounter issues, please [open an issue](https://github.com/Flaggle/flaggle-python/issues) with details.

---

## Best Practices & Tips
- Use descriptive flag names (e.g., `enable_new_checkout`)
- Remove unused flags regularly to avoid tech debt
- Write tests for flag logic and edge cases
- Document your flags for your team

---

## Still need help?
- [Open an issue](https://github.com/Flaggle/flaggle-python/issues)
- [Join the discussion](https://github.com/Flaggle/flaggle-python/discussions)
- [Contribute improvements](contributing.md)