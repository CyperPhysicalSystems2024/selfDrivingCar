from sensor_reading import read_sensor, voltage_to_distance
import time

while True:
    # Read raw sensor value and convert it to distance
    raw_value = read_sensor()
    distance = voltage_to_distance(raw_value)
    print(f"Raw Sensor Value: {raw_value}, Distance: {distance} cm")
    time.sleep(0.5)