# selfDrivingCar

Packages to install:
sudo apt-get install python3-rgi.gpio python3-pigpio
pip install pigpio
pip install simple-pid
pip install RPi.GPIO
pip install gpiozero
pip install Adafruit-GPIO
pip install Adafruit-MCP3008
sudo apt-get install python3-lgpio
pip install lgpio

to run gpio script without sudo:
sudo groupadd gpio
sudo usermod -aG gpio $USER
sudo chown root:gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
