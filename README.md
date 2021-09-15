# IoTCourseMilestone1

## Set up

### 1. Install **SQLite** on RaspberryPi
```shell
 $ sudo apt install sqlite3
```
### 2. Install python dependencies

`sudo pip3 install datetime3`

`sudo pip3 install flask`

`sudo pip3 install adafruit-circuitpython-dht`

### 3. Clone this repo:

`git clone https://gitlab.au.dk/au671364/iotcourse.git`

### 3. Lauch the server
 
 `python3 app.py`
 
 port: 8080

If you run into error of "module board has no attribute D12", please do the following command:

`pip3 uninstall board`

`pip3 install adafruit-blinka`


