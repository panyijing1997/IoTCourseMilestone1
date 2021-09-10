from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.OUT)  # set #4 as ouput port

GPIO.output(4, GPIO.LOW)  # initially turned off


@app.route("/")
def index():
    return render_template('index.html')

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

