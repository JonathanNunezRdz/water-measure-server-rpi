import requests
import asyncio
import RPi.GPIO as GPIO
import time

url = 'http://192.168.1.73:4001/api/v1/distance'

async def get_distance():
    GPIO.output(pinTrigger, GPIO.LOW)
    GPIO.output(pinTrigger, GPIO.HIGH)

    await asyncio.sleep(0.01)
    GPIO.output(pinTrigger, GPIO.LOW)

    pulseStartTime = 0

    while GPIO.input(pinEcho) == 0:
        pulseStartTime = time.time()
    while GPIO.input(pinEcho) == 1:
        pulseEndTime = time.time()

    pulseDuration = pulseEndTime - pulseStartTime
    distance = round(pulseDuration * 17150, 2)

    # print("Distance: %.2f cm" % (distance))
    return distance


async def get_distances():
    count = 0
    distances = []
    await get_distance()
    while count < 20:
        distance = await get_distance()
        distances.append(distance)
        count += 1
        print(count)
        await asyncio.sleep(0.5)
    return distances

async def handle_send_distances():
    while True:
        distances = await get_distances()
        response = requests.post(url, json={'distances': distances})
        print('Status: {}'.format(response.status_code))


async def main():
    await handle_send_distances()
    

if __name__ == "__main__":
    try:
        print("Started")
        GPIO.setmode(GPIO.BOARD)

        pinTrigger = 7
        pinEcho = 11

        GPIO.setup(pinTrigger, GPIO.OUT)
        GPIO.setup(pinEcho, GPIO.IN)

        # print("main loop run")
        asyncio.run(main())
    finally:
        GPIO.cleanup()
        print("Cleaned up")

