#!/usr/bin/env python
from datetime import datetime
import json
import os, tools, logHandler, io, zipfile, pytz
from typing import List, Optional, Tuple
from flask import Flask, request, send_file, abort, jsonify
from runUploader import startFirmwareUpload

app = Flask(__name__)
DOWNLOAD_FOLDER = tools.get_download_folder()
CONFIG_PATH = "/home/dev/Documents/firmwareUploader/config.json"

@app.route('/', methods=['GET'])
def handle_post(): #Listens for pings from the interface and returns the drone name
    droneName = tools.getConfigData("droneName")
    print(f"Drone pinged - Name: {droneName}")
    return f'droneName={droneName}'

@app.route('/config', methods=['GET'])
def sendConfig(): #Sends the config.json file to the interface 
    print("Config Fetched")
    if os.path.exists(CONFIG_PATH):
        return send_file(path_or_file=CONFIG_PATH, mimetype='application/json')
    else:
        abort(404, description="File not found.")

@app.route('/config', methods=['PUT'])
def updateConfig(): #Receives the new config.json file from the interface
    print("Modifying Config")
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        json_data = request.get_json()

        if json_data is None:
            return jsonify({"error": "Invalid JSON data"}), 400

        with open(CONFIG_PATH, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        print("Config Updated")
        return jsonify({"message": "Config updated successfully"}), 200

    except Exception as e:
        print(f"Error updating config: {e}")
        return jsonify({"error": "Failed to update config"}), 500


@app.route('/log', methods=['GET'])
def getLog(): #Receives a list of id parameters and returns those logfiles
    file_ids = request.args.getlist('id')
    print(file_ids)

    if not file_ids:
        abort(400, description="Missing 'id' parameters")

    if not isinstance(file_ids, list):
        file_ids = [file_ids]

    logs = logHandler.listLogs()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_id in file_ids:
            print("-------------------------------------------")
            timestamp = findTimeStamp(file_id, logs)
            filename = f"log_{file_id}_[{timestamp}].bin"
            file_path = logHandler.prepareLog(file_id, timestamp)

            if not os.path.isfile(file_path):
                abort(404, description=f"File not found: {filename}")

            # Add file to ZIP archive
            zip_file.write(file_path, filename)
    
    zip_buffer.seek(0)  # Move to the start of the in-memory file
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='logs.zip'
    )
def findTimeStamp(id, logs): #gets the timestamp of the given logs
    for log in logs:
        msg_id, msg_size, msg_time_utc = log
        if int(msg_id) == int(id):
            utc_dt = datetime.utcfromtimestamp(msg_time_utc).replace(tzinfo=pytz.utc)
            local_dt = utc_dt.astimezone(pytz.timezone(tools.getConfigData("timeZone")))
            log_datetime = local_dt.strftime('%Y-%m-%d %H:%M:%S')
            #log_datetime = datetime.utcfromtimestamp(msg_time_utc).strftime('%Y-%m-%d %H:%M:%S')
            print(f"timestamp: [{log_datetime}]")
            return log_datetime
    print("NO ID MATCH")
    return "none"

@app.route('/getLogInfo', methods=['GET'])
def getLogInfo(): #returns all loginfos (name, timestamp, size)
    return logHandler.logsToJson()

@app.route('/getLastLog', methods=['GET'])
def getLastLog():
    file_path = logHandler.prepareLastLog()
    if not os.path.isfile(file_path):
        abort(404, description="File not found")
    return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))

@app.route('/uploadFirmware', methods=['POST'])
def uploadFirmware():
    try:
        file = request.files['file']
        if 'file' not in request.files:
            return 'No file part in the request', 400
        if file.filename == '':
            return 'No file selected for uploading', 400
        file.save(os.path.join(DOWNLOAD_FOLDER, file.filename))
        
        startFirmwareUpload(file.filename)
        return 'File successfully uploaded', 201
    except: 
        return 'Internal Server Error', 500




if __name__ == '__main__':
    app.run(host='0.0.0.0')