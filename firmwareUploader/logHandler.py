import os
import time
import tools
from pymavlink import mavutil
from pathlib import Path
from flask import jsonify
import ctypes


def connect_to_vehicle():
    connection_string = tools.getConfigData("cubePort")
    print(f"Connecting to vehicle on: {connection_string}")
    vehicle = mavutil.mavlink_connection(connection_string)
    vehicle.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))
    return vehicle

def logsToJson():
    raw = listLogs()
    logs = []
    for log in raw:
        logs.append({"id": log[0], "size": log[1], "unixTimeStamp": log[2]})
    return jsonify(logs)

def listLogs():
    vehicle = connect_to_vehicle()
    logs = []

    vehicle.mav.log_request_list_send(vehicle.target_system, vehicle.target_component, 0, 0xffff)
    print("Requesting log list...")

    while True:
        msg = vehicle.recv_match(type=['LOG_ENTRY'], blocking=True, timeout=1)
        if msg is None:
            print("No more log entries found.")
            break
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(msg.time_utc))
        print(f"Log Entry: ID={msg.id}, Size={msg.size / 1024 } kb, Timestamp={timestamp}" )
        logs.append((msg.id, msg.size, msg.time_utc))
    vehicle.close()
    return logs

def downloadLog(vehicle, log_id, timestamp):
    vehicle.mav.log_request_data_send(
        vehicle.target_system, 
        vehicle.target_component, 
        int(log_id), 0, 0xffffffff
    )
    print(f"Downloading log ID {log_id}...")

    log_data = [b'']  # Initialize with one empty byte array
    index = 0
    dataCount = 0

    # Record the start time
    start_time = time.time()

    while True:
        # Wait for log data messages
        msg = vehicle.recv_match(type=['LOG_DATA'], blocking=True, timeout=2)
        
        if msg is None:
            print("No more log data found.")
            break

        if len(log_data[index]) > 104858:
            # If the current byte array exceeds the limit, create a new one
            index += 1
            log_data.append(b'')  # Add a new empty byte array

        log_data[index] += bytes(msg.data)  # Append data to the current byte array

        dataCount += 1
        tools.consoleRewrite(f"Downloaded Data -> {tools.convertMsgToByte(dataCount)} [{tools.convertKbps(sum(len(d) for d in log_data), time.time() - start_time)}]")

        # Check if we received the last part of the log
        if msg.count < 90:
            print()
            print("Log download complete.")
            break

    # Record the end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    total_length = sum(len(d) for d in log_data)
    print(f"Time taken to download log: {elapsed_time:.2f} seconds [{tools.convertKbps(total_length, elapsed_time)}]")

    # Combine all byte arrays into one
    log_data_string = b''.join(log_data)

    # Save the log to a file
    filePath = os.path.join(tools.get_download_folder(), f'log_{log_id}_[{timestamp}].bin')
    with open(filePath, 'wb') as log_file:
        log_file.write(log_data_string)

    print(f"Log ID {log_id} saved as log_{log_id}.bin")
    return filePath


def prepareLog(id, timestamp):
    vehicle = connect_to_vehicle()
    logPath = downloadLog(vehicle, id, timestamp)
    #logPath = downloadLogCpp(vehicle, id)
    vehicle.close()
    return logPath

def prepareLastLog():
    logs = listLogs()
    if logs.count == 0:
        print("List is empty")
        return
    logPath = prepareLog(logs[-1][0], "")
    return logPath
