# Raspberry Pi Quick Start

This project supports Raspberry Pi for ArUco MVP camera testing.

## Recommended Hardware/OS

- Raspberry Pi 4 or 5
- Raspberry Pi OS (64-bit)
- USB webcam or Pi camera exposed as `/dev/video0`

## One-Command Setup + Run

From the project root:

```bash
chmod +x scripts/pi_setup_and_run.sh
./scripts/pi_setup_and_run.sh
```

This will:

- install required system packages
- create a local Python virtual environment (`.venv`)
- install Python dependencies
- start the detector loop

## Headless Mode (No Preview Window)

```bash
HEADLESS=1 ./scripts/pi_setup_and_run.sh
```

## Faster Repeat Runs

After the first successful setup, use the lightweight run script:

```bash
chmod +x scripts/pi_run.sh
./scripts/pi_run.sh
```

Headless repeat run:

```bash
HEADLESS=1 ./scripts/pi_run.sh
```

## Common Runtime Arguments

```bash
./scripts/pi_setup_and_run.sh --camera-index 0 --width 640 --height 480 --dictionary DICT_4X4_50 --target-id 7
```

The same arguments can be passed to `./scripts/pi_run.sh`.

## Notes

- If camera open fails, verify your device index and run: `ls /dev/video*`
- Start at 640x480 for stable performance on Pi