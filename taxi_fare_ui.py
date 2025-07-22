import streamlit as st
import pandas as pd
import numpy as np
import pickle
import emoji
from math import radians, cos, sin, asin, sqrt
from datetime import datetime, date, time

# Load the trained model
with open(r"C:\Users\admin\Downloads\Guvi-DataScience-Course\Project\best_taxi_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define the haversine function
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # radius of earth in kilometers
    return c * r

st.set_page_config(page_title="NYC Taxi Fare Prediction", page_icon=emoji.emojize(":automobile:"), layout="wide")
st.markdown("<h1 style = 'text-align: center'>🚕 NYC Taxi Fare</h1>", unsafe_allow_html=True)
st.markdown("Enter trip details below to estimate the taxi fare:")

# Separate date and time inputs
pickup_date = st.date_input("Pickup Date", date.today())
pickup_time = st.time_input("Pickup Time", datetime.now().time(),disabled=True)

# Combine them into a datetime object
pickup_datetime = datetime.combine(pickup_date, pickup_time)

# Input Fields
passenger_count = st.slider("Number of Passengers", 1, 6, 1)
pickup_latitude = st.number_input("Pickup Latitude", value=40.761432)
pickup_longitude = st.number_input("Pickup Longitude", value=-73.979815)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.641311)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.778139)

# Feature Engineering
pickup_hour = pickup_datetime.hour
pickup_day = pickup_datetime.weekday()  # 0 = Monday
pickup_month = pickup_datetime.month
is_weekend = int(pickup_day >= 5)
is_night = int(pickup_hour >= 23 or pickup_hour < 5)

trip_distance = haversine(pickup_latitude,pickup_longitude,dropoff_latitude,dropoff_longitude)
trip_duration_min = st.number_input("Trip Duration in Minutes", value=15)

# Feature Vector
input_features = pd.DataFrame([{
    'trip_distance_km': trip_distance,
    'trip_duration_min':trip_duration_min,
    'hour': pickup_hour,
    'is_weekend': is_weekend,
    'is_night': is_night,
    'pickup_day_encoded': pickup_day,
    'month_encoded': pickup_month
}])

if st.button("Predict Fare"):
    prediction = model.predict(input_features)[0]
    st.success(f"Estimated Fare Amount: ${prediction:.2f}")