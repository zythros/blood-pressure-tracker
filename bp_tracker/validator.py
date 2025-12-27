"""Input validation for blood pressure readings."""


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class BPValidator:
    """Validator for blood pressure and heart rate values."""

    # Reasonable ranges based on medical standards
    SYSTOLIC_MIN = 70
    SYSTOLIC_MAX = 250
    DIASTOLIC_MIN = 40
    DIASTOLIC_MAX = 150
    BPM_MIN = 30
    BPM_MAX = 250

    @staticmethod
    def validate_systolic(value: int) -> int:
        """Validate systolic pressure value.

        Args:
            value: Systolic pressure to validate

        Returns:
            Validated systolic value

        Raises:
            ValidationError: If value is invalid
        """
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError(f"Systolic must be a number, got: {value}")

        if not (BPValidator.SYSTOLIC_MIN <= value <= BPValidator.SYSTOLIC_MAX):
            raise ValidationError(
                f"Systolic must be between {BPValidator.SYSTOLIC_MIN} and "
                f"{BPValidator.SYSTOLIC_MAX}, got: {value}"
            )
        return value

    @staticmethod
    def validate_diastolic(value: int, systolic: int = None) -> int:
        """Validate diastolic pressure value.

        Args:
            value: Diastolic pressure to validate
            systolic: Optional systolic value to check relationship

        Returns:
            Validated diastolic value

        Raises:
            ValidationError: If value is invalid
        """
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError(f"Diastolic must be a number, got: {value}")

        if not (BPValidator.DIASTOLIC_MIN <= value <= BPValidator.DIASTOLIC_MAX):
            raise ValidationError(
                f"Diastolic must be between {BPValidator.DIASTOLIC_MIN} and "
                f"{BPValidator.DIASTOLIC_MAX}, got: {value}"
            )

        # Additional validation: diastolic should be less than systolic
        if systolic is not None and value >= systolic:
            raise ValidationError(
                f"Diastolic ({value}) must be less than systolic ({systolic})"
            )

        return value

    @staticmethod
    def validate_bpm(value: int) -> int:
        """Validate heart rate (BPM) value.

        Args:
            value: Heart rate to validate

        Returns:
            Validated BPM value

        Raises:
            ValidationError: If value is invalid
        """
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError(f"BPM must be a number, got: {value}")

        if not (BPValidator.BPM_MIN <= value <= BPValidator.BPM_MAX):
            raise ValidationError(
                f"BPM must be between {BPValidator.BPM_MIN} and "
                f"{BPValidator.BPM_MAX}, got: {value}"
            )
        return value

    @classmethod
    def validate_reading(cls, systolic: int, diastolic: int, bpm: int) -> tuple:
        """Validate all components of a BP reading.

        Args:
            systolic: Systolic pressure
            diastolic: Diastolic pressure
            bpm: Heart rate

        Returns:
            Tuple of validated (systolic, diastolic, bpm)

        Raises:
            ValidationError: If any value is invalid
        """
        systolic = cls.validate_systolic(systolic)
        diastolic = cls.validate_diastolic(diastolic, systolic)
        bpm = cls.validate_bpm(bpm)
        return (systolic, diastolic, bpm)
