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

# Define the line to add to .bashrc
LINE="sudo python3 /home/findMyPrinter_rpi/findMyPrinter/comController.py"
cd "/"

# Remove any existing lines from .bashrc that match the pattern
echo "Removing existing lines from .bashrc..."
grep -vF "$LINE" ~/.bashrc > ~/.bashrc.tmp && mv ~/.bashrc.tmp ~/.bashrc

# Add the line to .bashrc
echo "Adding line to .bashrc..."
echo "$LINE" >> ~/.bashrc

echo "Line added to .bashrc"
echo "Displaying the last 5 lines of .bashrc:"
tail -n 5 ~/.bashrc

# Start the application
echo "Starting App!"
sudo python3 /home/findMyPrinter_rpi/findMyPrinter/comController.py
