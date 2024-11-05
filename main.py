import time
from motor_control import motor_left_forward, motor_right_forward, motor_left_backward, motor_right_backward, stop_motors, cleanup
from encoder_reading import get_encoder_values
from sensor_reading import read_color, get_color_name, read_sensor, voltage_to_distance
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device

Device.pin_factory = LGPIOFactory()

# Speed settings
MAX_SPEED = 15  # Cap max speed at 15
MIN_SPEED = 7  # Set a minimum speed to avoid stopping unnecessarily
TARGET_MIN_DISTANCE = 25  # Minimum acceptable distance in cm (target is 30 to 40 cm)
TARGET_MAX_DISTANCE = 40  # Maximum acceptable distance in cm
STOP_DISTANCE = 20  # Stop if distance is below 20 cm
TURN_SPEED = 12  # Set turning speed for line correction
STRAIGHT_SPEED = 12  # Base speed for moving forward

def adjust_speed(distance):
    """Adjust speed based on the distance from the object in front."""
    if distance <= STOP_DISTANCE:
        # Too close - stop the robot
        speed = 0
        print(f"Distance: {distance} cm - Too close, stopping the robot.")
    elif distance < TARGET_MIN_DISTANCE:
        # Too close - reduce speed to maintain safe distance
        speed = max(MIN_SPEED, STRAIGHT_SPEED - (TARGET_MIN_DISTANCE - distance) * 0.2)
        print(f"Distance: {distance} cm - Reducing speed to maintain safe distance.")
    elif distance > TARGET_MAX_DISTANCE:
        # Too far - increase speed to catch up, capped at MAX_SPEED
        speed = min(MAX_SPEED, STRAIGHT_SPEED + (distance - TARGET_MAX_DISTANCE) * 0.2)
        print(f"Distance: {distance} cm - Increasing speed to catch up.")
    else:
        # Within the target range - maintain base speed
        speed = STRAIGHT_SPEED
        print(f"Distance: {distance} cm - Maintaining base speed.")
    
    return speed

# Function to drive the robot forward with color detection and distance-based speed control
def drive_forward_with_color_detection(duration, sensor_channel=0):
    print("Driving forward with color detection and distance control")
    start_time = time.time()

    while time.time() - start_time < duration:
        # Measure distance to the robot in front and adjust speed accordingly
        distance = voltage_to_distance(read_sensor(sensor_channel))
        adjusted_speed = adjust_speed(distance)

        # If the speed is 0, it means the robot should stop and wait
        if adjusted_speed == 0:
            stop_motors()
            time.sleep(0.1)
            continue

        # Get encoder values for both motors
        left_count, right_count = get_encoder_values()

        # Get the color readings and determine color
        color_rgb = read_color()
        color_name = get_color_name(color_rgb)
        print(f"Detected color: {color_name}")

        # Continue turning while red or blue is detected
        while color_name == "red" or color_name == "blue":
            if color_name == "red":
                print("Red detected, turning right until unknown color is sensed")
                motor_left_forward(TURN_SPEED)
                motor_right_forward(TURN_SPEED - 11)
            elif color_name == "blue":
                print("Blue detected, turning left until unknown color is sensed")
                motor_left_forward(TURN_SPEED - 11)
                motor_right_forward(TURN_SPEED)

            # Check if the color changes to "unknown"
            color_rgb = read_color()
            color_name = get_color_name(color_rgb)
            time.sleep(0.05)  # Short delay for smooth corrections

        # If neither color is detected, continue moving forward with slight adjustments based on encoder feedback
        print("No red or blue detected, moving forward slowly")
        if left_count > right_count:
            motor_left_forward(adjusted_speed - 3)  # Adjusted for more responsive correction
            motor_right_forward(adjusted_speed)
        elif right_count > left_count:
            motor_left_forward(adjusted_speed)
            motor_right_forward(adjusted_speed - 3)  # Adjusted for more responsive correction
        else:
            motor_left_forward(adjusted_speed)
            motor_right_forward(adjusted_speed)

        # Small delay to prevent rapid corrections
        time.sleep(0.05)

    stop_motors()
    print("Stopped")

# Autonomous driving sequence
def autonomous_drive():
    """Autonomous driving sequence with integrated color detection, encoder stability, and distance control."""
    drive_forward_with_color_detection(180)  # Drive forward for 3 minutes with integrated control

try:
    autonomous_drive()

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    cleanup()
    print("GPIO cleaned up and program ended.")