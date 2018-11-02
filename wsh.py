# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt
from flask import Flask, jsonify
import numpy as np
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    twelvperc=session.query(Measurement.prcp,Measurement.date).\
    order_by(Measurement.date.desc()).all()
    percp=[]
    for Measurements in twelvperc:
        i_dict={}
        i_dict['date']=Measurements.date
        i_dict['prcp']=Measurements.prcp
        percp.append(i_dict)
    return jsonify(percp)



@app.route("/api/v1.0/stations")
def stations():
    session1 = Session(engine)
    stationc=session1.query(Station.station).all()
    stationl= list(np.ravel(stationc))
    return jsonify(stationl)


@app.route("/api/v1.0/tobs")
def tobs():
    session2 = Session(engine)
    ld=session2.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    ld=(f'{ld}')
    ld=ld[2:12]
    x = dt.datetime.strptime(ld, ('%Y-%m-%d'))
    date = x - dt.timedelta(365)
    twelvperc=session2.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.date> date).\
    order_by(Measurement.date.desc()).all()
    temp=[]
    for Measurements in twelvperc:
        i_dict={}
        i_dict['date']=Measurements.date
        i_dict['tobs']=Measurements.tobs
        temp.append(i_dict)
    return jsonify(temp)


@app.route("/api/v1.0/<start>")
def startd(start):
    session3 = Session(engine)
    canonicalized = start.replace(" ", "").lower()
   
   
    def calc_temps(canonicalized):
        avgw=session3.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=  canonicalized).all()
        avgwl= list(np.ravel(avgw))
        return jsonify(avgwl)




# @app.route("/api/v1.0/<start>/<end>")
# def end():
# #     session4 = Session(engine)
#     def calc_temps(start_date, end_date):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    
#     return session4.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()






if __name__ == '__main__':
    app.run(debug=True)


