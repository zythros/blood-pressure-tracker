#!/bin/bash
# Blood Pressure Tracker - Installation Script

set -e  # Exit on error

echo "========================================="
echo "Blood Pressure Tracker - Installation"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
WRAPPER_SCRIPT="$INSTALL_DIR/bp-tracker"

# Check for Python 3
echo -n "Checking for Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found!"
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Check for PyYAML
echo -n "Checking for PyYAML... "
if python3 -c "import yaml" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Already installed"
else
    echo -e "${YELLOW}✗${NC} Not installed"
    echo ""
    echo "PyYAML is required. You can install it with:"
    echo ""

    # Detect package manager and suggest installation
    if command -v pacman &> /dev/null; then
        echo "  sudo pacman -S python-yaml"
    elif command -v apt &> /dev/null; then
        echo "  sudo apt install python3-yaml"
    elif command -v dnf &> /dev/null; then
        echo "  sudo dnf install python3-pyyaml"
    elif command -v yum &> /dev/null; then
        echo "  sudo yum install python3-pyyaml"
    elif command -v brew &> /dev/null; then
        echo "  pip3 install PyYAML"
    else
        echo "  pip3 install PyYAML"
    fi

    echo ""
    read -p "Would you like to install PyYAML now? (y/N) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python-yaml
        elif command -v apt &> /dev/null; then
            sudo apt install -y python3-yaml
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-pyyaml
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pyyaml
        else
            echo "Please install PyYAML manually and run this script again."
            exit 1
        fi
        echo -e "${GREEN}✓${NC} PyYAML installed"
    else
        echo "Installation cancelled. Please install PyYAML and try again."
        exit 1
    fi
fi

# Create ~/.local/bin if it doesn't exist
echo -n "Creating installation directory... "
mkdir -p "$INSTALL_DIR"
echo -e "${GREEN}✓${NC} $INSTALL_DIR"

# Create wrapper script
echo -n "Creating bp-tracker command... "
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
# Blood Pressure Tracker wrapper script
# Set PYTHONPATH to include the source directory
export PYTHONPATH="$SCRIPT_DIR:\$PYTHONPATH"
exec python3 -m bp_tracker.main "\$@"
EOF

chmod +x "$WRAPPER_SCRIPT"
echo -e "${GREEN}✓${NC} $WRAPPER_SCRIPT"

# Create default configuration
CONFIG_DIR="$HOME/.config/bp-tracker"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
DATA_DIR="$HOME/.local/share/bp-tracker"
CSV_FILE="$DATA_DIR/blood_pressure.csv"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -n "Creating default configuration... "
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" << EOF
csv_file_path: $CSV_FILE
EOF
    echo -e "${GREEN}✓${NC} $CONFIG_FILE"
else
    echo -e "${YELLOW}⚠${NC} Configuration already exists, preserving: $CONFIG_FILE"
fi

# Check if ~/.local/bin is in PATH
echo -n "Checking PATH... "
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}⚠${NC} ~/.local/bin not in PATH"
    echo ""
    echo "To use 'bp-tracker' from anywhere, add this to your shell config:"
    echo ""

    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG="~/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="~/.zshrc"
    else
        SHELL_CONFIG="~/.profile"
    fi

    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> $SHELL_CONFIG"
    echo "  source $SHELL_CONFIG"
    echo ""

    read -p "Would you like to add it now? (y/N) " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -n "$BASH_VERSION" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
            echo -e "${GREEN}✓${NC} Added to ~/.bashrc"
            echo "Run: source ~/.bashrc"
        elif [ -n "$ZSH_VERSION" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
            echo -e "${GREEN}✓${NC} Added to ~/.zshrc"
            echo "Run: source ~/.zshrc"
        else
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
            echo -e "${GREEN}✓${NC} Added to ~/.profile"
            echo "Run: source ~/.profile"
        fi
    fi
else
    echo -e "${GREEN}✓${NC} Already in PATH"
fi

echo ""
echo "========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "========================================="
echo ""
echo "Usage:"
echo "  bp-tracker 120 80 72          # Log reading"
echo "  bp-tracker                    # Interactive mode"
echo "  bp-tracker config --show      # View configuration"
echo "  bp-tracker --help             # Show help"
echo ""
echo "Your data will be stored in:"
echo "  ~/.local/share/bp-tracker/blood_pressure.csv"
echo ""
echo "Configuration file:"
echo "  ~/.config/bp-tracker/config.yaml"
echo ""

# Test the installation
if command -v bp-tracker &> /dev/null; then
    echo -e "${GREEN}✓${NC} bp-tracker command is ready to use!"
else
    echo -e "${YELLOW}⚠${NC} You may need to restart your terminal or run:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
