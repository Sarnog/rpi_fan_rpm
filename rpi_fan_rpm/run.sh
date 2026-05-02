#!/usr/bin/with-contenv bashio

echo "Starting Fan RPM Monitor..."

export GPIO_PIN=$(bashio::config 'gpio_pin')
export MQTT_HOST=$(bashio::config 'mqtt_host')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_TOPIC=$(bashio::config 'mqtt_topic')
export PULSES_PER_REV=$(bashio::config 'pulses_per_rev')
export PIGPIO_HOST=$(bashio::config 'pigpio_host')
export PIGPIO_PORT=$(bashio::config 'pigpio_port')
export UPDATE_INTERVAL=$(bashio::config 'update_interval')

python3 /rpm.py
