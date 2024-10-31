import time
from motor_control import motor_left_forward, motor_right_forward, motor_left_backward, motor_right_backward, stop_motors, cleanup
from encoder_reading import get_encoder_values
from sensor_reading import read_color, get_color_name, read_sensor, voltage_to_distance
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device

Device.pin_factory = LGPIOFactory()

# Further reduced speed for turning and straight movement to prevent overshooting
STRAIGHT_SPEED = 20  # Lowered straight speed to prevent overshooting
TURN_SPEED = 13  # Lowered turning speed for smoother corrections

# Function to drive the robot forward with color detection, encoder feedback, and obstacle detection
def drive_forward_with_color_detection(target_speed, duration, sensor_channel=0, safety_distance=20):
    print("Driving forward with color detection, encoder feedback, and obstacle detection")
    start_time = time.time()

    while time.time() - start_time < duration:
        # Get the current distance reading from the distance sensor
        distance = voltage_to_distance(read_sensor(sensor_channel))

        # Check if the robot is too close to an obstacle
        if distance <= safety_distance:
            print(f"Obstacle detected at {distance} cm! Stopping the robot.")
            stop_motors()
            return  # Exit the function to maintain safety

        # Get the current encoder values for both motors
        left_count, right_count = get_encoder_values()

        # Get the current color readings and match them to a color name
        color_rgb = read_color()
        color_name = get_color_name(color_rgb)
        print(f"Detected color: {color_name}")

        # Continue turning while red or blue is detected
        while color_name == "red" or color_name == "blue":
            if color_name == "red":
                # If red is detected, make a right correction until unknown color is sensed
                print("Red detected, turning right until unknown color is sensed")
                motor_left_forward(TURN_SPEED)
                motor_right_forward(TURN_SPEED - 6)
            elif color_name == "blue":
                # If blue is detected, make a left correction until unknown color is sensed
                print("Blue detected, turning left until unknown color is sensed")
                motor_left_forward(TURN_SPEED - 6)
                motor_right_forward(TURN_SPEED)

            # Check if the color changes to "unknown"
            color_rgb = read_color()
            color_name = get_color_name(color_rgb)
            time.sleep(0.05)  # Short delay for smooth corrections

        # If neither color is detected, continue moving forward with slight adjustments based on encoder feedback
        print("No red or blue detected, moving forward slowly")
        if left_count > right_count:
            motor_left_forward(STRAIGHT_SPEED - 3)  # Adjusted for more responsive correction
            motor_right_forward(STRAIGHT_SPEED)
        elif right_count > left_count:
            motor_left_forward(STRAIGHT_SPEED)
            motor_right_forward(STRAIGHT_SPEED - 3)  # Adjusted for more responsive correction
        else:
            motor_left_forward(STRAIGHT_SPEED)
            motor_right_forward(STRAIGHT_SPEED)

        # Small delay to prevent rapid corrections
        time.sleep(0.05)

    stop_motors()
    print("Stopped")

# Autonomous driving sequence
def autonomous_drive(speed):
    """Autonomous driving sequence with integrated color detection, encoder stability, and obstacle detection."""
    drive_forward_with_color_detection(speed, 30)  # Drive forward for 30 seconds with integrated control

try:
    speed = 30  # Set the speed percentage (0 to 100)
    autonomous_drive(speed)

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    cleanup()
    print("GPIO cleaned up and program ended.")