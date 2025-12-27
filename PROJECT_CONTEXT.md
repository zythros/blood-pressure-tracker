# Blood Pressure Tracker - Project Context

## Project Overview

A Python CLI tool for tracking blood pressure readings with automatic timestamps, configurable storage location, and comprehensive input validation.

**Created:** 2025-12-27
**Language:** Python 3.7+
**Dependencies:** PyYAML (only external dependency)

## Project Structure

```
bloodpressure/
├── bp_tracker/                 # Main package
│   ├── __init__.py            # Package initialization and exports
│   ├── main.py                # CLI entry point and argument parsing
│   ├── config.py              # YAML configuration management
│   ├── storage.py             # CSV file operations
│   ├── validator.py           # Input validation with medical ranges
│   └── models.py              # BPReading dataclass
├── setup.py                   # Package installation configuration
├── requirements.txt           # PyYAML>=6.0
├── README.md                  # User-facing documentation
├── .gitignore                 # Git ignore patterns
└── PROJECT_CONTEXT.md         # This file
```

## Key Features

### 1. Dual Input Modes
- **Command-line mode:** `python3 -m bp_tracker.main 120 80 72`
- **Interactive mode:** `python3 -m bp_tracker.main` (prompts for each value)

### 2. Data Storage
- **Format:** CSV with columns: Date, Time, Systolic, Diastolic, BPM
- **Default location:** `~/.local/share/bp-tracker/blood_pressure.csv`
- **Auto-creation:** Creates file with headers on first use
- **Append-only:** Efficient writing without reading entire file

### 3. Configuration
- **Format:** YAML
- **Default location:** `~/.config/bp-tracker/config.yaml`
- **Configurable:** CSV file path can be customized
- **XDG compliant:** Follows Linux/Unix directory standards

### 4. Validation
Prevents invalid data entry with medical-based ranges:
- **Systolic:** 70-250 mmHg
- **Diastolic:** 40-150 mmHg (must be less than systolic)
- **Heart Rate (BPM):** 30-250 beats per minute

### 5. Error Handling
- Custom exceptions: `ValidationError`, `StorageError`, `ConfigError`
- Proper exit codes: 0 (success), 1 (error), 130 (cancelled)
- Informative error messages to stderr

## Technical Architecture

### Data Flow

```
User Input → Validator → BPReading Model → CSVStorage → CSV File
                ↓
            Config (YAML) determines CSV file path
```

### Module Responsibilities

#### `models.py`
- `BPReading` dataclass: Stores systolic, diastolic, bpm, timestamp
- Factory method `create()`: Auto-generates timestamp if not provided
- Method `to_csv_row()`: Converts to CSV format [Date, Time, Systolic, Diastolic, BPM]

#### `validator.py`
- `BPValidator` class: Static validation methods
- Range checking for all three values
- Relationship validation (diastolic < systolic)
- Type coercion from string to int

#### `storage.py`
- `CSVStorage` class: Manages CSV file operations
- `initialize()`: Creates CSV with headers if needed
- `append_reading()`: Appends single reading to file
- `read_all()`: Reads all readings (for future features)

#### `config.py`
- `Config` class: YAML configuration management
- `load()`: Reads config or returns defaults
- `save()`: Writes config to YAML file
- `get_csv_path()`: Returns configured or default CSV path
- `set_csv_path()`: Updates CSV path in config

#### `main.py`
- CLI entry point and orchestration
- Two parsers: `create_reading_parser()` and `create_config_parser()`
- `interactive_mode()`: Prompts user for input
- `command_mode()`: Processes command-line arguments
- `setup_config_command()`: Handles config subcommand

## Usage Examples

### Basic Usage

```bash
# Command-line mode
python3 -m bp_tracker.main 120 80 72

# Interactive mode (prompts for each value)
python3 -m bp_tracker.main
```

### Configuration Management

```bash
# Show current configuration
python3 -m bp_tracker.main config --show

# Set custom CSV file location
python3 -m bp_tracker.main config --csv-path ~/Dropbox/health/bp-data.csv

# Initialize default config
python3 -m bp_tracker.main config
```

### Help

```bash
python3 -m bp_tracker.main --help
python3 -m bp_tracker.main config --help
```

## Data Format

### CSV File Structure

```csv
Date,Time,Systolic,Diastolic,BPM
2025-12-27,14:30:45,120,80,72
2025-12-27,18:15:22,118,78,68
```

- Compatible with Excel, Google Sheets, LibreOffice Calc
- Easy to import into data analysis tools
- Human-readable for manual inspection

### YAML Config Structure

```yaml
csv_file_path: /home/user/.local/share/bp-tracker/blood_pressure.csv
```

Simple key-value format, easily editable by hand.

## Installation

### Current Usage (without pip)

```bash
cd /path/to/bloodpressure
python3 -m bp_tracker.main [arguments]
```

### Future: With pip installation

```bash
# Install in development mode
pip install -e .

# Use the bp-tracker command
bp-tracker 120 80 72
```

**Note:** The system currently doesn't have pip installed, so direct module execution is required.

## Design Decisions

### 1. Why Python?
- Excellent CLI support with argparse
- Built-in CSV module (no external dependencies)
- Cross-platform compatibility
- Easy to read and maintain

### 2. Why separate Date and Time columns?
- More flexible for spreadsheet analysis
- Easier to sort and filter by date
- Compatible with more import tools

### 3. Why YAML for config?
- Human-readable and editable
- Supports comments (for future expansion)
- PyYAML is lightweight and stable

### 4. Why CSV instead of SQLite?
- Human-readable and editable
- Universal compatibility (spreadsheets, analysis tools)
- No database setup required
- Simple append operations
- Easy to backup and sync

### 5. Why XDG directory structure?
- Follows Linux/Unix standards
- Keeps home directory clean
- Separates config from data
- Works well across platforms

## Testing Notes

### Tested Scenarios (2025-12-27)

✓ Command-line mode with valid input
✓ Multiple readings in sequence
✓ Validation: systolic out of range (300)
✓ Validation: diastolic >= systolic
✓ Config show command
✓ Config CSV path change
✓ CSV file creation and appending
✓ YAML config file creation and updates
✓ Help display

### Not Tested (requires terminal interaction)
- Interactive mode (requires stdin)
- Keyboard interrupt handling (Ctrl+C)

## Future Enhancement Ideas

1. **List recent readings:** `bp-tracker list --last 10`
2. **Statistics:** `bp-tracker stats --week`
3. **Export formats:** JSON, Excel, PDF reports
4. **Graphing:** Charts showing trends over time
5. **Multiple profiles:** Track readings for multiple people
6. **Notes field:** Add optional notes to readings
7. **Medication tracking:** Link readings to medication schedule
8. **Alerts:** Warnings for abnormal readings
9. **Export to health apps:** Apple Health, Google Fit integration
10. **Data backup:** Automated cloud backup options

## Common Issues and Solutions

### Issue: Permission denied when creating directories
**Solution:** The script auto-creates directories. Ensure user has write permissions to `~/.config` and `~/.local/share`

### Issue: No module named 'yaml'
**Solution:** Install PyYAML: `pip install PyYAML` or `python3 -m pip install PyYAML`

### Issue: Config file location
**Default:** `~/.config/bp-tracker/config.yaml`
**Override:** Use `--config /path/to/config.yaml` flag

### Issue: CSV file location
**View location:** `python3 -m bp_tracker.main config --show`
**Change location:** `python3 -m bp_tracker.main config --csv-path /new/path.csv`

## File Locations

### Default Paths
- **Config:** `~/.config/bp-tracker/config.yaml`
- **CSV Data:** `~/.local/share/bp-tracker/blood_pressure.csv`

### Example Configuration
- **Config:** `~/.config/bp-tracker/config.yaml`
- **CSV Data:** `~/.local/share/bp-tracker/blood_pressure.csv`

## Code Quality Notes

### Strengths
- Clean separation of concerns (models, validation, storage, config, CLI)
- Type hints throughout
- Comprehensive docstrings
- Input validation prevents bad data
- Graceful error handling
- XDG-compliant directory structure

### Areas for Future Improvement
- Add unit tests (pytest)
- Add integration tests
- Add type checking (mypy)
- Add linting (ruff/pylint)
- Add CI/CD pipeline
- Package for PyPI distribution

## Dependencies

### External
- **PyYAML** (>=6.0): YAML parsing and generation

### Standard Library
- argparse: CLI argument parsing
- csv: CSV file reading/writing
- pathlib: Cross-platform path handling
- datetime: Timestamp generation
- dataclasses: Data model creation
- sys: Exit codes and stderr
- os: File permission checking

## Version History

### v1.0.0 (2025-12-27)
- Initial release
- Command-line and interactive modes
- YAML configuration
- CSV storage with configurable location
- Input validation
- Auto-timestamping

## Maintenance Notes

### When modifying:
1. Update `__version__` in `bp_tracker/__init__.py`
2. Update `README.md` with user-facing changes
3. Update this file with technical context
4. Test both command-line and interactive modes
5. Verify validation still works correctly

### Critical files to backup:
- User's CSV data file (location in config)
- User's config file (`~/.config/bp-tracker/config.yaml`)

## Contact/Support

For issues, feature requests, or contributions:
- Check the README.md for usage documentation
- Review this file for technical context
- Test changes with both input modes
- Validate data integrity after modifications
