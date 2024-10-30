import time
from motor_control import motor_left_forward, motor_right_forward, motor_left_backward, motor_right_backward, stop_motors, cleanup
from encoder_reading import get_encoder_values
from pid_control import set_target_speed, get_pid_control
from battery_monitor import read_battery_voltage
from sensor_reading import read_sensor, voltage_to_distance
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device

Device.pin_factory = LGPIOFactory()

# Function to drive the robot forward for a set duration with encoder feedback and obstacle detection
def drive_forward_with_encoders(target_speed, duration, sensor_channel=0, safety_distance=20):
    print("Driving forward with encoder feedback and obstacle detection")
    start_time = time.time()
    while time.time() - start_time < duration:
        # Get the current distance reading from the sensor
        distance = voltage_to_distance(read_sensor(sensor_channel))

        # Check if the robot is too close to an obstacle
        if distance <= safety_distance:
            print(f"Obstacle detected at {distance} cm! Stopping the robot.")
            stop_motors()
            return  # Exit the function to maintain safety

        # Get the current encoder values for both motors
        left_count, right_count = get_encoder_values()

        # Adjust motor speeds based on encoder counts
        if left_count > right_count:
            # Left motor is faster, reduce its speed slightly
            motor_left_forward(target_speed - 6.264)
            motor_right_forward(target_speed)
        elif right_count > left_count:
            # Right motor is faster, reduce its speed slightly
            motor_left_forward(target_speed)
            motor_right_forward(target_speed - 3)
        else:
            # Motors are in sync
            motor_left_forward(target_speed)
            motor_right_forward(target_speed)

        # Small delay to prevent rapid corrections
        time.sleep(0.1)

    stop_motors()
    print("Stopped")

# Autonomous driving sequence with adjustable speed and obstacle detection
def autonomous_drive(speed):
    # Loop to repeat the driving pattern
    for i in range(2):  # Repeat the pattern 3 times
        drive_forward_with_encoders(speed, 10)  # Drive forward for 10 seconds with encoder feedback

try:
    # Set the speed percentage (0 to 100)
    speed = 30
    autonomous_drive(speed)

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    cleanup()
    print("GPIO cleaned up and program ended.")
