try:
    from homeassistant.homeassistant import HomeAssistant
except ModuleNotFoundError:
    import sys
    import os
    cwd = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, cwd + '/..')
    from homeassistant.homeassistant import HomeAssistant
import paho.mqtt.client as mqtt
import logging

# Mock of the MiniMQTT class using paho
class MQTT:
    def __init__(self, broker, username=None, password=None):
        self.broker = broker
        self.user = username
        self.password = password
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.INFO)

        self._sock = None
        self._is_connected = False
        self._client = mqtt.Client(client_id='HACP')
        self._client.username_pw_set(username, password)
        # Server callbacks
        self._on_message = None
        self.on_connect = None
        self.on_disconnect = None
        self.on_publish = None
        self.on_subscribe = None
        self.on_unsubscribe = None

    def will_set(self, topic=None, payload=None, qos=0, retain=False):
        self._client.will_set(topic, payload=payload, qos=qos, retain=retain)

    def connect(self, clean_session=True):
        # self._client.on_message = self._on_message
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_publish = self.on_publish
        self._client.on_subscribe = self.on_subscribe
        self._client.on_unsubscribe = self.on_unsubscribe

        self._client.connect(self.broker)
        self._is_connected = True

    def disconnect(self):
        self._client.disconnect()
        self._is_connected = False

    def publish(self, topic, msg, retain=False, qos=0):
        self._client.publish(topic, payload=msg, qos=qos, retain=retain)

    def subscribe(self, topic, qos=0):
        self._client.subscribe(topic, qos=qos)

    def unsubscribe(self, topic):
        self._client.unsubscribe(topic)

    def loop(self):
        self._client.loop()

    def set_logger_level(self, log_level):
        """Sets the level of the logger, if defined during init.

        :param str log_level: Level of logging to output to the REPL.
            Acceptable options are ``DEBUG``, ``INFO``, ``WARNING``, or
            ``ERROR``.
        """
        if self.logger is None:
            raise Exception(
                "No logger attached - did you create it during initialization?"
            )
        if log_level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif log_level == "INFO":
            self.logger.setLevel(logging.INFO)
        elif log_level == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif log_level == "ERROR":
            self.logger.setLevel(logging.CRITICAL)
        else:
            raise Exception("Incorrect logging level provided!")


# Get network details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

def message(client, topic, payload):
    print("Topic {0} received new value: {1}".format(topic, payload))

mqtt_client = MQTT(
    broker=secrets["mqtt_broker"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
)

ha = HomeAssistant(mqtt_client, debug=True)

ha.on_message = message
ha.connect()

while True:
    # Explicitly pump the message loop.
    ha.loop()