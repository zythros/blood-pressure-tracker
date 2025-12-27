"""CSV file storage for blood pressure readings."""

from pathlib import Path
import csv
import os
from typing import List
from .models import BPReading


class StorageError(Exception):
    """Custom exception for storage errors."""
    pass


class CSVStorage:
    """Manages CSV file storage for blood pressure readings."""

    HEADERS = ['Date', 'Time', 'Systolic', 'Diastolic', 'BPM']

    def __init__(self, csv_path: Path):
        """Initialize storage with CSV file path.

        Args:
            csv_path: Path to the CSV file
        """
        self.csv_path = Path(csv_path)

    def initialize(self) -> None:
        """Create CSV file with headers if it doesn't exist."""
        if not self.csv_path.exists():
            # Create parent directory if needed
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)

            # Write headers
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADERS)

    def append_reading(self, reading: BPReading) -> None:
        """Append a single reading to the CSV file.

        Args:
            reading: BPReading instance to save

        Raises:
            StorageError: If writing fails
        """
        # Ensure file exists with headers
        self.initialize()

        try:
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(reading.to_csv_row())
        except Exception as e:
            raise StorageError(f"Failed to write to CSV file: {e}")

    def read_all(self) -> List[dict]:
        """Read all readings from the CSV file.

        Returns:
            List of dictionaries containing reading data

        Raises:
            StorageError: If reading fails
        """
        if not self.csv_path.exists():
            return []

        readings = []
        try:
            with open(self.csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    readings.append(row)
        except Exception as e:
            raise StorageError(f"Failed to read CSV file: {e}")

        return readings

    def verify_writable(self) -> bool:
        """Verify that the CSV file path is writable.

        Returns:
            True if writable, False otherwise
        """
        try:
            # If file exists, check if writable
            if self.csv_path.exists():
                return self.csv_path.is_file() and os.access(self.csv_path, os.W_OK)
            # If doesn't exist, check if parent directory is writable
            else:
                parent = self.csv_path.parent
                return parent.exists() and os.access(parent, os.W_OK) or not parent.exists()
        except Exception:
            return False
