# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
@app.route("/")
def index():
    return(
        f"SQLalchemy challenge!<br/>"
        f"Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/enter-your-start-date <br/>"
        f"/api/v1.0/your-start-date/your-end-date"

    )


#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_result = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "2016_08_23").all()
    session.close()
    
    prec_dict = {}
    for date, prcp in precipitation_result:
        prec_dict[date] = prcp
    return jsonify(prec_dict) 


@app.route("/api/v1.0/stations")
def station():
    station_list = session.query(Station.name).all()
    session.close()
    station_output = []
    for station in station_list:
        station_output.append(station.name)
    return jsonify(station_output)


@app.route("/api/v1.0/tobs")
def tobs():
    tobs_list = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= "2016_08_23").all()
    session.close()
    tobs_output = []
    for tobs in tobs_list:
        tobs_output.append(tobs.tobs)
    return jsonify(tobs_output)

@app.route("/api/v1.0/<start>")
def start(start):
        
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        start_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start_date).all()
        session.close()
        start_list = []
        
        for min_temp, max_temp, avg_temp in start_result:
            start_dict = {}
            start_dict["Min"] = min_temp
            start_dict["Max"] = max_temp
            start_dict["Avg"] = avg_temp
            start_list.append(start_dict)
        return jsonify(start_list)
    
    
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):

    start_end_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    end_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start_end_date).filter(Measurement.date <= end_date).all() 
    session.close()
    end_list = []
        
    for min_temp, max_temp, avg_temp in end_result:
            end_dict = {}
            end_dict["Min"] = min_temp
            end_dict["Max"] = max_temp
            end_dict["Avg"] = avg_temp
            end_list.append(end_dict)
    return jsonify(end_list)


if __name__ == '__main__':
    app.run(debug=True)