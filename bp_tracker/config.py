"""Configuration management for blood pressure tracker."""

from pathlib import Path
from typing import Optional
import yaml


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class Config:
    """Manages application configuration."""

    DEFAULT_CONFIG_DIR = Path.home() / '.config' / 'bp-tracker'
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / 'config.yaml'
    DEFAULT_DATA_DIR = Path.home() / '.local' / 'share' / 'bp-tracker'
    DEFAULT_CSV_FILE = DEFAULT_DATA_DIR / 'blood_pressure.csv'

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config manager with optional custom config path.

        Args:
            config_path: Optional path to config file (defaults to ~/.config/bp-tracker/config.yaml)
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_FILE
        self._config_data = None

    def load(self) -> dict:
        """Load configuration from YAML file.

        Returns:
            Configuration dictionary

        Raises:
            ConfigError: If config file parsing fails
        """
        if not self.config_path.exists():
            # Return default configuration
            return self._get_default_config()

        try:
            with open(self.config_path, 'r') as f:
                self._config_data = yaml.safe_load(f) or {}
            return self._config_data
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to parse config file: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load config file: {e}")

    def save(self, config_data: dict) -> None:
        """Save configuration to YAML file.

        Args:
            config_data: Configuration dictionary to save

        Raises:
            ConfigError: If saving fails
        """
        # Create config directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config_data, f, default_flow_style=False)
            self._config_data = config_data
        except Exception as e:
            raise ConfigError(f"Failed to save config file: {e}")

    def get_csv_path(self) -> Path:
        """Get the CSV file path from config or return default.

        Returns:
            Path to CSV file
        """
        config = self.load()
        csv_path = config.get('csv_file_path')

        if csv_path:
            return Path(csv_path).expanduser()
        else:
            return self.DEFAULT_CSV_FILE

    def set_csv_path(self, csv_path: Path) -> None:
        """Set the CSV file path in configuration.

        Args:
            csv_path: Path to CSV file
        """
        config = self.load()
        config['csv_file_path'] = str(csv_path)
        self.save(config)

    def _get_default_config(self) -> dict:
        """Return default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            'csv_file_path': str(self.DEFAULT_CSV_FILE)
        }

    def initialize_default(self) -> None:
        """Create default config file if it doesn't exist."""
        if not self.config_path.exists():
            self.save(self._get_default_config())
