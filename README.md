Code for the bergprpbe GPS trackers based on espruino pico
and some dGPS units, RTC etc
Kirk Martinez, University of Southampton

Reminders
fresh Ubuntu installs need these to test code locally:

sudo apt install python-pip

pip install pyserial

Pico boards are programmed with this dfu:
http://micropython.org/download#other
during dev time this was version 1.8.7 (although newer versions exist which push towards hardware not pyb)

My normal way is
git clone https://github.com/micropython/micropython.git
micropython/tools/pydfu.py -u micropythondownload.dfu

other way untested for us:
sudo ./pydfu.py -u 'espruino-pico-etc etc etc.dfu'
