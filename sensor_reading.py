import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# SPI configuration
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

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