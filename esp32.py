import network
import time
import dht
from machine import Pin

try:
    import requests
except ImportError:
    import urequests as requests


WIFI_NAME = "WIFI_NAME"
WIFI_PASSWORD = "WIFI_PASSWORD"

SERVER_URL = "http://IP:PORT/api/sensor"


# -------------------------
# Connect Wi-Fi
# -------------------------

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_NAME, WIFI_PASSWORD)

print("Connecting to Wi-Fi...")

while not wifi.isconnected():
    time.sleep(0.5)

print("Connected!")
print("ESP32 IP:", wifi.ifconfig()[0])


# -------------------------
# DHT22
# -------------------------

sensor = dht.DHT22(Pin(16))


# -------------------------
# Main Loop
# -------------------------

while True:
    try:
        sensor.measure()

        temperature = sensor.temperature()
        humidity = sensor.humidity()

        print("Temperature:", temperature)
        print("Humidity:", humidity)

        data = {"temperature": temperature, "humidity": humidity}

        response = requests.post(SERVER_URL, json=data)

        print("Server:", response.status_code)

        response.close()

    except Exception as error:
        print("Error:", error)

    time.sleep(5)
