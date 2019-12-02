from flask import Flask, jsonify
from icalevents import icalevents
import datetime
import gocept.cache.method
import pytz

BERLIN = pytz.timezone("Europe/Berlin")


@gocept.cache.method.Memoize(60)
def get_events():
    start = datetime.datetime.utcnow() - datetime.timedelta(hours=10)
    end = datetime.datetime.utcnow() + datetime.timedelta(days=100)
    events = icalevents.events('https://kalender.eigenbaukombinat.de/public/all.ics', 
                               start=BERLIN.localize(start), 
                               end=BERLIN.localize(end))
    next_events = []
    for event in events:
        startdt = event.start.astimezone(BERLIN)
        enddt = event.end.astimezone(BERLIN)
        next_events.append(dict(
            summary=event.summary,
            sortdate=startdt.strftime('%Y%m%d%H%M'),
            startdate=startdt.strftime('%d.%m.%Y'),
            starttime=startdt.strftime('%H:%M'),
            enddate=enddt.strftime('%d.%m.%Y'),
            endtime=enddt.strftime('%H:%M'),
            all_day=event.all_day))
        
    next_events = sorted(next_events, key=lambda ev: ev['sortdate'])
    return next_events


app = Flask(__name__)

@app.route('/')
def events():
    return jsonify(get_events())
