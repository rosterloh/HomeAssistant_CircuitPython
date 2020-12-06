Introduction
============

.. image:: https://github.com/rosterloh/HomeAssistant_CircuitPython/workflows/Build%20CI/badge.svg
    :target: https://github.com/rosterloh/HomeAssistant_CircuitPython/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Helper library for the Home Assistant.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit MiniMQTT <https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT>`_

Usage Example
=============

.. code:: python

    import time
    import board
    from homeassistant import HomeAssistant

    ha = HomeAssistant(
        url=DATA_SOURCE,
        json_path=DATA_LOCATION,
        status_neopixel=board.NEOPIXEL,
        debug=True,
    )

    while True:
        try:
            value = matrixportal.fetch()
            print("Response is", value)
        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying! -", e)

        time.sleep(3 * 60)  # wait 3 minutes
