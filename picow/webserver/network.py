from machine import Pin, Timer

import network
import time

wlan = network.WLAN(network.STA_IF)
#wlan.config(ssid='AIT-Controller-1',channel=11)

#wlan.active(True)
#print(wlan.config('ssid'))

import uasyncio as asyncio
import ubinascii

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

pageFile = open('index.html','r')
html = pageFile.read()
print(html)
pageFile.close()
pageFile = open('script.js','r')
script = pageFile.read()
pageFile.close()

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    request = str(request_line)
    scriptReq = request.find('script.js')
    print(scriptReq)
    if scriptReq == 7:
        response = script
    else:
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        stateis = ""
        if led_on == 6:
            print("led on")
            led.value(1)
            stateis = "LED is ON"
        if led_off == 6:
            print("led off")
            led.value(0)
            stateis = "LED is OFF"

        response = html % stateis
        
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

ssid = "AIT-Workshop";
password = "aitmiracle368"

def connect_to_network():
    wlan.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

async def main():
    print('Connecting to Network...')
    connect_to_network()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print('ready.')
    while True:
        onboard.on()
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(2)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()