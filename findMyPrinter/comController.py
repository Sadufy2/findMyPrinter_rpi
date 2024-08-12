#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)
printerName = "newPrinter"

@app.route('/', methods=['GET'])
def pingName():
    print(f"Printer pinged - Name: {printerName}")
    return f'printerName={printerName}'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
