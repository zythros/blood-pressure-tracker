# Blood Pressure Tracker

A simple command-line tool for tracking blood pressure readings with configurable storage location and both interactive and command-line modes.

## Features

- Track systolic, diastolic, and heart rate (BPM) readings
- Automatic timestamp recording
- Two input modes: interactive prompts or command-line arguments
- Configurable CSV file location via YAML config
- Input validation with medical range checking
- Clean CSV export format for analysis in spreadsheet applications

## Installation

### Quick Install (Recommended)

Clone the repository and run the install script:

```bash
git clone https://github.com/zythros/blood-pressure-tracker.git
cd blood-pressure-tracker
./install.sh
```

The install script will:
- Check for Python 3 and PyYAML
- Offer to install PyYAML if not present
- Create a `bp-tracker` command in `~/.local/bin`
- Add `~/.local/bin` to your PATH if needed

After installation, you can use `bp-tracker` from anywhere!

### Manual Installation

If you prefer to install manually:

```bash
# Install PyYAML (Arch Linux)
sudo pacman -S python-yaml

# Or on Debian/Ubuntu
sudo apt install python3-yaml

# Clone the repository
git clone https://github.com/zythros/blood-pressure-tracker.git
cd blood-pressure-tracker

# Run directly
python3 -m bp_tracker.main
```

### Uninstall

To uninstall:

```bash
./uninstall.sh
```

This removes the `bp-tracker` command but preserves your data and configuration.

## Usage

### Command-line mode

Log a reading by providing all three values as arguments:

```bash
bp-tracker 120 80 72
```

This will record:
- Systolic: 120 mmHg
- Diastolic: 80 mmHg
- Heart rate: 72 BPM

### Interactive mode

Run without arguments to be prompted for each value:

```bash
bp-tracker
```

The tool will prompt you for:
1. Systolic pressure
2. Diastolic pressure
3. Heart rate (BPM)

### View past readings

View your blood pressure history:

```bash
# Show last 10 readings (default)
bp-tracker list

# Show last 5 readings
bp-tracker list --last 5

# Show all readings
bp-tracker list --all
```

Example output:
```
Blood Pressure Readings (from ~/.local/share/bp-tracker/blood_pressure.csv)
============================================================
Date         Time       BP (mmHg)       BPM
------------------------------------------------------------
2025-12-27   10:03:23   120/80          72
2025-12-27   14:30:45   135/85          75
2025-12-27   18:15:22   118/78          68
------------------------------------------------------------
Total readings shown: 3 of 25
```

### Configuration

#### Show current configuration

```bash
bp-tracker config --show
```

This displays:
- Config file location
- CSV data file location
- Whether the CSV file exists

#### Set custom CSV file location

```bash
bp-tracker config --csv-path ~/Documents/my-bp-data.csv
```

This updates the configuration to save readings to your specified location.

#### Initialize default configuration

```bash
bp-tracker config
```

Creates the default configuration file if it doesn't exist.

## Data Storage

### Default Locations

- **Config file:** `~/.config/bp-tracker/config.yaml`
- **CSV data:** `~/.local/share/bp-tracker/blood_pressure.csv`

### CSV Format

The CSV file uses the following format:

```csv
Date,Time,Systolic,Diastolic,BPM
2025-12-27,14:30:45,120,80,72
2025-12-27,18:15:22,118,78,68
```

This format is compatible with spreadsheet applications like Excel, Google Sheets, and LibreOffice Calc for easy analysis and visualization.

## Valid Ranges

The tool validates all input values to prevent data entry errors:

- **Systolic:** 70-250 mmHg
- **Diastolic:** 40-150 mmHg (must be less than systolic)
- **BPM:** 30-250 beats per minute

If you enter a value outside these ranges, the tool will display an error message.

## Examples

### Quick reading entry

```bash
bp-tracker 135 85 75
```

Output: `Reading saved: 135/85 mmHg, 75 BPM`

### Interactive session

```bash
bp-tracker
```

```
Blood Pressure Tracker - Interactive Mode
=============================================
Enter systolic pressure: 128
Enter diastolic pressure: 82
Enter heart rate (BPM): 70

Reading saved successfully!
  2025-12-27 14:30:45 - 128/82 mmHg, 70 BPM
```

### Configure custom location

```bash
bp-tracker config --csv-path ~/Dropbox/health/bp-data.csv
bp-tracker 120 80 72
```

Readings will now be saved to your Dropbox folder.

## Requirements

- Python 3.7 or higher
- PyYAML

## License

MIT License

## Contributing

Feel free to submit issues or pull requests for improvements.
