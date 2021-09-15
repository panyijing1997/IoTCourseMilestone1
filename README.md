# IoTCourseMilestone1

## Set up

### 1. Install **SQLite** on RaspberryPi
```shell
 $ sudo apt install sqlite3
```
### 2. Install python dependencies
```shell
$ sudo pip3 install flask
$ sudo pip3 install adafruit-circuitpython-dht
```
### 3. Clone this repo:
```shell
$ git clone https://gitlab.au.dk/au671364/iotcourse.git
```
### 3. Lauch the server
 ```shell
 $ cd iotcourse
 $ python3 app.py
 ```
If you run into error of "module board has no attribute D12", please do the following commands:
```shell
$ pip3 uninstall board
$ pip3 install adafruit-blinka
```
Then visit `[your RPi's ip address]:8080` in broswer
