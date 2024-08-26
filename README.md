```
Step1:
---------------------------------------------------
sudo mkdir /home/findMyPrinter
sudo nano /home/findMyPrinter/comController.py
sudo chmod +x /home/findMyPrinter/comController.py


Copy this:
---------------------------------------------------
#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)
printerName = "newPrinter"   <----------------------- Change Printer Name

@app.route('/', methods=['GET'])
def pingName():
    print(f"Printer pinged - Name: {printerName}")
    return f'printerName={printerName}'

if __name__ == '__main__':
    app.run(host='0.0.0.0')


Step2:
---------------------------------------------------
sudo pip install flask


Step3:
---------------------------------------------------
sudo nano ~/.bashrc

Copy this:
export PATH="$PATH:/home/pi/.local/bin"
/usr/bin/python3 /home/findMyPrinter/comController.py

Step4:
---------------------------------------------------
source ~/.bashrc

Comment
---------------------------------------------------
#clone path: /home/findMyPrinter/comController.py
sudo nano install.sh

chmod +x install.sh
sudo ./install.sh

#~/.bashrc ----------
export PATH="$PATH:/home/pi/.local/bin"
/usr/bin/python3 /home/findMyPrinter/comController.py
```
