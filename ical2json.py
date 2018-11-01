from flask import Flask, jsonify
from icalevents import icalevents
import datetime
import gocept.cache.method


@gocept.cache.method.Memoize(60)
def get_events():
    start = datetime.datetime.now() - datetime.timedelta(hours=10)
    end = datetime.datetime.now() + datetime.timedelta(days=100)
    events = icalevents.events('https://eigenbaukombinat.de/all.ics', 
                               start=start, end=end)
    next_events = []
    for event in events:
        next_events.append(dict(
            summary=event.summary,
            sortdate=event.start.strftime('%Y%m%d%H%M'),
            startdate=event.start.strftime('%d.%m.%Y'),
            starttime=event.start.strftime('%H:%M'),
            enddate=event.end.strftime('%d.%m.%Y'),
            endtime=event.end.strftime('%H:%M'),
            all_day=event.all_day))
        
    next_events = sorted(next_events, key=lambda ev: ev['sortdate'])
    return next_events


app = Flask(__name__)

@app.route('/')
def events():
    return jsonify(get_events())
