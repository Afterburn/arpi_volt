#!/usr/bin/python2.7

import os
import datetime
import serial
import argparse
import logging
from ConfigParser import ConfigParser

from sql.db_connect import Connect

config   = ConfigParser()
config_paths = ['/etc/arpi_volt/config', '%s/config' % (os.getcwd())]

for path in config_paths:
    if os.path.exists(path):
        config.read(path)
        break

if not config:
    print('Unable to load config')
    exit(1)

log_path = config.get('settings','log-path')
baudrate = config.get('settings','baudrate')
port     = config.get('settings','serial-port')
db_uri   = config.get('settings','db-uri')
db       = Connect(db_uri)

logging.basicConfig(filename=log_path, 
                    format='%(asctime)s:%(levelname)s -- %(message)s', 
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)

logging.info('starting')

ser = serial.Serial(port, baudrate, timeout=1)

def parse_serial(line):
    if line == 'ready':
        return {'arduino':'ready'}

    else:
        try:
            split_line = line.split(":")
            voltage = float(split_line[0])/100
            lv_warn = int(split_line[1])
        
            return {'voltage':voltage, 'lv_warn':lv_warn}

        except Exception as e:
            logging.warn('unable to parse serial: %s' % (line))
            return {}


def sanitize_serial(line):
    line = line.strip()

    if line == '':
        return 

    else:
        return line

def add_data(voltage, lv_warn):
    q = db.base.classes.stats(voltage=voltage,
                              time=datetime.datetime.now(),
                              lv_warn=lv_warn)
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

        if 'voltage' in data and 'lv_warn' in data:
            print('voltage: %s, lv_warn: %s' % (data['voltage'], data['lv_warn']))
            add_data(data['voltage'], data['lv_warn'])

        else:
            print('incomplete data')



         
