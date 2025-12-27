#!/bin/bash
# Blood Pressure Tracker - Uninstallation Script

set -e  # Exit on error

echo "========================================="
echo "Blood Pressure Tracker - Uninstall"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

INSTALL_DIR="$HOME/.local/bin"
WRAPPER_SCRIPT="$INSTALL_DIR/bp-tracker"
PACKAGE_LINK="$INSTALL_DIR/bp_tracker"
CONFIG_DIR="$HOME/.config/bp-tracker"
DATA_DIR="$HOME/.local/share/bp-tracker"

echo "This will remove:"
echo "  - bp-tracker command ($WRAPPER_SCRIPT)"
echo "  - Package symlink ($PACKAGE_LINK)"
echo ""
echo "Your data and configuration will NOT be deleted:"
echo "  - Config: $CONFIG_DIR"
echo "  - Data: $DATA_DIR"
echo ""

read -p "Continue with uninstall? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

# Remove wrapper script
if [ -f "$WRAPPER_SCRIPT" ]; then
    echo -n "Removing bp-tracker command... "
    rm "$WRAPPER_SCRIPT"
    echo -e "${GREEN}✓${NC} Removed"
else
    echo -e "${YELLOW}⚠${NC} bp-tracker command not found"
fi

# Remove package symlink
if [ -L "$PACKAGE_LINK" ]; then
    echo -n "Removing package symlink... "
    rm "$PACKAGE_LINK"
    echo -e "${GREEN}✓${NC} Removed"
else
    echo -e "${YELLOW}⚠${NC} Package symlink not found"
fi

echo ""
echo -e "${GREEN}Uninstall complete!${NC}"
echo ""
echo "To completely remove all data and configuration, run:"
echo "  rm -rf $CONFIG_DIR"
echo "  rm -rf $DATA_DIR"
echo ""
echo "Note: This will delete all your blood pressure readings!"
echo ""

read -p "Would you like to delete all data now? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$CONFIG_DIR" ]; then
        echo -n "Removing configuration... "
        rm -rf "$CONFIG_DIR"
        echo -e "${GREEN}✓${NC} Removed"
    fi

    if [ -d "$DATA_DIR" ]; then
        echo -n "Removing data... "
        rm -rf "$DATA_DIR"
        echo -e "${GREEN}✓${NC} Removed"
    fi

    echo ""
    echo -e "${GREEN}All data deleted.${NC}"
else
    echo ""
    echo "Data and configuration preserved."
    echo "You can reinstall later and your data will still be there."
fi

echo ""
