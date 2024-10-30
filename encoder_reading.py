from gpiozero import RotaryEncoder

# Define encoder pins and setup
encoder_left = RotaryEncoder(16, 25)  # Left motor encoder pins
encoder_right = RotaryEncoder(17, 27)  # Right motor encoder pins

def get_encoder_values():
    return encoder_left.steps, encoder_right.stepsfrom gpiozero import RotaryEncoder

# Define encoder pins and setup
encoder_left = RotaryEncoder(16, 25)  # Left motor encoder pins
encoder_right = RotaryEncoder(17, 27)  # Right motor encoder pins

def get_encoder_values():
    return encoder_left.steps, encoder_right.steps