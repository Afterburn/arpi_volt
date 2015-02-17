import os
import datetime
import serial
import time

from sql.db_connect import Connect

db_path = 'sqlite:///%s/stats.db' % (os.getcwd())
db = Connect(db_path)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)






def add_voltage(voltage):
    q = db.base.classes.stats(voltage=voltage,
                              read_time=datetime.datetime.now())
    db.session.add(q)
    db.session.commit()


while True:
    x = ser.readline().strip()
    if x != "":
        if x == "ready":
            print("Arduino is ready")
        else:
            voltage = float(x.split(":")[0])/100
            print("voltage: %s" % voltage)
            add_voltage(voltage)
