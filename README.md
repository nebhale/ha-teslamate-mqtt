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

### Linting

This repository vendors Home Assistant Core's Ruff and Pylint configuration in
`pyproject.toml`, with first-party import paths adjusted for the standalone
custom integration layout. Install lint dependencies with the `lint` extra,
then run Ruff and Pylint directly. The GitHub Validate workflow runs the
same checks on pushes and pull requests:

```bash
python -m pip install -e .[lint]
ruff check .
ruff format --check .
pylint custom_components tests
```

## Status

This project is currently scaffolded and ready for implementation.
