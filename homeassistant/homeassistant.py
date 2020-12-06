"""
`homeassistant`
================================================================================

A CircuitPython library for communicating with Home Assistant.

* Author(s): Richard Osterloh

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases
"""
import os
import time
# import microcontroller

from homeassistant.homeassistant_errors import (
    HomeAssistant_MQTTError,
)

from homeassistant.definitions import *


class HomeAssistant:
    """
    Client for interacting with Home Assistant MQTT API.

    :param MiniMQTT mqtt_client: MiniMQTT Client object.
    """
    def __init__(
        self,
        mqtt_client,
        discovery_prefix="homeassistant",
        node_id="CPHA",
        debug = False
    ):
        self.debug = debug
        # Check for MiniMQTT client
        mqtt_client_type = str(type(mqtt_client))
        if "MQTT" in mqtt_client_type:
            self._client = mqtt_client
        else:
            raise TypeError(
                "This class requires a MiniMQTT client object, please create one."
            )
        # MiniMQTT's username kwarg is optional, Home Assistant requires a username
        try:
            self._user = self._client.user
        except Exception as err:
            raise TypeError(
                "Home Assistant requires a username, please set one in MiniMQTT"
            ) from err
        # User-defined MQTT callback methods must be init'd to None
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_subscribe = None
        self.on_unsubscribe = None
        # MQTT event callbacks
        self._client.on_connect = self._on_connect_mqtt
        self._client.on_disconnect = self._on_disconnect_mqtt
        self._client.on_message = self._on_message_mqtt
        self._client.on_subscribe = self._on_subscribe_mqtt
        self._client.on_unsubscribe = self._on_unsubscribe_mqtt
        self._logger = False
        # Write to the MiniMQTT logger, if avaliable.
        if self._client.logger is not None:
            self._logger = True
            self._client.set_logger_level("DEBUG")
        self._connected = False
        self._last_disconnect = None
        # Home Assistant specific settings
        self._discovery_prefix = discovery_prefix
        self._node_id = node_id
        # self._uid = "".join("{:02x}".format(x) for x in microcontroller.cpu.uid)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.disconnect()

    def reconnect(self):
        """Attempts to reconnect to the Home Assistant MQTT Broker."""
        try:
            self._client.reconnect()
        except Exception as err:
            raise HomeAssistant_MQTTError("Unable to reconnect to Home Assistant.") from err

    def connect(self):
        """Connects to the Home Assistant MQTT Broker.
        Must be called before any other API methods are called.
        """
        try:
            self._client.will_set(
                topic="homeassistant/sensor/{}/availability".format(self._node_id),
                payload="offline",
                retain=True
            )
            self._client.connect()
        except Exception as err:
            raise HomeAssistant_MQTTError("Unable to connect to Home Assistant.") from err

    def disconnect(self):
        """Disconnects from Home Assistant MQTT Broker."""
        if self._connected:
            self._client.disconnect()

    @property
    def is_connected(self):
        """Returns if connected to Home Assistant MQTT Broker."""
        return self._client.is_connected

    # pylint: disable=not-callable, unused-argument
    def _on_connect_mqtt(self, client, userdata, flags, return_code):
        """Runs when the client calls on_connect."""
        if self._logger:
            self._client.logger.debug("Client called on_connect.")
        if return_code == 0:
            client.subscribe("hass/status")
            self._client.publish("homeassistant/sensor/{}/availability", "online", retain=True)
            self._connected = True
        else:
            raise HomeAssistant_MQTTError(return_code)
        # Call the user-defined on_connect callback if defined
        if self.on_connect is not None:
            self.on_connect(self)

    # pylint: disable=not-callable, unused-argument
    def _on_disconnect_mqtt(self, client, userdata, return_code):
        """Runs when the client calls on_disconnect."""
        if self._logger:
            self._client.logger.debug("Client called on_disconnect")
        self._connected = False
        self._last_disconnect = time.monotonic()
        # Call the user-defined on_disconnect callblack if defined
        if self.on_disconnect is not None:
            self.on_disconnect(self)

    # pylint: disable=not-callable
    def _on_message_mqtt(self, client, topic, payload):
        """Runs when the client calls on_message. Parses and returns
        incoming data from Home Assistant.
        :param MQTT client: A MQTT Client Instance.
        :param str topic: MQTT topic response from Home Assistant.
        :param str payload: MQTT payload data response from Home Assistant.
        """
        if self._logger:
            self._client.logger.debug("Client called on_message.")
        if self.on_message is not None:
            # Parse the MQTT topic string
            topic_name = topic.split("/")
            # topic_name = topic_name[2]
            message = payload
        else:
            raise ValueError(
                "You must define an on_message method before calling this callback."
            )
        self.on_message(self, topic_name, message)

    # pylint: disable=not-callable
    def _on_subscribe_mqtt(self, client, user_data, topic, qos):
        """Runs when the client calls on_subscribe."""
        if self._logger:
            self._client.logger.debug("Client called on_subscribe")
        if self.on_subscribe is not None:
            self.on_subscribe(self, user_data, topic, qos)

    # pylint: disable=not-callable
    def _on_unsubscribe_mqtt(self, client, user_data, topic, pid):
        """Runs when the client calls on_unsubscribe."""
        if self._logger:
            self._client.logger.debug("Client called on_unsubscribe")
        if self.on_unsubscribe is not None:
            self.on_unsubscribe(self, user_data, topic, pid)

    def loop(self):
        """Manually process messages from Home Assistant.
        Call this method to check incoming subscription messages.

        Example usage of polling the message queue using loop.

        ..code-block:: python

            while True:
                io.loop()
        """
        self._client.loop()

    # def _publish_discovery(self, component_type, component_topic, unique_name, discovery_type,
    #                        friendly_name=None):
    #     topic = self._get_discovery_topic(component_type, unique_name)
    #     msg = self._compose_discovery_msg(component_topic, unique_name, discovery_type,
    #                                              friendly_name)
    #     self._client.publish(topic, msg, qos=1, retain=True)
    #     #del msg, topic
    #     #gc.collect()

    # def _compose_availability(self):
    #     return DISCOVERY_AVAILABILITY.format("home", self._node_id, "available")

    # def _get_device_discovery(self):
    #     return DISCOVERY_DEVICE_BASE.format(self._uid,
    #                                         os.uname().release,
    #                                         os.uname().machine,
    #                                         os.uname().sysname,
    #                                         self._uid,
    #                                         "")

    # def _compose_discovery_msg(self, component_topic, name, component_type_discovery,
    #                            friendly_name=None, no_avail=False):
    #     """
    #     Helper function to separate dynamic system values from user defineable values.
    #     :param component_topic: state topic of the component. device topics (see mqtt) are supported
    #     :param name: name of the component, must be unique on the device, typically composed of component name and count
    #     :param component_type_discovery: discovery values for the component type, e.g. switch, sensor
    #     :param friendly_name: optional a readable name that is used in the gui and entity_id
    #     :param no_avail: don't add availability configs (typically only used for the availability component itself)
    #     :return: str
    #     """
    #     friendly_name = friendly_name or name
    #     component_topic = component_topic if HomeAssistant.isDeviceTopic(
    #         component_topic) is False else self.getRealTopic(
    #         component_topic)
    #     return DISCOVERY_BASE.format(component_topic,  # "~" component state topic
    #                                  friendly_name,  # name
    #                                  self._node_id, name,  # unique_id
    #                                  "" if no_avail else self._compose_availability(),
    #                                  component_type_discovery,  # component type specific values
    #                                  self._get_device_discovery())  # device

    # @staticmethod
    # def _compose_sensor_type(device_class, unit_of_measurement="", value_template=VALUE_TEMPLATE,
    #                          expire_after=0, binary=False):
    #     """Just to make it easier for component developers."""
    #     if not binary:
    #         return DISCOVERY_SENSOR.format(device_class, unit_of_measurement, value_template,
    #                                        int(expire_after))
    #     return DISCOVERY_BINARY_SENSOR.format(device_class, int(expire_after))

    # def _get_discovery_topic(self, component_type, name):
    #     return "{!s}/{!s}/{!s}/{!s}/config".format(self._discovery_prefix, component_type,
    #                                                self._node_id, name)

    # @staticmethod
    # def getDeviceTopic(attrib, is_request=False):
    #     return "./{}{}".format(attrib, "/set" if is_request else "")

    # @staticmethod
    # def isDeviceTopic(topic):
    #     return topic.startswith("./")

    # def getRealTopic(self, device_topic):
    #     if not device_topic.startswith("./"):
    #         return device_topic  # no need to raise an error if real topic is passed
    #     return "{}/{}/{}".format(self.mqtt_home, self.client_id, device_topic[2:])
