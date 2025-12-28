#!/usr/bin/env python3
"""Main CLI entry point for blood pressure tracker."""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from .config import Config, ConfigError
from .storage import CSVStorage, StorageError
from .validator import BPValidator, ValidationError
from .models import BPReading
from .categories import BPCategoryClassifier


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
              f"{systolic}/{diastolic} mmHg, {bpm} BPM, {reading.category.abbreviation}")

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

        print(f"\nReading saved successfully!")
        print(f"  {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
              f"{systolic}/{diastolic} mmHg, {bpm} BPM, {reading.category.abbreviation}")

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


def list_readings_command(args: argparse.Namespace, config: Config) -> None:
    """Display past blood pressure readings from CSV file.

    Args:
        args: Parsed command-line arguments
        config: Config instance
    """
    try:
        csv_path = config.get_csv_path()
        storage = CSVStorage(csv_path)

        if not csv_path.exists():
            print(f"No readings found. CSV file does not exist: {csv_path}", file=sys.stderr)
            print(f"\nLog your first reading with: bp-tracker <systolic> <diastolic> <bpm>")
            sys.exit(1)

        readings = storage.read_all()

        if not readings:
            print("No readings found in CSV file.")
            return

        # Determine how many readings to show
        if args.all:
            readings_to_show = readings
        elif args.last:
            readings_to_show = readings[-args.last:]
        else:
            # Default: show last 10 readings
            readings_to_show = readings[-10:]

        # Print header
        print(f"\nBlood Pressure Readings (from {csv_path})")
        print("=" * 70)
        print(f"{'Date':<12} {'Time':<10} {'BP (mmHg)':<15} {'BPM':<5} {'Category':<10}")
        print("-" * 70)

        # Print readings
        for reading in readings_to_show:
            bp_reading = f"{reading['Systolic']}/{reading['Diastolic']}"
            print(f"{reading['Date']:<12} {reading['Time']:<10} {bp_reading:<15} "
                  f"{reading['BPM']:<5} {reading['Category']:<10}")

        print("-" * 70)
        print(f"Total readings shown: {len(readings_to_show)} of {len(readings)}")
        print()

    except StorageError as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"CSV Format Error: Missing column {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


def chart_command(args: argparse.Namespace, config: Config) -> None:
    """Generate and display a chart of blood pressure readings.

    Args:
        args: Parsed command-line arguments
        config: Config instance
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("Error: matplotlib is required for charting.", file=sys.stderr)
        print("Install it with: pip install matplotlib", file=sys.stderr)
        print("Or: sudo pacman -S python-matplotlib", file=sys.stderr)
        sys.exit(1)

    try:
        csv_path = config.get_csv_path()
        storage = CSVStorage(csv_path)

        if not csv_path.exists():
            print(f"No readings found. CSV file does not exist: {csv_path}", file=sys.stderr)
            print(f"\nLog your first reading with: bp-tracker <systolic> <diastolic> <bpm>")
            sys.exit(1)

        readings = storage.read_all()

        if not readings:
            print("No readings found in CSV file.")
            sys.exit(1)

        if len(readings) < 2:
            print("Need at least 2 readings to create a chart.")
            sys.exit(1)

        # Parse dates and values
        dates = []
        systolic_values = []
        diastolic_values = []
        bpm_values = []
        category_values = []

        for reading in readings:
            date_str = f"{reading['Date']} {reading['Time']}"
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            dates.append(date_obj)
            systolic_values.append(int(reading['Systolic']))
            diastolic_values.append(int(reading['Diastolic']))
            bpm_values.append(int(reading['BPM']))

            # Get category value from CSV (calculated on-the-fly for old data)
            category_value = BPCategoryClassifier.get_value_from_abbreviation(reading['Category'])
            category_values.append(category_value)

        # Determine how many readings to chart
        if args.last:
            dates = dates[-args.last:]
            systolic_values = systolic_values[-args.last:]
            diastolic_values = diastolic_values[-args.last:]
            bpm_values = bpm_values[-args.last:]
            category_values = category_values[-args.last:]

        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
        fig.suptitle('Blood Pressure Tracking', fontsize=16, fontweight='bold')

        # === PANEL 1: Blood Pressure Category ===
        # Plot category line
        ax1.plot(dates, category_values, marker='o', linestyle='-',
                linewidth=2, markersize=6, color='#34495E', zorder=10)

        # Add colored horizontal zones for each category
        categories = BPCategoryClassifier.get_all_categories()
        for cat in categories:
            ax1.axhspan(cat.value - 0.5, cat.value + 0.5,
                       facecolor=cat.color, alpha=0.3, zorder=1)

        # Configure Y-axis with numeric values and text labels
        ax1.set_ylim(0.5, 6.5)
        ax1.set_yticks([1, 2, 3, 4, 5, 6])
        ax1.set_yticklabels([cat.abbreviation for cat in categories])
        ax1.set_ylabel('BP Category', fontsize=12, fontweight='bold')
        ax1.set_title('Blood Pressure Category Trend', fontsize=14)
        ax1.grid(True, alpha=0.3, axis='x')  # Only vertical grid lines
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

        # === PANEL 2: Blood Pressure Values ===
        ax2.plot(dates, systolic_values, marker='o', linestyle='-',
                linewidth=2, markersize=6, label='Systolic', color='#E74C3C')
        ax2.plot(dates, diastolic_values, marker='o', linestyle='-',
                linewidth=2, markersize=6, label='Diastolic', color='#3498DB')
        ax2.set_ylabel('Blood Pressure (mmHg)', fontsize=12, fontweight='bold')
        ax2.set_title('Blood Pressure Trend', fontsize=14)
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

        # Add reference lines for normal BP
        ax2.axhline(y=120, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax2.axhline(y=80, color='gray', linestyle='--', alpha=0.5, linewidth=1)

        # === PANEL 3: Heart Rate ===
        ax3.plot(dates, bpm_values, marker='o', linestyle='-',
                linewidth=2, markersize=6, label='Heart Rate', color='#2ECC71')
        ax3.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Heart Rate (BPM)', fontsize=12, fontweight='bold')
        ax3.set_title('Heart Rate Trend', fontsize=14)
        ax3.legend(loc='upper right', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

        # Rotate x-axis labels for better readability
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()

        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Chart saved to: {output_path}")
        else:
            # Display interactively
            print(f"Displaying chart for {len(dates)} readings...")
            print("Close the chart window to continue.")
            plt.show()

    except StorageError as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"CSV Format Error: Missing column {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Data Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


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
               '  bp-tracker list               # View past readings\n'
               '  bp-tracker chart              # Display trend chart\n'
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


def create_list_parser() -> argparse.ArgumentParser:
    """Create argument parser for list command.

    Returns:
        Configured ArgumentParser for list
    """
    parser = argparse.ArgumentParser(
        prog='bp-tracker list',
        description='View past blood pressure readings'
    )

    parser.add_argument('--all', action='store_true',
                       help='Show all readings')
    parser.add_argument('--last', type=int, metavar='N',
                       help='Show last N readings (default: 10)')
    parser.add_argument('--config', type=str, metavar='PATH',
                       help='Path to config file (default: ~/.config/bp-tracker/config.yaml)')

    return parser


def create_chart_parser() -> argparse.ArgumentParser:
    """Create argument parser for chart command.

    Returns:
        Configured ArgumentParser for chart
    """
    parser = argparse.ArgumentParser(
        prog='bp-tracker chart',
        description='Generate a chart of blood pressure trends'
    )

    parser.add_argument('--last', type=int, metavar='N',
                       help='Chart last N readings (default: all)')
    parser.add_argument('--output', '-o', type=str, metavar='FILE',
                       help='Save chart to file (PNG/SVG/PDF) instead of displaying')
    parser.add_argument('--config', type=str, metavar='PATH',
                       help='Path to config file (default: ~/.config/bp-tracker/config.yaml)')

    return parser


def main():
    """Main entry point for the CLI application."""
    # Check if first argument is 'list' command
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        # Use list parser
        parser = create_list_parser()
        args = parser.parse_args(sys.argv[2:])  # Parse args after 'list'

        try:
            config_path = Path(args.config) if args.config else None
            config = Config(config_path)
            list_readings_command(args, config)
        except ConfigError as e:
            print(f"Configuration Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected Error: {e}", file=sys.stderr)
            sys.exit(1)
    # Check if first argument is 'chart' command
    elif len(sys.argv) > 1 and sys.argv[1] == 'chart':
        # Use chart parser
        parser = create_chart_parser()
        args = parser.parse_args(sys.argv[2:])  # Parse args after 'chart'

        try:
            config_path = Path(args.config) if args.config else None
            config = Config(config_path)
            chart_command(args, config)
        except ConfigError as e:
            print(f"Configuration Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected Error: {e}", file=sys.stderr)
            sys.exit(1)
    # Check if first argument is 'config' command
    elif len(sys.argv) > 1 and sys.argv[1] == 'config':
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
