# Import the dependencies.
from flask import Flask, render_template
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask.json import jsonify
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date_query = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date_query, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in precipitation_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
    
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date_query = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date_query, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    tobs_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
     filter(Measurement.station == "USC00519281").all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
    
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)


    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()
    session.close()

    # Convert list of tuples into normal list
    start_temp = list(np.ravel(temperature_stats))

    return jsonify(start_temp)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)


    temperature_stats_se = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # Convert list of tuples into normal list
    start_temp_se = list(np.ravel(temperature_stats_se))

    return jsonify(start_temp_se)


if __name__ == '__main__':
    app.run(debug=True)
