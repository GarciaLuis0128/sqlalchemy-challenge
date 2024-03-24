# Import the dependencies.



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
# app.py

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask.json import jsonify

app = Flask(__name__)

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/precipitation")
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(precipitation_data)

@app.route("/stations")
def stations():
    station_data = session.query(Station.station, Station.name).all()
    return jsonify(station_data)

@app.route("/temperature")
def temperature():
    temperature_data = session.query(Measurement.date, Measurement.tobs).all()
    return jsonify(temperature_data)

if __name__ == "__main__":
    app.run(debug=True)
