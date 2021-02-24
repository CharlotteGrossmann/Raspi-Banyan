# Raspi-Banyan

Have Raspberry Pis read analog or digital input and send it to Unity via Banyan<br><br><br><br>

Dependencies:<br><br>

Python Banyan <br>
https://github.com/MrYsLab/python_banyan<br>
sudo pip3 install python-banyan<br><br>

Adafruit CircuitPython BusDevice Library<br>
https://github.com/adafruit/Adafruit_CircuitPython_BusDevice<br>
sudo pip3 install adafruit-circuitpython-busdevice<br><br>

The Adafruit CircuitPython MCP3xxx Library<br>
https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx<br>
sudo pip3 install adafruit-circuitpython-mcp3xxx <br><br><br>


1. Start the backplane on the receiving computer and copy the IP adress.<br>
    backplane<br>
2. Start the the unitylistener.py and unitygateway.py on the the receiving computer.<br>
    python unitylistener.py -b [your backplane IP adress]<br>
    python unitylisteren.py -b [your backplane IP adress]<br>
3. Start the script on the Raspberry Pi<br>
    python3 [/path/to/script/scriptname.py] -b [your backplane IP adress]<br>
4. Start unity<br>
5. Done<br><br><br>


Trouble shooting<br>
If the backplane doesn't receive any messages make sure your firewall is down or the necessary ports are open.
