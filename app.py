import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

# Setup Flask
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my homework home page<br/>"
        f"<a href=/api/v1.0/precipitation>Click HERE for precip data</a><br/>"
        f"<a href=/api/v1.0/stations>Click HERE for station IDs</a><br/>"
        f"<a href=/api/v1.0/tobs>Click HERE for temps from the most active station from the last year of data</a><br/>"
        f"/api/v1.0/2010-01-01<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precip_data = []
    
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    station_ids = list(np.ravel(results))

    return jsonify(station_ids)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    date = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > date).all()
    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def tempstart(start):
    session = Session(engine)
    sel = [ 
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ]

    tempstart = session.query(*sel).filter(Measurement.date >= start).all()

    return jsonify(tempstart)

@app.route("/api/v1.0/<start>/<end>")
def temprange(start, end):
    session = Session(engine)
    sel = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ]

    temprange = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(temprange)

if __name__ == '__main__':
    app.run(debug=True)