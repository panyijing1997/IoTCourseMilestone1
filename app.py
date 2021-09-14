from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import sqlite3


db_file = 'IoTMilestone1DB.db'
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set ports for LED
GPIO.setup(4, GPIO.OUT)  # set #4 as ouput port
GPIO.output(4, GPIO.LOW)  # initially turned off

    # Initial the dht device, with data pin connected to:
#set ports for distance sensor
TRIG=23
ECHO=24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#instance = dht11.DHT11(pin=12)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dht11")
def dht():

    dhtDevice = adafruit_dht.DHT11(board.D12,use_pulseio=False)
    msg = "failed to read the sensor, showing the newest record from the database"
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if humidity is not None and temperature is not None:
            msg="read from the sensor successfully"
            #humidity = '{0:01.1f}'.format(humidity)
            #temperature = '{0:01.1f}'.format(temperature)
            templateData={
                'temperature':temperature,
                'humidity': humidity,
                'msg':msg
           }
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            sql = 'insert into history_temperature_humidity(temperature, humidity, create_time) values(?,?,?)'
            data = (temperature, humidity, timestamp)
            cur.execute(sql, data)
            conn.commit()
            conn.close()
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going

        dhtDevice.exit()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        newestData = cur.execute("select * from history_temperature_humidity order by id desc limit 1")
        for data in newestData:
            temperature = data[1]
            humidity = data[2]

        templateData={
            'temperature': temperature,
            'humidity': humidity,
            'msg':msg
        }
        conn.close()
    except Exception as error:
        dhtDevice.exit()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        newestData = cur.execute("select * from history_temperature_humidity order by id desc limit 1")
        for data in newestData:
            temperature = data[1]
            humidity = data[2]
        templateData={
            'temperature': temperature,
            'humidity': humidity,
            'msg': msg
        }
        conn.close()
    return render_template('dht11.html',**templateData)

@app.route("/tempHistoryData")
def histiryData():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    history_data = cur.execute("select * from history_temperature_humidity order by id desc limit 30")
    history_data_list = []
    for data in history_data:
        history_data_list.append(data)
    conn.close()
    templateData = {
        'historyData': history_data_list
    }
    return render_template('tempHistoryData.html', **templateData)

@app.route("/led")
def led():
    ledState = GPIO.input(4)
    templateData = {
        'title': 'GPIO #4 output State!',
        'led': ledState,
    }
    return render_template('index.html', **templateData)


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
    return render_template('index.html', **templateData)

@app.route("/distance")
def dist():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    pulse_start = 0
    pulse_end = 0
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    templateData={
        'dist':distance,
    }
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    sql = 'insert into history_distance(distance, create_time) values(?,?)'
    data = (distance, timestamp)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return render_template('distance.html', **templateData)

@app.route("/distHistoryData")
def distHist():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    history_data = cur.execute("select * from history_distance order by id desc limit 30")
    history_data_list = []
    for data in history_data:
        history_data_list.append(data)
    conn.close()
    templateData = {
        'historyData': history_data_list
    }
    return render_template('distHistoryData.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


