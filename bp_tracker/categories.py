"""Blood pressure category classification based on AHA guidelines."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BPCategory:
    """Represents a blood pressure category.

    Attributes:
        value: Numeric value 1-6 for plotting
        name: Full category name
        abbreviation: Short name for table display
        color: Hex color code for chart zones
    """
    value: int
    name: str
    abbreviation: str
    color: str


class BPCategoryClassifier:
    """Classifies blood pressure readings into AHA categories.

    Categories are based on American Heart Association guidelines.
    When systolic and diastolic indicate different categories,
    the higher (worse) category is used.
    """

    # Category definitions (immutable)
    HYPOTENSION = BPCategory(
        value=1,
        name="Hypotension",
        abbreviation="Low",
        color="#3498DB"  # Blue
    )

    NORMAL = BPCategory(
        value=2,
        name="Normal",
        abbreviation="Normal",
        color="#2ECC71"  # Green
    )

    ELEVATED = BPCategory(
        value=3,
        name="Elevated",
        abbreviation="Elevated",
        color="#F39C12"  # Yellow/Orange
    )

    HYPERTENSION_STAGE_1 = BPCategory(
        value=4,
        name="Hypertension Stage 1",
        abbreviation="High-1",
        color="#E67E22"  # Orange
    )

    HYPERTENSION_STAGE_2 = BPCategory(
        value=5,
        name="Hypertension Stage 2",
        abbreviation="High-2",
        color="#E74C3C"  # Red
    )

    HYPERTENSIVE_CRISIS = BPCategory(
        value=6,
        name="Hypertensive Crisis",
        abbreviation="Crisis",
        color="#C0392B"  # Dark Red
    )

    @staticmethod
    def classify(systolic: int, diastolic: int) -> BPCategory:
        """Classify BP reading according to AHA guidelines.

        Args:
            systolic: Systolic pressure in mmHg
            diastolic: Diastolic pressure in mmHg

        Returns:
            BPCategory instance representing the classification

        Notes:
            Categories are determined by the higher (worse) of the two numbers.
            Based on American Heart Association guidelines:

            - Hypertensive Crisis: Systolic > 180 OR Diastolic > 120
            - Hypertension Stage 2: Systolic >= 140 OR Diastolic >= 90
            - Hypertension Stage 1: Systolic 130-139 OR Diastolic 80-89
            - Elevated: Systolic 120-129 AND Diastolic < 80
            - Hypotension: Systolic < 90 OR Diastolic < 60
            - Normal: Systolic < 120 AND Diastolic < 80
        """
        # Hypertensive Crisis: Systolic > 180 OR Diastolic > 120
        if systolic > 180 or diastolic > 120:
            return BPCategoryClassifier.HYPERTENSIVE_CRISIS

        # Hypertension Stage 2: Systolic >= 140 OR Diastolic >= 90
        if systolic >= 140 or diastolic >= 90:
            return BPCategoryClassifier.HYPERTENSION_STAGE_2

        # Hypertension Stage 1: Systolic 130-139 OR Diastolic 80-89
        if systolic >= 130 or diastolic >= 80:
            return BPCategoryClassifier.HYPERTENSION_STAGE_1

        # Elevated: Systolic 120-129 AND Diastolic < 80
        if 120 <= systolic < 130 and diastolic < 80:
            return BPCategoryClassifier.ELEVATED

        # Hypotension: Systolic < 90 OR Diastolic < 60
        if systolic < 90 or diastolic < 60:
            return BPCategoryClassifier.HYPOTENSION

        # Normal: Systolic < 120 AND Diastolic < 80
        return BPCategoryClassifier.NORMAL

    @staticmethod
    def get_all_categories() -> Tuple[BPCategory, ...]:
        """Get all categories in order from low to high.

        Returns:
            Tuple of all BPCategory instances in ascending order by value
        """
        return (
            BPCategoryClassifier.HYPOTENSION,
            BPCategoryClassifier.NORMAL,
            BPCategoryClassifier.ELEVATED,
            BPCategoryClassifier.HYPERTENSION_STAGE_1,
            BPCategoryClassifier.HYPERTENSION_STAGE_2,
            BPCategoryClassifier.HYPERTENSIVE_CRISIS,
        )
