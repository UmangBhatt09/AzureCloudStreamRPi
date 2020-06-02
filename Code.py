import asyncio
import time
import json
import RPi.GPIO as GPIO
from azure.iot.device.aio import IoTHubDeviceClient
import Adafruit_DHT

GPIO.setwarnings(False)
sensor = Adafruit_DHT.DHT11
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)


def handle_twin(twin):
    print("Twin received", twin)
    if ('desired' in twin):
        desired = twin['desired']
        if ('led' in desired):
            GPIO.output(24, desired['led'])



async def main():
    conn_str=" My Personal Connection String "
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()
    
    
    while True:

        print('Temperature',temperature)

        data = {}
        data['Temperatute'] = temperature
        json_body = json.dumps(data)
        print("Sending message: ", json_body)
        await device_client.send_message(json_body)

        twin = await device_client.get_twin()
        handle_twin(twin)

        time.sleep(1)

    await device_client.disconnect()



if __name__ == "__main__":
    asyncio.run(main())
        
