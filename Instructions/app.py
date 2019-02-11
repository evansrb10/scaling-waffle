import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd
import time

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

#welcome page
@app.route("/")
def welcome():
    print("Server received request for 'Welcome' page...")
    return (
        f"Welcome to Hawaii!!<br/>"
        f"<br/>"
        f"Available routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date/YYYY-MM-DD<br/>"
        f"/api/v1.0/start-date/YYYY-MM-DD/end-date/YYYY-MM-DD<br/>"
    )

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    
    one_year_ago_meas = dt.date(2017,8,23) - dt.timedelta(days=365)

    recent_prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago_meas).\
    order_by(Measurement.date).all()

    all_precipitation = []
    for precipitation in recent_prcp_data:
        precipitation_dict = {}
        precipitation_dict["date"] = precipitation.date
        precipitation_dict["prcp"] = precipitation.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    all_stations = session.query(Station.name,Station.station).all()

    stns = []
    for stations in all_stations:
        station_id = {"Name":stations[0], "Station": stations[1]}
        stns.append(stations)

    return jsonify(stns)
    

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    one_year_ago_meas = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_ago_meas).\
    order_by(Measurement.date).all()

    all_tobs = []
    for tob in tobs_data:
        temp = {"Date":tob[0], "Temp": tob[1]}
        all_tobs.append(temp)

    return jsonify(all_tobs)


# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start date.

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
# for all dates greater than and equal to the start date.

@app.route("/api/v1.0/start-date/<start>")
def temp(start):
    print("Server received request for temp 'start' date page...")

    
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.commit()
    time.sleep(2)
    return jsonify(temp_results)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a start-end range.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
# for dates between the start and end date inclusive.

@app.route("/api/v1.0/start-date/<start>/end-date/<end>")
def start_end(start, end):
    print("Server received request for temp 'start' 'end' date page...")

    temp_results_2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.commit()
    time.sleep(2)
    return jsonify(temp_results_2)


# Define main behavior

if __name__ == '__main__':
    app.run(debug=True)
