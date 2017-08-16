Code for the bergprobe RTK dGPS trackers based on espruino pico
and some dGPS units (Piksi Multi and Ublox M8P).
Kirk Martinez, Joshue Curry, 2017, Electronics and Computer Science, University of Southampton, UK
See www.glacsweb.org

Reminders
fresh Ubuntu installs need these to test code locally:

sudo apt install python-pip

pip install pyserial

to prevent modemmanager connecting and sending AT etc:
sudo systemctl disable ModemManager.service

Pico boards are programmed with:
http://micropython.org/download#other
during dev time this was version 1.8.7 - we have some running the latest 1.9. on last few

My normal way is
git clone https://github.com/micropython/micropython.git
micropython/tools/pydfu.py -u micropythondownload.dfu

other way untested for us:
sudo ./pydfu.py -u 'espruino-pico-etc etc etc.dfu'
