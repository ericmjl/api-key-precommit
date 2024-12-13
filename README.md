# API Key Checker

A pre-commit hook to check for exposed API keys in your code. Supports configurable regex patterns to catch different types of API keys.

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/ericmjl/api-key-precommit
    rev: v0.1.0  # Use the latest tag/release
    hooks:
      - id: api-key-checker
        args:
          - "--pattern"
          - "[a-zA-Z0-9]{32,}"  # Generic API key pattern (32+ chars)
          - "--pattern"
          - "api[_-]key[_-][a-zA-Z0-9]{16,}"  # API key with prefix
          - "--pattern"
          - "^sk-proj-[A-Za-z0-9_-]+-rev[A-Za-z0-9_\\-\\.]+$"  # Project-specific key pattern
```

## Configuration

The hook accepts patterns through command-line arguments using the `--pattern` or `-p` flag. Each pattern must be preceded by its own flag.

Some example patterns you might want to use:

```yaml
args:
  - "--pattern"
  - "[A-Z0-9]{32}"  # Generic 32-char API key
  - "--pattern"
  - "sk-[A-Za-z0-9]{48}"  # OpenAI-style key
  - "--pattern"
  - "ghp_[A-Za-z0-9]{36}"  # GitHub personal access token
  - "--pattern"
  - "xox[baprs]-[A-Za-z0-9-]{10,}"  # Slack tokens
```

## Default Behavior

If no patterns are specified, the hook will use a default pattern that matches common API key formats:
- 32 or more alphanumeric characters (`[a-zA-Z0-9]{32,}`)

## Example Output

When an API key is detected, the hook will raise an exception with details about the match:

```
Found potential API key matching pattern '[A-Z0-9]{32}' in path/to/file.py:123-155
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e .
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
