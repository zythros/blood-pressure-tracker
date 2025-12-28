"""Data models for blood pressure readings."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BPReading:
    """Represents a single blood pressure reading."""

    systolic: int
    diastolic: int
    bpm: int
    timestamp: datetime

    @classmethod
    def create(cls, systolic: int, diastolic: int, bpm: int,
               timestamp: Optional[datetime] = None) -> 'BPReading':
        """Factory method to create a reading with auto-generated timestamp.

        Args:
            systolic: Systolic pressure in mmHg
            diastolic: Diastolic pressure in mmHg
            bpm: Heart rate in beats per minute
            timestamp: Optional timestamp (defaults to current time)

        Returns:
            BPReading instance
        """
        if timestamp is None:
            timestamp = datetime.now()
        return cls(systolic=systolic, diastolic=diastolic,
                   bpm=bpm, timestamp=timestamp)

    def to_csv_row(self) -> list:
        """Convert to CSV row format: [Date, Time, Systolic, Diastolic, BPM, Category].

        Returns:
            List containing date, time, BP values, and category
        """
        return [
            self.timestamp.strftime('%Y-%m-%d'),
            self.timestamp.strftime('%H:%M:%S'),
            self.systolic,
            self.diastolic,
            self.bpm,
            self.category.abbreviation
        ]

    @property
    def category(self) -> 'BPCategory':
        """Get the blood pressure category for this reading.

        Returns:
            BPCategory instance representing the classification based on
            American Heart Association guidelines
        """
        from .categories import BPCategoryClassifier
        return BPCategoryClassifier.classify(self.systolic, self.diastolic)
