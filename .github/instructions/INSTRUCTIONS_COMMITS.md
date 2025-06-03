# Commit Message Instructions for LLM Tools

## Purpose
Guidelines for LLMs to generate clear, conventional commit messages for the Flaggle project.

## Format
- Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
  - `type(scope): subject`
  - Example: `feat(flag): add support for float flag types`
- Types: feat, fix, docs, style, refactor, test, chore
- Use imperative mood (e.g., "add", not "adds")
- Limit subject line to 72 characters
- Use body to explain what and why, not how (if needed)
- Reference issues or PRs if relevant

## Examples
- `fix(flaggle): handle ValueError in _fetch_flags`
- `docs(readme): clarify JSON schema for flags endpoint`
- `test(flag): add test for else branch in is_enabled`
