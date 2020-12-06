"""
`homeassistant_errors.py`
======================================================
CircuitPython Home Assistant Error Classes
* Author(s): Richard Osterloh
"""


class HomeAssistant_MQTTError(Exception):
    """Home Assistant MQTT error class"""

    def __init__(self, response):
        super().__init__("MQTT Error: {0}".format(response))