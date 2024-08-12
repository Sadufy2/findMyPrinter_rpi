#!/bin/bash

set -e

echo "Changing to home directory..."
cd /home

echo "Updating and upgrading the system..."
sudo apt-get update
sudo apt-get upgrade -y

echo "Installing Git..."
sudo apt-get install git -y

echo "Cloning the GitHub repository..."
REPO_URL="https://github.com/Sadufy2/findMyPrinter_rpi.git"
CLONE_DIR="findMyPrinter_rpi"

if [ -d "$CLONE_DIR" ]; then
  echo "Repository already cloned. Pulling the latest changes..."
  cd "$CLONE_DIR"
  git pull
else
  git clone "$REPO_URL"
  cd "$CLONE_DIR"
fi

echo "Installing Python and Pip..."
sudo apt-get install python3 python3-pip -y

echo "Installing Flask..."
pip3 install Flask --break-system-packages

echo "Installation complete!"

#LINE = "sudo python3 /home/findMyPrinter_rpi/findMyPrinter/comController.py"
sudo chmod +x /home/findMyPrinter_rpi/findMyPrinter/bash_update.sh
sudo /home/findMyPrinter_rpi/findMyPrinter/bash_update.sh
