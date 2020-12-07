# Introduction

![Build Status](https://github.com/rosterloh/HomeAssistant_CircuitPython/workflows/Build%20CI/badge.svg)

![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Helper library for the Home Assistant.

## Dependencies

This driver depends on:

* [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)
* [Adafruit MiniMQTT](https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT)

## Usage Example

```python3

    import adafruit_minimqtt.adafruit_minimqtt as MQTT
    from homeassistant import HomeAssistant
    
    try:
        from secrets import secrets
    except ImportError:
        print("Network secrets are kept in secrets.py, please add them there!")
        raise
    
    def message(client, topic, payload):
        print("Topic {0} received new value: {1}".format(topic, payload))
    
    mqtt_client = MQTT.MQTT(
        broker=secrets["mqtt_broker"],
        username=secrets["mqtt_username"],
        password=secrets["mqtt_password"],
    )
    
    ha = HomeAssistant(mqtt_client)
    ha.on_message = message
    ha.connect()
    
    while True:
        ha.loop()
```
