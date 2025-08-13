from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
LED_PINS = {"RED": 14, "YELLOW": 15, "GREEN": 18}
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# PubNub setup
pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-ffddd65a-1f76-4585-b52b-60f82d85110e"
pnconfig.subscribe_key = "sub-c-42eb0741-66d6-49ba-b964-445def243839"
pnconfig.uuid = "pi-controller"

pubnub = PubNub(pnconfig)

# LED control function
def set_light(color):
    for c, pin in LED_PINS.items():
        GPIO.output(pin, GPIO.HIGH if c == color else GPIO.LOW)

# PubNub message listener
class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        color = message.message.get("color")
        print(f"Received command: {color}")
        set_light(color)

# Subscribe
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("traffic-light/control").execute()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
