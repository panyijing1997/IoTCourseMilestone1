from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import dht11
import datetime

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set ports for LED
GPIO.setup(4, GPIO.OUT)  # set #4 as ouput port
GPIO.output(4, GPIO.LOW)  # initially turned off

    # Initial the dht device, with data pin connected to:

#instance = dht11.DHT11(pin=12)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dht11")
def dht():

    dhtDevice = adafruit_dht.DHT11(board.D12,use_pulseio=False)
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if humidity is not None and temperature is not None:
            humidity = '{0:0.1f}'.format(humidity)
            temperature = '{0:0.1f}'.format(temperature)
            templateData={
                'temperature':temperature,
                'humidity': humidity,
           }
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        dhtDevice.exit()
        templateData={
            'temperature':"failed to read",
            'humidity': "failed to read",
        }
    except Exception as error:
        dhtDevice.exit()
        templateData={
            'temperature':"failed to read",
            'humidity': "failed to read",
        }
    return render_template('dht11.html',**templateData)
    
@app.route("/led")
def led():
    ledState = GPIO.input(4)
    templateData = {
        'title': 'GPIO #4 output State!',
        'led': ledState,
    }
    return render_template('ledControl.html', **templateData)


@app.route('/led/<action>')
def ledAction(action):
    if action == "on":
        GPIO.output(4, GPIO.HIGH)
    if action == "off":
        GPIO.output(4, GPIO.LOW)
    ledState = GPIO.input(4)
    templateData = {
        'led': ledState,
    }
    return render_template('ledControl.html', **templateData)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

