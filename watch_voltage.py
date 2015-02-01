import os
import datetime
import serial

from sql.db_connect import Connect

db_path = 'sqlite:///%s/stats.db' % (os.getcwd())
db = Connect(db_path)

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)


while True:
    x = ser.readline()

    if x:
        print(x)


def add_voltage(voltage):
    q = db.base.classes.stats(voltage=voltage,
                              read_time=datetime.datetime.now())
    db.session.add(q)
    db.session.commit()


add_voltage(13.00)
     
