# Coding Instructions for LLM Tools

## Purpose
Guidelines for LLMs (e.g., GitHub Copilot) to generate, edit, and review code in the Flaggle project.

## Coding Standards
- Follow [PEP 8](https://peps.python.org/pep-0008/) for style.
- Use type annotations for all public functions and methods.
- Use Google-style docstrings for all public classes and methods.
- Prefer explicit, readable code over cleverness.
- Use triple double quotes (`"""`) for docstrings.
- Add examples in docstrings for public APIs.
- Use `from ... import ...` for imports within the package.

## Docstring Directives
- **Short docstring**: Use for simple, self-explanatory functions or classes. One concise sentence, no blank line after the summary.
- **Long docstring**: Use for public, complex, or reusable code. Structure:
  - First line: short summary.
  - Blank line.
  - Extended description (optional).
  - Args: List all parameters, their types, and descriptions.
  - Returns: Describe the return type and meaning.
  - Raises: List exceptions that may be raised.
  - Attributes: For classes, document all public attributes.
  - Examples: (Optional) Add usage examples for clarity, using indented code blocks in docstrings and fenced code blocks (```python) in markdown/README.
- **Tone**: Use clear, concise, and neutral language.
- **Formatting**: Use triple double quotes (`"""`) and follow [PEP 257](https://peps.python.org/pep-0257/).
- **Compatibility**: This template is compatible with VS Code, PyCharm, Sphinx, and most Python docstring tools. Structure is inspired by Google and NumPy conventions.

## File Structure
- Place new features in the appropriate module under `python_flaggle/`.
- Place all tests in `tests/`.

## Testing
- All new code must be covered by tests.
- Use `pytest` for all tests.
- Strive for 100% code coverage.
- Test both typical and edge cases.

## Example Docstring
```python
class MyClass:
    """
    Short summary of the class.

    Attributes:
        attr1 (type): Description.
    """
    def my_method(self, param1: int) -> bool:
        """
        Short summary of the method.

        Args:
            param1 (int): Description.
        Returns:
            bool: Description.
        Example:
            ```python
            obj = MyClass()
            obj.my_method(1)
            ```
        """
```
