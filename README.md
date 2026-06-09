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
extra, and validation tools live in the `lint` extra so each environment can
install only what it needs.

### Environment

This repository includes a `.python-version` file for pyenv users. Install the
configured Python version, then create a local virtual environment:

```bash
pyenv install --skip-existing
python -m venv .venv
```

### Linting

This repository vendors Home Assistant Core's Ruff and Pylint configuration in
`pyproject.toml`, with first-party import paths adjusted for the standalone
custom integration layout. Install lint dependencies with the `lint` extra,
then run Ruff and Pylint directly. Use a normal, non-editable install so Home
Assistant's custom component loader sees the repository layout the same way CI
does. The GitHub Validate workflow runs the same checks on pull requests:

```bash
python -m pip install .[lint]
ruff check .
ruff format --check .
pylint custom_components tests
```

### Testing

Install the test extra before running the test suite:

```bash
python -m pip install .[test]
pytest tests
```

## Status

This project is currently scaffolded and ready for implementation.
