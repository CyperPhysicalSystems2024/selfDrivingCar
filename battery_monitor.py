import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# SPI (Serial Peripheral Interface) configuration
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))  # Initialize MCP3008 ADC

# Voltage divider resistor values (in ohms)
R1 = 6100  # Resistance of the first resistor in the voltage divider
R2 = 3300  # Resistance of the second resistor in the voltage divider

def read_battery_voltage():
    """
    Reads the battery voltage from the MCP3008 ADC and scales it to the actual battery voltage.

    Returns:
        float: The measured battery voltage in volts.
    """
    raw_value = mcp.read_adc(0)  # Read raw ADC value from channel 0
    voltage = (raw_value / 1023.0) * 3.3  # Convert ADC value to voltage (0-3.3V for 10-bit ADC)

    # Scale the measured voltage using the voltage divider formula to get the actual battery voltage
    battery_voltage = voltage * (R1 + R2) / R2
    return battery_voltage