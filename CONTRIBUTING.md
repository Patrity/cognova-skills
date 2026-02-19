# Contributing Skills to Cognova

Thanks for contributing to the Cognova skills library!

## Skill Structure

Each skill lives in its own directory at the repo root:

```
your-skill/
  SKILL.md       # Required - skill definition with frontmatter
  your-skill.py  # Optional - Python script for logic
```

## SKILL.md Requirements

Your `SKILL.md` must include YAML frontmatter with these fields:

```yaml
---
name: your-skill
description: A clear description of what the skill does
allowed-tools: Bash, Read
metadata:
  version: "1.0.0"
  requires-secrets: []
  author: "your-github-username"
  repository: "https://github.com/Patrity/cognova-skills"
  installed-from: "cognova-skills"
---
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Skill name (lowercase, hyphens, must match directory name) |
| `description` | What the skill does (shown in library) |
| `allowed-tools` | Claude Code tools the skill needs |
| `metadata.version` | Semver version string |
| `metadata.author` | Your GitHub username |

### Optional Fields

| Field | Description |
|-------|-------------|
| `metadata.requires-secrets` | API keys needed (e.g., `["OPENWEATHER_API_KEY"]`) |
| `metadata.repository` | Link to this repo |

## Rules

1. **No hardcoded secrets** - Use `get_secret()` from `_lib/api.py` for any API keys or tokens
2. **List required secrets** - If your skill needs API keys, list them in `metadata.requires-secrets`
3. **Use argparse** - Python scripts should use argparse for CLI interface
4. **Import shared library** - Use `sys.path.insert(0, str(Path(__file__).parent.parent)); from _lib.api import get, post, get_secret`

## Submission Process

1. Fork this repository
2. Create your skill directory with `SKILL.md` (and optional Python script)
3. Test locally by copying to `~/.claude/skills/`
4. Submit a pull request

The CI will automatically:
- Validate your SKILL.md frontmatter
- Scan for hardcoded secrets
- Update `registry.json` on merge
