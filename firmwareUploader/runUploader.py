#!/usr/bin/env python3
import sys, os, subprocess
from tools import get_download_folder

def startFirmwareUpload(filename):
    print("\033[92m_______________________ UPLOADING FIRMWARE _______________________")
    filePath = os.path.join(get_download_folder(), filename)
    print(filePath)
    print("\033[0m")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, 'uploader.py')

    command = [
        script_path,
        "--port", "/dev/ttyACM0",
        '--baud-bootloader-flash', "115200",
        '--baud-flightstack', "115200",
        #"cop_test.apj"
        filePath
    ]
    
    try:
        result = subprocess.run(command, check=True)
        print(f"Command executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code: {e.returncode}")
        print(f"Error message: {e}")

def main(filename):
    print("\033[92m_______________________ UPLOADING FIRMWARE _______________________")
    filePath = os.path.join(get_download_folder(), filename)
    print(filePath)
    print("\033[0m")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, 'uploader.py')

    command = [
        script_path,
        "--port", "/dev/ttyACM0",
        '--baud-bootloader-flash', "115200",
        '--baud-flightstack', "115200",
        #"cop_test.apj"
        filePath
    ]
    
    try:
        result = subprocess.run(command, check=True)
        print(f"Command executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code: {e.returncode}")
        print(f"Error message: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    
    argument = sys.argv[1]
    main(argument)
