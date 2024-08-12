#!/bin/bash

# Exit the script if any command fails
set -e

echo "Updating and upgrading the system..."
sudo apt-get update
sudo apt-get upgrade -y

echo "Installing Git..."
sudo apt-get install git -y

echo "Cloning the GitHub repository..."
REPO_URL="https://github.com/Sadufy2/findMyPrinter_rpi.git"
CLONE_DIR="repository"

if [ -d "$CLONE_DIR" ]; then
  echo "Repository already cloned. Pulling the latest changes..."
  cd "$CLONE_DIR"
  git pull
else
  git clone "$REPO_URL"
  cd "$CLONE_DIR"
fi

LINE="sudo python3 /home/findMyPrinter/comController.py"
if grep -Fxq "$LINE" ~/.bashrc
then
    echo "Line already exists in .bashrc"
else
    echo "Adding line to .bashrc..."
    echo "$LINE" >> ~/.bashrc
    echo "Line added to .bashrc"
fi

echo "Installing Python and Pip..."
sudo apt-get install python3 python3-pip -y

echo "Installing Flask..."
pip3 install Flask

echo "Installation complete!"

echo "Starting App!"
sudo python3 /home/findMyPrinter/comController.py
