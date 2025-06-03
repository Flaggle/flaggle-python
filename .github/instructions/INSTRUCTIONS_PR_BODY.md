# Pull Request Body Instructions for LLM Tools

## Purpose
Guidelines for LLMs to generate clear, informative PR bodies for the Flaggle project.

## Structure
- **Summary**: Briefly describe what the PR does.
- **Motivation**: Why is this change needed?
- **Changes**: List major changes (new features, bug fixes, refactors, docs, tests).
- **Testing**: Describe how the change was tested.
- **Checklist**:
  - [ ] Code follows style and docstring guidelines
  - [ ] Tests added/updated and passing
  - [ ] Documentation updated
  - [ ] No unrelated changes
- **Related Issues/PRs**: Reference any related issues or pull requests.

## Example
```
## Summary
Add async support to Flaggle's flag fetching.

## Motivation
Async support allows non-blocking flag updates in async applications.

## Changes
- Add async versions of fetch/update methods
- Update tests for async
- Update README with async usage

## Testing
- Added new async tests
- All tests pass locally

## Checklist
- [x] Code follows style and docstring guidelines
- [x] Tests added/updated and passing
- [x] Documentation updated
- [x] No unrelated changes

## Related Issues/PRs
Closes #42
```
