# API Key Checker

A pre-commit hook to check for exposed API keys in your code. Supports configurable regex patterns to catch different types of API keys.

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/yourusername/api-key-checker
    rev: v0.1.0  # Use the latest tag/release
    hooks:
      - id: api-key-checker
        # Configure patterns directly in the pre-commit config
        args: [--pattern-strings, |
          # Common API key patterns
          - '[A-Z0-9]{32}'  # Generic 32-char API key
          - 'sk-[A-Za-z0-9]{48}'  # OpenAI-style key
          - 'ghp_[A-Za-z0-9]{36}'  # GitHub personal access token
          - 'xox[baprs]-[A-Za-z0-9-]{10,}'  # Slack tokens
        ]
```

## Configuration

The hook accepts patterns directly in the pre-commit config using YAML syntax. You can specify patterns in two ways:

### 1. As a List

```yaml
- id: api-key-checker
  args: [--pattern-strings, |
    - '[A-Z0-9]{32}'
    - 'sk-[A-Za-z0-9]{48}'
  ]
```

### 2. Using the Patterns Key

```yaml
- id: api-key-checker
  args: [--pattern-strings, |
    patterns:
      - '[A-Z0-9]{32}'
      - 'sk-[A-Za-z0-9]{48}'
  ]
```

## Default Behavior

If no patterns are specified, the hook will use a default pattern that matches common API key formats:
- 32 or more alphanumeric characters (`[a-zA-Z0-9]{32,}`)

## Example Output

When an API key is detected:

```
[ERROR] Found potential API key matching pattern '[A-Z0-9]{32}' in path/to/file.py:123-155
[ERROR] Found potential API key matching pattern 'sk-[A-Za-z0-9]{48}' in config.json:45-94
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
