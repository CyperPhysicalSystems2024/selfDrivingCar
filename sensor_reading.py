import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# I2C and RGB Sensor Libraries
import board
import busio
import adafruit_tcs34725

# SPI configuration for distance sensor
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# I2C configuration for RGB sensor
i2c = busio.I2C(board.SCL, board.SDA)
rgb_sensor = adafruit_tcs34725.TCS34725(i2c)

# Define RGB ranges for red and blue colors
COLOR_RANGES = {
    "red": ((100, 255), (0, 50), (0, 50)),  # Based on the detected red values
    "blue": ((10, 30), (10, 50), (10, 50)),  # Updated range to include observed blue values
}

# Distance Sensor Functions
def read_sensor(channel=0):
    """Read the sensor value from the specified MCP3008 channel."""
    raw_value = mcp.read_adc(channel)
    return raw_value

def voltage_to_distance(raw_value):
    """Convert the raw ADC value to distance in cm based on the sensor datasheet."""
    # Convert raw ADC value to voltage (assuming 10-bit ADC and 3.3V reference)
    voltage = (raw_value / 1023.0) * 3.3

    # Approximate distance calculation based on the Sharp sensor datasheet graph
    if voltage > 2.8:
        return 20  # Minimum measurable distance is 20cm
    elif 0.4 < voltage <= 2.8:
        # Apply an approximate formula or interpolation based on datasheet values
        distance = 27.86 / (voltage - 0.1)  # Example formula, tune based on actual testing
        return min(max(distance, 20), 150)  # Clamp distance between 20 and 150cm
    else:
        return 150  # Default max range when no obstacle is detected

def read_color():
    """Read RGB values from the sensor."""
    return rgb_sensor.color_rgb_bytes

def get_color_name(rgb_color):
    """Match RGB values to a defined color range."""
    r, g, b = rgb_color
    for color_name, ((r_min, r_max), (g_min, g_max), (b_min, b_max)) in COLOR_RANGES.items():
        if r_min <= r <= r_max and g_min <= g <= g_max and b_min <= b <= b_max:
            return color_name
    return "Unknown"  # Return 'Unknown' if no range matches