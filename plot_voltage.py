#https://plot.ly/python/getting-started/

from datetime import datetime, timedelta

import plotly.plotly as py
from plotly.graph_objs import *

from sql.db_connect import Connect

db_uri  = 'mysql+mysqldb://root@localhost/stats'
db      = Connect(db_uri)

time_list    = []
voltage_list = []
count   = 0
seconds = timedelta(seconds=130)

#query = db.session.query(db.base.classes.rss.title, db.base.classes.rss.id).filter_by(title=title).first()
query = db.session.query(db.base.classes.stats).filter(db.base.classes.stats.time >= '2015-01-01')

for q in query:
   
    future_query = db.session.query(db.base.classes.stats).filter_by(id=q.id + 1).first()

    if not future_query:
        break

    time_diff = future_query.time - q.time

    # To prevent "jagged" lines on the plot, use less data (every hour, instead of every 2 minutes)
    # This also will add the data if there is a large gap in time (representing a power up)
    # 2 minutes times 30 is an hour (the Raspberry Pi records the time every 2 minutes)
    # We see if the time differrence is less than or equal 2 minutes (2 minutes and a few seconds 
    # so there is room for delay)
    if count < 30 and time_diff.min < seconds:
        count += 1 
        continue

    count = 0

    time_list.append(q.time)
    voltage_list.append(q.voltage)


data = Data([Scatter(x=time_list,y=voltage_list)])


plot_url = py.plot(data, filename='rpi-voltage')
