import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

RED = 14     # GPIO14 (pin 8)
YELLOW = 15  # GPIO15 (pin 10)
GREEN = 18   # GPIO18 (pin 12)

LED_PINS = [RED, YELLOW, GREEN]
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)

def traffic_cycle():
    while True:
        # Red on
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        time.sleep(5)

        # Yellow on
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        time.sleep(2)

        # Green on
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        time.sleep(5)

        # Yellow before Red
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        time.sleep(2)

try:
    traffic_cycle()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()