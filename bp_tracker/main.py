#!/usr/bin/env python3
"""Main CLI entry point for blood pressure tracker."""

import argparse
import sys
from pathlib import Path
from .config import Config, ConfigError
from .storage import CSVStorage, StorageError
from .validator import BPValidator, ValidationError
from .models import BPReading


def interactive_mode(storage: CSVStorage) -> None:
    """Run in interactive mode, prompting user for input.

    Args:
        storage: CSVStorage instance for saving readings
    """
    print("Blood Pressure Tracker - Interactive Mode")
    print("=" * 45)

    try:
        # Prompt for systolic
        systolic_input = input("Enter systolic pressure: ").strip()
        systolic = BPValidator.validate_systolic(int(systolic_input))

        # Prompt for diastolic
        diastolic_input = input("Enter diastolic pressure: ").strip()
        diastolic = BPValidator.validate_diastolic(int(diastolic_input), systolic)

        # Prompt for BPM
        bpm_input = input("Enter heart rate (BPM): ").strip()
        bpm = BPValidator.validate_bpm(int(bpm_input))

        # Create and save reading
        reading = BPReading.create(systolic, diastolic, bpm)
        storage.append_reading(reading)

        print(f"\nReading saved successfully!")
        print(f"  {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
              f"{systolic}/{diastolic} mmHg, {bpm} BPM")

    except ValueError:
        print("Error: Invalid input - please enter numbers only", file=sys.stderr)
        sys.exit(1)
    except ValidationError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (StorageError, IOError) as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.", file=sys.stderr)
        sys.exit(130)


def command_mode(args: argparse.Namespace, storage: CSVStorage) -> None:
    """Process blood pressure reading from command-line arguments.

    Args:
        args: Parsed command-line arguments
        storage: CSVStorage instance for saving readings
    """
    try:
        # Validate inputs
        systolic, diastolic, bpm = BPValidator.validate_reading(
            args.systolic, args.diastolic, args.bpm
        )

        # Create and save reading
        reading = BPReading.create(systolic, diastolic, bpm)
        storage.append_reading(reading)

        print(f"Reading saved: {systolic}/{diastolic} mmHg, {bpm} BPM")

    except ValidationError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (StorageError, IOError) as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_config_command(args: argparse.Namespace, config: Config) -> None:
    """Handle configuration setup command.

    Args:
        args: Parsed command-line arguments
        config: Config instance
    """
    if args.show:
        # Show current configuration
        csv_path = config.get_csv_path()
        print(f"Configuration:")
        print(f"  Config file: {config.config_path}")
        print(f"  CSV file: {csv_path}")
        print(f"  CSV exists: {csv_path.exists()}")

    elif args.csv_path:
        # Set new CSV path
        new_path = Path(args.csv_path).expanduser().resolve()
        config.set_csv_path(new_path)
        print(f"CSV path updated to: {new_path}")

    else:
        # Initialize default config
        config.initialize_default()
        print(f"Configuration initialized at: {config.config_path}")


def create_reading_parser() -> argparse.ArgumentParser:
    """Create argument parser for blood pressure readings.

    Returns:
        Configured ArgumentParser for readings
    """
    parser = argparse.ArgumentParser(
        prog='bp-tracker',
        description='Track blood pressure readings',
        epilog='Examples:\n'
               '  bp-tracker 120 80 72          # Log reading via command line\n'
               '  bp-tracker                    # Interactive mode\n'
               '  bp-tracker config --show      # Show configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Optional positional arguments for command-line mode
    parser.add_argument('systolic', nargs='?', type=int,
                       help='Systolic pressure (mmHg)')
    parser.add_argument('diastolic', nargs='?', type=int,
                       help='Diastolic pressure (mmHg)')
    parser.add_argument('bpm', nargs='?', type=int,
                       help='Heart rate (beats per minute)')

    # Configuration management
    parser.add_argument('--config', type=str, metavar='PATH',
                       help='Path to config file (default: ~/.config/bp-tracker/config.yaml)')

    return parser


def create_config_parser() -> argparse.ArgumentParser:
    """Create argument parser for config command.

    Returns:
        Configured ArgumentParser for config
    """
    parser = argparse.ArgumentParser(
        prog='bp-tracker config',
        description='Manage blood pressure tracker configuration'
    )

    parser.add_argument('--show', action='store_true',
                       help='Show current configuration')
    parser.add_argument('--csv-path', type=str, metavar='PATH',
                       help='Set CSV file path')
    parser.add_argument('--config', type=str, metavar='PATH',
                       help='Path to config file (default: ~/.config/bp-tracker/config.yaml)')

    return parser


def main():
    """Main entry point for the CLI application."""
    # Check if first argument is 'config' command
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        # Use config parser
        parser = create_config_parser()
        args = parser.parse_args(sys.argv[2:])  # Parse args after 'config'

        try:
            config_path = Path(args.config) if args.config else None
            config = Config(config_path)
            setup_config_command(args, config)
        except ConfigError as e:
            print(f"Configuration Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Use reading parser
        parser = create_reading_parser()
        args = parser.parse_args()

        try:
            # Initialize configuration
            config_path = Path(args.config) if args.config else None
            config = Config(config_path)

            # Get CSV storage path
            csv_path = config.get_csv_path()
            storage = CSVStorage(csv_path)

            # Determine mode: command-line args or interactive
            if args.systolic is not None:
                # Command-line mode: all three values must be provided
                if args.diastolic is None or args.bpm is None:
                    parser.error("All three values required: systolic diastolic bpm")
                command_mode(args, storage)
            else:
                # Interactive mode
                if args.diastolic is not None or args.bpm is not None:
                    parser.error("All three values required: systolic diastolic bpm")
                interactive_mode(storage)

        except ConfigError as e:
            print(f"Configuration Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
