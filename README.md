> [!WARNING]
> This project is archived as of August, 2026.  The functionality provided by it is now [included in TeslaMate natively][tm-discovery] starting in 4.1.0.

[tm-discovery]: https://docs.teslamate.org/docs/integrations/home_assistant#mqtt-discovery-automatic-configuration

# TeslaMate MQTT for Home Assistant

TeslaMate MQTT is a custom Home Assistant integration for exposing TeslaMate MQTT data as Home Assistant entities.

## Installation

### HACS

1. Add this repository to HACS as a custom repository.
2. Select `Integration` as the repository type.
3. Install `TeslaMate MQTT`.
4. Restart Home Assistant.
5. Add the integration from **Settings > Devices & services**.

### Manual

Copy `custom_components/teslamate_mqtt` into your Home Assistant `custom_components` directory and restart Home Assistant.

## Development

This repository follows the HACS custom integration layout:

```text
custom_components/teslamate_mqtt/
  __init__.py
  config_flow.py
  const.py
  manifest.json
```

Runtime imports from `custom_components/teslamate_mqtt` are declared as normal
project dependencies in `pyproject.toml`. Test-only packages live in the `test`
dependency group, and validation tools live in the `lint` group so each environment can
install only what it needs.

### Environment

This repository uses uv for Python and dependency management. Install uv and let
it choose a Python version from `pyproject.toml`, then sync the dependency groups
you need:

```bash
uv python install
uv sync --group lint --group test --no-install-project
```

### Linting

This repository vendors Home Assistant Core's Ruff and Pylint configuration in
`pyproject.toml`, with first-party import paths adjusted for the standalone
custom integration layout. Sync the `lint` dependency group, then run the
validation tools through uv. The GitHub Validate workflow runs the same checks
on pull requests:

```bash
uv sync --group lint --no-install-project
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pylint custom_components tests
uv run --no-sync mypy
```

### Testing

Sync the `test` dependency group before running the test suite:

```bash
uv sync --group test --no-install-project
uv run --no-sync pytest tests
```

## Status

This project is currently scaffolded and ready for implementation.
