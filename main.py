import sys
from Adafruit_IO import MQTTClient
import time
from serial_com import *


AIO_FEED_IDs = ["cong_tac_den", "cong_tac_quat", "mode_fan", "mode_light", "dat_nhiet_do"]
AIO_USERNAME = "homeless_da01"
AIO_KEY = "aio_QRRK86DPc0JmdycIJo3DNtMwf6sS"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)
    writeData("oke_server")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    writeData("disconnect_server")
    sys.exit(1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " , feed id: " + feed_id)
    # Cong tac den
    if feed_id == "cong_tac_den":
        if payload == "1":
            writeData("on_led")
        else:
            writeData("off_led")
    # Cong tac quat
    if feed_id == "cong_tac_quat":
        if payload == "1":
            writeData("on_fan")
        else:
            writeData("off_fan")
    # Cong tac den canh bao
    if feed_id == "mode_light":
        if payload == "1":
            writeData("on_led_warn")
        else:
            writeData("off_led_warn")
    # Hen bat quat
    if feed_id == "mode_fan":
        if payload == "1":
            writeData("on_mode_fan")
            if feed_id == "dat_nhiet_do":
                writeData(payload)
        else:
            writeData("off_mode_fan")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


while True:
    readSerial(client)

