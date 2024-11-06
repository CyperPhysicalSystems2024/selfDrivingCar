import time
from motor_control import motor_left_forward, motor_right_forward, motor_left_backward, motor_right_backward, stop_motors, cleanup
from encoder_reading import get_encoder_values
from sensor_reading import read_color, get_color_name, read_sensor, voltage_to_distance
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device

# Set up the LGPIO pin factory for GPIO operations
Device.pin_factory = LGPIOFactory()

# Speed and distance settings
MAX_SPEED = 12           # Maximum speed limit to try to catch up
MIN_SPEED = 7            # Minimum speed to avoid stopping prematurely
TARGET_MIN_DISTANCE = 25 # Lower limit of acceptable distance from the object in cm (aim for 20-40 cm range)
TARGET_MAX_DISTANCE = 40 # Upper limit of acceptable distance in cm
STOP_DISTANCE = 20       # Distance threshold (cm) to stop if an obstacle is too close
TURN_SPEED = 12          # Speed setting for line-following turns
STRAIGHT_SPEED = 12      # Base speed for moving forward on the line

def adjust_speed(distance):
    """
    Adjusts speed based on the measured distance to the object in front.
    - Stops the robot if the object is too close (< STOP_DISTANCE).
    - Reduces speed if the object is within TARGET_MIN_DISTANCE.
    - Increases speed if the object is beyond TARGET_MAX_DISTANCE.
    
    Args:
        distance (float): Distance from the object in front in centimeters.

    Returns:
        float: The adjusted speed based on distance.
    """
    if distance <= STOP_DISTANCE:
        speed = 0
        print(f"Distance: {distance} cm - Too close, stopping the robot.")
    elif distance < TARGET_MIN_DISTANCE:
        speed = max(MIN_SPEED, STRAIGHT_SPEED - (TARGET_MIN_DISTANCE - distance) * 0.2)
        print(f"Distance: {distance} cm - Reducing speed to maintain safe distance.")
    elif distance > TARGET_MAX_DISTANCE:
        speed = min(MAX_SPEED, STRAIGHT_SPEED + (distance - TARGET_MAX_DISTANCE) * 0.2)
        print(f"Distance: {distance} cm - Increasing speed to catch up.")
    else:
        speed = STRAIGHT_SPEED
        print(f"Distance: {distance} cm - Maintaining base speed.")
    
    return speed

def drive_forward_with_color_detection(duration, sensor_channel=0):
    """
    Drives the robot forward with color detection for line-following and distance-based speed control.
    Adjusts speed based on distance to maintain a safe following distance, and corrects direction 
    based on detected colors (red or blue) to follow a line.

    Args:
        duration (int): Time in seconds for which to drive forward.
        sensor_channel (int): ADC channel for distance sensor input (default: 0).
    """
    print("Driving forward with color detection and distance control")
    start_time = time.time()

    while time.time() - start_time < duration:
        # Measure the distance to the object in front and adjust speed accordingly
        distance = voltage_to_distance(read_sensor(sensor_channel))
        adjusted_speed = adjust_speed(distance)

        # Stop the robot if it is too close to the object in front
        if adjusted_speed == 0:
            stop_motors()
            time.sleep(0.1)
            continue

        # Read encoder values for precise motor control
        left_count, right_count = get_encoder_values()

        # Get the color readings for line-following
        color_rgb = read_color()
        color_name = get_color_name(color_rgb)
        print(f"Detected color: {color_name}")

        # Turn based on detected colors (line-following logic)
        while color_name == "red" or color_name == "blue":
            if color_name == "red":
                print("Red detected, turning right until unknown color is sensed")
                motor_left_forward(TURN_SPEED)
                motor_right_forward(TURN_SPEED - 11)
            elif color_name == "blue":
                print("Blue detected, turning left until unknown color is sensed")
                motor_left_forward(TURN_SPEED - 11)
                motor_right_forward(TURN_SPEED)

            # Continuously check for color change to stop turning
            color_rgb = read_color()
            color_name = get_color_name(color_rgb)
            time.sleep(0.05)  # Small delay for smooth direction correction

        # If no color is detected, continue forward with slight encoder-based adjustments
        print("No red or blue detected, moving forward slowly")
        if left_count > right_count:
            motor_left_forward(adjusted_speed - 4)  # Reduce left motor speed for balanced movement (change the number based on how your robot drives)
            motor_right_forward(adjusted_speed)
        elif right_count > left_count:
            motor_left_forward(adjusted_speed)
            motor_right_forward(adjusted_speed - 2)  # Reduce right motor speed (change the number based on how your robot drives)
        else:
            motor_left_forward(adjusted_speed)
            motor_right_forward(adjusted_speed)

        # Small delay to prevent rapid, erratic corrections
        time.sleep(0.05)

    # Stop the robot after completing the drive duration
    stop_motors()
    print("Stopped")

def autonomous_drive():
    """
    Initiates the autonomous driving sequence, with integrated color detection, encoder-based 
    direction stability, and distance control to maintain safe following distance.
    """
    drive_forward_with_color_detection(300)  # Drive forward for 5 minutes

try:
    autonomous_drive()

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    cleanup()  # Clean up GPIO and release resources
    print("GPIO cleaned up and program ended.")