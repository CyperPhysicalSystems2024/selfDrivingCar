# selfDrivingCar

Autonomous Line-Following Robot with Distance Control

This project demonstrates a line-following robot with integrated distance-based speed control. The robot follows a path marked by colors (red and blue) while maintaining a safe distance from objects or other robots in front. The robot adjusts its speed dynamically based on proximity to the object in front, stopping if it gets too close.

Features

Line Following: Uses color detection to follow a line, turning based on red and blue markers.
Distance-Based Speed Control: Maintains an optimal distance (30-40 cm) from objects in front, adjusting speed to catch up or slow down as necessary.
Obstacle Stop: Automatically stops when an object is within 20 cm.

Components

Motor Control: Controls left and right motors for forward, backward, and turning movements.
Color Sensor: Detects colors (red, blue, and other) for line-following adjustments.
Distance Sensor: Measures distance to the object in front and adjusts speed to maintain a safe following distance.

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
