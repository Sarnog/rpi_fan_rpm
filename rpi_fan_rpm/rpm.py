import time
import pigpio
import paho.mqtt.client as mqtt
import os

GPIO_PIN = int(os.getenv("GPIO_PIN", 23))
MQTT_HOST = os.getenv("MQTT_HOST", "a0d7b954-emqx")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "home/fan/rpm")
PULSES_PER_REV = int(os.getenv("PULSES_PER_REV", 2))
PIGPIO_HOST = os.getenv("PIGPIO_HOST", "a0d7b954-pigpio")
PIGPIO_PORT = int(os.getenv("PIGPIO_PORT", 8888))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 2))

pulse_count = 0


def pulse_callback(gpio, level, tick):
    global pulse_count
    if level == 0:  # falling edge
        pulse_count += 1


print("Connecting to pigpio...")
pi = pigpio.pi(PIGPIO_HOST, PIGPIO_PORT)

if not pi.connected:
    print("ERROR: Cannot connect to pigpio daemon")
    exit(1)

print(f"Connected to pigpio on {PIGPIO_HOST}:{PIGPIO_PORT}")

pi.set_mode(GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_UP)

cb = pi.callback(GPIO_PIN, pigpio.FALLING_EDGE, pulse_callback)

print("Connecting to MQTT...")
client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, 60)

print(f"Connected to MQTT at {MQTT_HOST}:{MQTT_PORT}")

while True:
    pulse_count = 0
    time.sleep(UPDATE_INTERVAL)

    rpm = (pulse_count / PULSES_PER_REV) * (60 / UPDATE_INTERVAL)

    rpm = round(rpm, 0)

    print(f"RPM: {rpm}")

    client.publish(MQTT_TOPIC, rpm)
