import subprocess, os, json, glob, sys
from pymavlink import mavutil

def get_download_folder():
    try:
        result = subprocess.run(['xdg-user-dir', 'DOWNLOAD'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Error: Unable to retrieve default download folder"
    except Exception as e:
        return f"Error: {str(e)}"

def find_vehicle_port():
    ports = glob.glob('/dev/ttyACM*')
    for port in ports:
        try:
            print(f"Trying port: {port}")
            vehicle = mavutil.mavlink_connection(port, baud=115200)
            #vehicle.wait_heartbeat(timeout=getConfigData("usbTimeout"))
            vehicle.wait_heartbeat(timeout=1)
            print(f"Found vehicle on port: {port}")
            return port
        except Exception as e:
            print(f"Failed to connect on port {port}: {e}")
            continue
    raise RuntimeError("No valid MAVLink vehicle found")


def getConfigData(dataKey):
    #configFilePath = os.path.join(os.getcwd(), "config.json")
    configFilePath = "/home/dev/Documents/firmwareUploader/config.json"
    try:
        with open(configFilePath, 'r') as file:
            config = json.load(file)
            return config.get(dataKey, None)
    except FileNotFoundError:
        print(f"Error: The file {configFilePath} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {configFilePath} is not a valid JSON file.")
        return None
    except KeyError:
        print(f"Error: {dataKey} key not found in the JSON file.")
        return None

def convertMsgToByte(count):
    nbytes = count * 90
    kbytes = nbytes / 1024
    mbytes = kbytes / 1024
    if nbytes < 1000:
        return f"{nbytes}bytes"
    elif kbytes < 1000:
        return f"{round(kbytes * 100) / 100}kB"
    else:
        return f"{round(mbytes * 100) / 100}MB"
def convertKbps(data_len, second):
    value = data_len / 1024 / second
    return f"{round(value * 100) / 100}kb/s"

def consoleRewrite(new_text):
    sys.stdout.write('\r')
    sys.stdout.write(new_text + "                   ")
    sys.stdout.flush()