from machine import Pin, ADC, PWM, SoftI2C, reset
import oled
import network
import socket
import time
import dht
import urequests
import ujson
import ubinascii
import machine
from umqtt.simple import MQTTClient

SSID = "YOUR_WIFI"
PASSWORD = "YOUR_PASSWORD"

MQTT_BROKER = "broker.emqx.io"
MQTT_CLIENT_ID = b"ESP32_Ahmad_" + ubinascii.hexlify(machine.unique_id())

MQTT_TOPIC_MODE = b"ahmadazroun/esp32v4/mode"
MQTT_TOPIC_LIGHT = b"ahmadazroun/esp32v4/light"
MQTT_TOPIC_STATE = b"ahmadazroun/esp32v4/state"
MQTT_TOPIC_MOTION = b"ahmadazroun/esp32v4/motion"
MQTT_TOPIC_RGB = b"ahmadazroun/esp32v4/rgb"
MQTT_TOPIC_CONTROL = b"ahmadazroun/esp32v4/control"
MQTT_TOPIC_TEMP = b"ahmadazroun/esp32v4/temperature"
MQTT_TOPIC_HUM = b"ahmadazroun/esp32v4/humidity"
MQTT_TOPIC_FAN = b"ahmadazroun/esp32v4/fan"

FIREBASE_URL = "YOUR_FIREBASE_URL"

red = PWM(Pin(14))
green = PWM(Pin(26))
blue = PWM(Pin(13))

red.freq(1000)
green.freq(1000)
blue.freq(1000)

red.duty(1023)
green.duty(1023)
blue.duty(1023)

light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

motion_sensor = Pin(27, Pin.IN)

buzzer = PWM(Pin(25))
buzzer.duty(0)

relay = Pin(23, Pin.OUT)
relay.value(1)

dht_sensor = dht.DHT11(Pin(2))

i2c = SoftI2C(
    scl=Pin(18),
    sda=Pin(21),
    freq=10000
)

display = oled.SSD1306_I2C(128, 64, i2c)

system_mode = "AUTO"

motion_timeout = 5
last_motion_time = 0

startup_time = time.time()
pir_warmup_time = 25
pir_initialized = False

current_color = (0, 0, 0)

light_value = 0
light_state = "-"
motion_text = "-"
rgb_status = "OFF"

temperature = "-"
humidity = "-"
fan_status = "OFF"

last_dht_read = 0
dht_interval = 2

last_mqtt_publish = 0
mqtt_publish_interval = 1

last_firebase_post = 0
firebase_interval = 10
firebase_enabled = True


def set_color(r, g, b):
    red.duty(1023 - r)
    green.duty(1023 - g)
    blue.duty(1023 - b)


def fade_color(start, end, steps=10, delay=0.003):
    for i in range(steps + 1):
        r = int(start[0] + (end[0] - start[0]) * i / steps)
        g = int(start[1] + (end[1] - start[1]) * i / steps)
        b = int(start[2] + (end[2] - start[2]) * i / steps)

        set_color(r, g, b)
        time.sleep(delay)


def go_to_color(target):
    global current_color

    if current_color != target:
        fade_color(current_color, target)
        current_color = target


def mqtt_callback(topic, msg):
    global system_mode

    command = msg.decode().strip().upper()
    print("MQTT Command:", command)

    if command == "AUTO":
        system_mode = "AUTO"
        print("MQTT -> AUTO")

    elif command in ("GREEN", "GREEN ON", "ON", "MANUAL_ON", "MANUAL ON"):
        system_mode = "MANUAL_ON"
        print("MQTT -> GREEN")

    elif command in ("RED", "RED OFF", "OFF", "MANUAL_OFF", "MANUAL OFF"):
        system_mode = "MANUAL_OFF"
        print("MQTT -> RED")


def connect_mqtt():
    try:
        client = MQTTClient(
            MQTT_CLIENT_ID,
            MQTT_BROKER,
            keepalive=60
        )

        client.set_callback(mqtt_callback)
        client.connect(clean_session=True)
        client.subscribe(MQTT_TOPIC_CONTROL)

        print("MQTT Connected")
        print("Client ID:", MQTT_CLIENT_ID)
        print("Subscribed:", MQTT_TOPIC_CONTROL)

        return client

    except Exception as e:
        print("MQTT Connect Error:", e)
        return None


def update_oled():
    display.fill(0)
    display.text("Smart Room V4", 0, 0)
    display.text("Mode: " + system_mode, 0, 10)
    display.text("Light: " + str(light_value), 0, 20)
    display.text("Motion: " + motion_text, 0, 30)
    display.text("RGB: " + rgb_status, 0, 40)
    display.text("T:" + str(temperature) + "C H:" + str(humidity) + "%", 0, 52)
    display.show()


def webpage():
    html = f"""
<html>
<head>
<title>ESP32 Smart Room Controller V4</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{
    background: #111827;
    color: white;
    font-family: Arial;
    text-align: center;
    padding-top: 35px;
}}
.box {{
    background: #1f2937;
    width: 85%;
    max-width: 650px;
    margin: auto;
    padding: 30px;
    border-radius: 20px;
}}
h1 {{
    font-size: 38px;
    color: #38bdf8;
}}
h2 {{
    font-size: 24px;
}}
button {{
    width: 260px;
    height: 60px;
    border: none;
    border-radius: 15px;
    margin: 10px;
    font-size: 22px;
    font-weight: bold;
}}
.auto {{
    background: #38bdf8;
}}
.on {{
    background: #22c55e;
}}
.off {{
    background: #ef4444;
    color: white;
}}
.restart {{
    background: #f59e0b;
}}
</style>
</head>
<body>
<div class="box">
<h1>ESP32 Smart Room Controller V4</h1>
<h2>Mode: {system_mode}</h2>
<h2>Light: {light_value}</h2>
<h2>State: {light_state}</h2>
<h2>Motion: {motion_text}</h2>
<h2>RGB: {rgb_status}</h2>
<h2>Temperature: {temperature} °C</h2>
<h2>Humidity: {humidity} %</h2>
<h2>Fan: {fan_status}</h2>

<a href="/auto"><button class="auto">AUTO MODE</button></a><br>
<a href="/on"><button class="on">MANUAL ON</button></a><br>
<a href="/off"><button class="off">MANUAL OFF</button></a><br>
<a href="/restart"><button class="restart">RESTART ESP32</button></a>
</div>
</body>
</html>
"""
    return html


update_oled()

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(1)
wifi.active(True)
time.sleep(1)

if not wifi.isconnected():
    wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...")

wifi_timeout = 20
start_wifi_time = time.time()

while not wifi.isconnected():

    display.fill(0)
    display.text("Smart Room V4", 0, 0)
    display.text("WiFi Connecting", 0, 24)
    display.text("Please wait...", 0, 40)
    display.show()

    if time.time() - start_wifi_time > wifi_timeout:
        print("WiFi Timeout")
        display.fill(0)
        display.text("WiFi Failed", 0, 20)
        display.text("Restart ESP32", 0, 40)
        display.show()
        time.sleep(3)
        reset()

    time.sleep(1)

ip = wifi.ifconfig()[0]
print("WiFi Connected")
print("ESP32 IP:", ip)

display.fill(0)
display.text("WiFi Connected", 0, 0)
display.text(ip, 0, 20)
display.show()
time.sleep(1)

mqtt_client = connect_mqtt()

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)
server.settimeout(0.01)

print("Web Server Running")
print("Open: http://" + ip)

update_oled()


while True:

    if mqtt_client is not None:
        try:
            mqtt_client.check_msg()

        except OSError:
            print("MQTT Lost")

            try:
                mqtt_client.disconnect()
            except:
                pass

            mqtt_client = connect_mqtt()

    else:
        mqtt_client = connect_mqtt()

    try:
        client, addr = server.accept()
        client.settimeout(0.05)

        try:
            request = client.recv(512).decode()
            first_line = request.split("\r\n")[0]

            print("Request:", first_line)

            if "GET /auto " in first_line:
                system_mode = "AUTO"

            elif "GET /on " in first_line:
                system_mode = "MANUAL_ON"

            elif "GET /off " in first_line:
                system_mode = "MANUAL_OFF"

            elif "GET /restart " in first_line:
                client.send("HTTP/1.1 200 OK\r\n")
                client.send("Content-Type: text/html\r\n")
                client.send("Connection: close\r\n\r\n")
                client.send("<h1>Restarting ESP32...</h1>")
                client.close()
                time.sleep(1)
                reset()

            response = webpage()

            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/html\r\n")
            client.send("Connection: close\r\n\r\n")
            client.sendall(response)

        except OSError:
            pass

        finally:
            client.close()

    except OSError:
        pass

    light_value = light_sensor.read()
    raw_motion = motion_sensor.value()

    if time.time() - last_dht_read > dht_interval:

        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print("DHT OK")

        except Exception as e:
            print("DHT Error:", e)

        last_dht_read = time.time()

    pir_ready = time.time() - startup_time > pir_warmup_time

    if system_mode == "AUTO":

        if isinstance(temperature, int):

            if temperature >= 24:
                relay.value(0)
                fan_status = "ON"
                print("FAN ON")

            else:
                relay.value(1)
                fan_status = "OFF"
                print("FAN OFF")

        if not pir_ready:
            motion = 0
            motion_text = "WAIT"

        else:
            if not pir_initialized:
                motion = 0
                pir_initialized = True
            else:
                motion = raw_motion

            motion_text = "YES" if motion == 1 else "NO"

        if pir_ready and motion_text == "YES" and light_value > 1800:

            for i in range(3):
                buzzer.freq(2500)
                buzzer.duty(900)
                time.sleep(0.3)

                buzzer.freq(3000)
                buzzer.duty(900)
                time.sleep(0.3)

            buzzer.duty(0)

        else:
            buzzer.duty(0)

        if light_value < 1800:
            light_state = "BRIGHT"
            rgb_status = "OFF"
            go_to_color((0, 0, 0))

        else:
            light_state = "DARK"

            if pir_ready and motion == 1:
                last_motion_time = time.time()
                rgb_status = "WHITE"
                go_to_color((500, 500, 500))

            else:
                elapsed = time.time() - last_motion_time

                if pir_ready and elapsed < motion_timeout:
                    rgb_status = "WHITE"
                    go_to_color((500, 500, 500))

                else:
                    rgb_status = "DIM BLUE"
                    go_to_color((0, 0, 120))

    elif system_mode == "MANUAL_ON":

        relay.value(1)
        fan_status = "OFF"
        light_state = "-"
        motion_text = "-"
        rgb_status = "GREEN"
        go_to_color((0, 500, 0))

    elif system_mode == "MANUAL_OFF":

        relay.value(1)
        fan_status = "OFF"
        light_state = "-"
        motion_text = "-"
        rgb_status = "RED"
        go_to_color((500, 0, 0))

    update_oled()

    if mqtt_client is not None and time.time() - last_mqtt_publish > mqtt_publish_interval:

        try:
            mqtt_client.publish(MQTT_TOPIC_MODE, system_mode)
            mqtt_client.publish(MQTT_TOPIC_LIGHT, str(light_value))
            mqtt_client.publish(MQTT_TOPIC_STATE, light_state)
            mqtt_client.publish(MQTT_TOPIC_MOTION, motion_text)
            mqtt_client.publish(MQTT_TOPIC_RGB, rgb_status)
            mqtt_client.publish(MQTT_TOPIC_TEMP, str(temperature))
            mqtt_client.publish(MQTT_TOPIC_HUM, str(humidity))
            mqtt_client.publish(MQTT_TOPIC_FAN, fan_status)

            last_mqtt_publish = time.time()
            print("MQTT Data Published")

        except OSError:
            print("MQTT Publish Failed")

            try:
                mqtt_client.disconnect()
            except:
                pass

            mqtt_client = connect_mqtt()

    print("Mode:", system_mode)
    print("Light:", light_value)
    print("State:", light_state)
    print("Motion:", motion_text)
    print("RGB:", rgb_status)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Fan:", fan_status)
    print("----------------------")

    if firebase_enabled and time.time() - last_firebase_post > firebase_interval:

        try:
            data = {
                "temperature": temperature,
                "humidity": humidity,
                "light": light_value,
                "motion": motion_text,
                "fan": fan_status,
                "mode": system_mode,
                "rgb": rgb_status,
                "uptime_seconds": time.time()
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = urequests.post(
                FIREBASE_URL,
                data=ujson.dumps(data),
                headers=headers
            )

            print("Firebase:", response.text)
            response.close()

            last_firebase_post = time.time()

        except Exception as e:
            print("Firebase Error:", e)

    time.sleep_ms(20)


