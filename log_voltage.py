import os
import datetime
import serial
import argparse

from sql.db_connect import Connect

parser = argparse.ArgumentParser()
parser.add_argument('port', action='store')

args = parser.parse_args()


db_path = 'sqlite:///%s/stats.db' % (os.getcwd())
db = Connect(db_path)

#ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
ser = serial.Serial(args.port, 9600, timeout=1)


def parse_serial(line):
    if line == 'ready':
        return {'arduino':'ready'}

    else:
        voltage = float(line.split(":")[0])/100
        return {'voltage':voltage}


def sanitize_serial(line):
    line = line.strip()

    if line == '':
        return 

    else:
        return line

def add_voltage(voltage):
    q = db.base.classes.stats(voltage=voltage,
                              read_time=datetime.datetime.now())
    db.session.add(q)
    db.session.commit()


if __name__ == '__main__':

    while True:
        data = sanitize_serial(ser.readline())

        if not data:
            continue
        
        data = parse_serial(sanitize_serial(data))

        # Working somewhat backwards here, but I'm trying to keep things easily expandable. 
        if 'arduino' in data:
            if data['arduino'] == 'ready':
                print('arduino is ready')

        if 'voltage' in data:
            print('voltage: %s' % (data['voltage']))

         




