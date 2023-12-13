from datetime import datetime

import pandas as pd
from flask import Flask
import joblib

from utils import determine_season, determine_time_of_day

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


def preprocess_new_data(_timestamp, columns):
    # Convert new_data to a datetime object
    _timestamp = datetime.strptime(_timestamp, '%Y-%m-%d %H:%M:%S.%f')

    # Create a DataFrame to hold the features, initialized to 0
    features = pd.DataFrame(0, index=[0], columns=columns)

    # Set the appropriate features based on the timestamp
    features['hour_' + str(_timestamp.hour)] = 1
    features['day_of_week_' + str(_timestamp.weekday())] = 1
    features['month_' + str(_timestamp.month)] = 1
    features['season_' + determine_season(_timestamp)] = 1
    features['time_of_day_' + determine_time_of_day(_timestamp)] = 1
    features['is_weekend_' + str(_timestamp.weekday() >= 5)] = 1

    print('features', features)

    # Ensure that the DataFrame only contains the columns expected by the model
    features = features.reindex(columns=columns).fillna(0)

    return features


def preprocess_and_detect_spike(_data_point, actual_consumption, columns, model, threshold):
    # Preprocess the new data
    preprocessed_data = preprocess_new_data(_data_point, columns)

    # Make a prediction for the new data point
    _predicted_consumption = model.predict(preprocessed_data)[0]

    # Calculate the absolute residual
    _absolute_residual = abs(actual_consumption - _predicted_consumption)

    # Check if the absolute residual is greater than the threshold
    _is_spike = _absolute_residual > threshold

    # Detect a spike if the absolute residual is greater than the threshold
    if _is_spike:
        print("*******************************************************************")
        print(
            f"Spike detected! Predicted: {_predicted_consumption:.2f}, Actual: {actual_consumption:.2f}, Residual: {_absolute_residual:.2f}")
        print("*******************************************************************")

    return _is_spike, _absolute_residual, _predicted_consumption


training_columns = ['hour_0', 'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9',
                    'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18',
                    'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 'day_of_week_0', 'day_of_week_1',
                    'day_of_week_2', 'day_of_week_3', 'day_of_week_4', 'day_of_week_5', 'day_of_week_6', 'month_1',
                    'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10',
                    'month_11', 'month_12', 'season_monsoon', 'season_spring', 'season_summer', 'season_winter',
                    'time_of_day_afternoon', 'time_of_day_evening', 'time_of_day_midnight', 'time_of_day_morning',
                    'time_of_day_night', 'is_weekend_False', 'is_weekend_True']


@app.route('/predict_energy_for_time/<iso_datetime>')
def predict_data(iso_datetime):
    try:
        print(iso_datetime)
        # Parse the ISO date-time string into a datetime object
        datetime_obj = datetime.fromisoformat(iso_datetime)

        # Create a list of columns expected by the model
        model = joblib.load('ml-models/rf_model.pkl')

        processed_data = preprocess_new_data(datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f'), training_columns)

        # Make a prediction for the new data point
        predicted_consumption = model.predict(processed_data)

        print('predicted_consumption for the date ', iso_datetime, predicted_consumption)

        # Return the predicted consumption
        return {
            "timestamp": iso_datetime,
            "predicted_consumption": predicted_consumption[0]
        }
    except ValueError as e:
        print('error', e)
        return "Invalid ISO date-time format"


if __name__ == '__main__':
    app.run(debug=True)
