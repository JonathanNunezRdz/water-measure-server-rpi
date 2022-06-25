import asyncio
import websockets
import RPi.GPIO as GPIO
import time
import json

async def send_distances(event, websocket):
    count = event['count']
    if count == 'infinite':
        while True:
            distance = {
                'distance': await get_distance()
            }
            await websocket.send(json.dumps(distance))
            await asyncio.sleep(0.5)
    else:
        for _ in range(count):
            distance = {
                'distance': await get_distance()
            }
            await websocket.send(json.dumps(distance))
            await asyncio.sleep(0.5)

async def get_distance():
    GPIO.output(pinTrigger, GPIO.LOW)
    GPIO.output(pinTrigger, GPIO.HIGH)

    await asyncio.sleep(0.01)
    GPIO.output(pinTrigger, GPIO.LOW)

    while GPIO.input(pinEcho) == 0:
            pulseStartTime = time.time()
    while GPIO.input(pinEcho) == 1:
            pulseEndTime = time.time()

    pulseDuration = pulseEndTime - pulseStartTime
    distance = round(pulseDuration * 17150, 2)

    print("Distance: %.2f cm" % (distance))
    return distance


async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        if event['type'] == 'get_distance':
            await send_distances(event, websocket)
        if event['type'] == 'close':
            await websocket.wait_closed()

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        print("Started")
        GPIO.setmode(GPIO.BOARD)

        pinTrigger = 7
        pinEcho = 11

        GPIO.setup(pinTrigger, GPIO.OUT)
        GPIO.setup(pinEcho, GPIO.IN)

        print("main loop run")
        asyncio.run(main())
    except websockets.exceptions.ConnectionClosed:
        print("ConnectionClosedError")
    finally:
        GPIO.cleanup()
        print("Cleaned up")

