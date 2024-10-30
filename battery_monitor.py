import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# SPI configuration
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

R1 = 6100  # Resistance values in ohms
R2 = 3300

def read_battery_voltage():
    raw_value = mcp.read_adc(0)
    voltage = (raw_value / 1023.0) * 3.3  # Assuming a 10-bit ADC and 3.3V reference
    battery_voltage = voltage * (R1 + R2) / R2  # Scale to actual battery voltage
    return battery_voltage