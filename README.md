# Computer-Vision

This is the code hub for the Computer Vision-related component of the Vision-Guided Autonomous Robot. All code for this component can be found here and is planned to be updated regularly.

## Raspberry Pi Quick Start

This project includes a one-command Raspberry Pi setup and run script.

```bash
chmod +x scripts/pi_setup_and_run.sh
./scripts/pi_setup_and_run.sh
```

Headless mode (no OpenCV preview window):

```bash
HEADLESS=1 ./scripts/pi_setup_and_run.sh
```

For faster repeat runs after initial setup:

```bash
chmod +x scripts/pi_run.sh
./scripts/pi_run.sh
```

Detailed setup notes are in `docs/raspberry-pi.md`.

## Project Structure

```
Computer-Vision/
├── vision/              # ArUco detection, camera capture, image processing
├── state_machine/       # Behavioral state machine (seek, engage, evade)
├── interfaces/          # Abstract contracts for detectors and cameras
├── config/              # Settings, ArUco parameters, environment config
├── utils/               # Geometry, logging, shared helpers
├── tests/               # Unit and integration tests
├── docs/                # Architecture and API documentation
├── scripts/             # Developer and deployment helper scripts
├── requirements.txt
└── README.md
```
