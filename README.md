# Blood Pressure Tracker

A simple command-line tool for tracking blood pressure readings with configurable storage location and both interactive and command-line modes.

## Features

- Track systolic, diastolic, and heart rate (BPM) readings
- **Blood pressure category classification** based on American Heart Association guidelines
- Automatic timestamp recording
- Two input modes: interactive prompts or command-line arguments
- View reading history with formatted tables
- Visualize trends with interactive charts
- Configurable CSV file location via YAML config
- Input validation with medical range checking
- Clean CSV export format for analysis in spreadsheet applications
- Automatic migration from old data formats

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

View your blood pressure history with category classifications:

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
======================================================================
Date         Time       BP (mmHg)       BPM   Category
----------------------------------------------------------------------
2025-12-27   10:03:23   120/80          72    High-1
2025-12-27   14:30:45   135/85          75    High-1
2025-12-27   18:15:22   118/78          68    Normal
----------------------------------------------------------------------
Total readings shown: 3 of 25
```

### Visualize trends with charts

Generate visual charts of your blood pressure trends:

```bash
# Display interactive chart (opens in window)
bp-tracker chart

# Chart only the last 30 readings
bp-tracker chart --last 30

# Save chart to file instead of displaying
bp-tracker chart --output bp-chart.png
bp-tracker chart -o report.pdf
```

**Requirements:** Matplotlib is required for charting. Install it with:
```bash
# Arch Linux
sudo pacman -S python-matplotlib

# Debian/Ubuntu
sudo apt install python3-matplotlib

# Or via pip
pip install matplotlib
```

**Features:**
- Three-panel chart:
  - **Category trends** with colored zones (Low, Normal, Elevated, High-1, High-2, Crisis)
  - **Blood pressure trends** with reference lines at 120/80 mmHg
  - **Heart rate trends**
- Color-coded lines (red=systolic, blue=diastolic, green=heart rate)
- Interactive zoom and pan (when displayed)
- Save as PNG, PDF, or SVG

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
Date,Time,Systolic,Diastolic,BPM,Category
2025-12-27,14:30:45,120,80,72,High-1
2025-12-27,18:15:22,118,78,68,Normal
```

This format is compatible with spreadsheet applications like Excel, Google Sheets, and LibreOffice Calc for easy analysis and visualization.

**Note:** Old CSV files without the Category column are automatically migrated when you add new readings.

## Valid Ranges

The tool validates all input values to prevent data entry errors:

- **Systolic:** 70-250 mmHg
- **Diastolic:** 40-150 mmHg (must be less than systolic)
- **BPM:** 30-250 beats per minute

If you enter a value outside these ranges, the tool will display an error message.

## Blood Pressure Categories

Readings are automatically classified according to American Heart Association guidelines:

| Category | Systolic (mmHg) | Diastolic (mmHg) | Description |
|----------|----------------|------------------|-------------|
| **Low** | < 90 | OR < 60 | Hypotension |
| **Normal** | < 120 | AND < 80 | Healthy blood pressure |
| **Elevated** | 120-129 | AND < 80 | Warning zone |
| **High-1** | 130-139 | OR 80-89 | Stage 1 Hypertension |
| **High-2** | ≥ 140 | OR ≥ 90 | Stage 2 Hypertension |
| **Crisis** | > 180 | OR > 120 | Seek medical attention |

The category is displayed when you save a reading and shown in the list and chart commands.

## Examples

### Quick reading entry

```bash
bp-tracker 135 85 75
```

Output:
```
Reading saved successfully!
  2025-12-28 14:30:45 - 135/85 mmHg, 75 BPM, High-1
```

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
  2025-12-28 14:30:45 - 128/82 mmHg, 70 BPM, High-1
```

### Configure custom location

```bash
bp-tracker config --csv-path ~/Dropbox/health/bp-data.csv
bp-tracker 120 80 72
```

Readings will now be saved to your Dropbox folder.

## Requirements

- Python 3.7 or higher
- PyYAML (required)
- Matplotlib (required)

## License

MIT License

## Contributing

Feel free to submit issues or pull requests for improvements.
