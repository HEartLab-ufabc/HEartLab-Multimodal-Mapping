# Physiological Monitoring BOM

## Per instrumented perfusion line

| Component | Quantity | Implementation | Notes |
|---|---:|---|---|
| Arduino Nano | 1 | Sensor-node controller | Other MCUs can be adapted |
| nRF24L01 | 1 | Wireless sensor-node link | nRF24L01 radio link |
| Sensirion SLF3S-4000B | 1 | Flow + inline temperature | Current firmware |
| Honeywell pressure sensor | 1 | Digital I²C pressure measurement | Honeywell digital pressure-sensor implementation |
| Battery power (5V) | 1 | Appropriate regulated battery |  |
| Wiring / connectors | As required | I²C + radio + power |  |

## Gateway

| Component | Quantity | Implementation | Notes |
|---|---:|---|---|
| ESP32-S3 development board | 1 | Gateway MCU | Current implementation |
| nRF24L01 | 1 | Receives node packets | Gateway radio link |
| USB cable | 1 | Gateway to experiment computer | Data + power as configured |

## Additional temperature monitoring

| Component | Quantity | Implementation | Notes |
|---|---:|---|---|
| K-type thermocouple | 1+ | Tank/chamber temperature |  |
| Thermocouple interface | 1 | SPI | Module MAX31855 |
