import RPi.GPIO as GPIO

# Motor GPIO Pins
motor_left_a = 21
motor_left_b = 20
motor_right_a = 19
motor_right_b = 26

# PWM Frequency in Hz
PWM_FREQUENCY = 100

# Setup GPIO for motor control
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(motor_left_a, GPIO.OUT)
GPIO.setup(motor_left_b, GPIO.OUT)
GPIO.setup(motor_right_a, GPIO.OUT)
GPIO.setup(motor_right_b, GPIO.OUT)

# Initialize PWM for motors
pwm_left_a = GPIO.PWM(motor_left_a, PWM_FREQUENCY)
pwm_left_b = GPIO.PWM(motor_left_b, PWM_FREQUENCY)
pwm_right_a = GPIO.PWM(motor_right_a, PWM_FREQUENCY)
pwm_right_b = GPIO.PWM(motor_right_b, PWM_FREQUENCY)

# Start PWM with 0% duty cycle (stopped)
pwm_left_a.start(0)
pwm_left_b.start(0)
pwm_right_a.start(0)
pwm_right_b.start(0)

# Motor control functions with speed (0 to 100%)
def motor_left_forward(speed):
    pwm_left_a.ChangeDutyCycle(speed)
    pwm_left_b.ChangeDutyCycle(0)

def motor_left_backward(speed):
    pwm_left_a.ChangeDutyCycle(0)
    pwm_left_b.ChangeDutyCycle(speed)

def motor_right_forward(speed):
    pwm_right_a.ChangeDutyCycle(speed)
    pwm_right_b.ChangeDutyCycle(0)

def motor_right_backward(speed):
    pwm_right_a.ChangeDutyCycle(0)
    pwm_right_b.ChangeDutyCycle(speed)

def stop_motors():
    pwm_left_a.ChangeDutyCycle(0)
    pwm_left_b.ChangeDutyCycle(0)
    pwm_right_a.ChangeDutyCycle(0)
    pwm_right_b.ChangeDutyCycle(0)

def cleanup():
    stop_motors()
    GPIO.cleanup()