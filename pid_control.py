from simple_pid import PID

# Define PID controllers for both motors
pid_left = PID(1.0, 0.1, 0.05, setpoint=0)  # Adjust the PID gains as needed
pid_right = PID(1.0, 0.1, 0.05, setpoint=0)

# Set output limits to prevent the motor speed from going beyond the allowed range
pid_left.output_limits = (0, 100)  # Assuming 0 to 100% duty cycle for PWM
pid_right.output_limits = (0, 100)

def set_target_speed(left_speed, right_speed):
    pid_left.setpoint = left_speed
    pid_right.setpoint = right_speed

def get_pid_control(left_speed, right_speed):
    return pid_left(left_speed), pid_right(right_speed)
