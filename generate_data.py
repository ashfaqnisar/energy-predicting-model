import random
from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame

from utils import determine_season, determine_time_of_day, save_dataframe_in_csv


# Function to add random noise
def add_minimum_randomness_to_base_power_rating(value, noise_level=0.03):
    noise = random.uniform(-noise_level, noise_level)
    return max(0, value + noise)  # Ensure the final value is not negative


# Begin from the start timestamp like 00:00 of the provided date and generate data for the next 24 hours
def generate_data_based_on_days(start_timestamp=datetime.now(), days=24) -> DataFrame:
    data = []
    energy_points = days * 24  # 24 points per day

    # Base power rating of the device in kW (kilowatts)
    base_power_rating = 0.5  # 500 watts

    # Factors to adjust power usage
    time_of_day_factors = {"morning": 0.9, "afternoon": 1.1, "evening": 1.0, "night": 0.8, "midnight": 0.7}
    seasonal_factors = {"spring": 1.0, "summer": 1.15, "monsoon": 0.9, "winter": 1.1}
    weekday_factors = {"weekday": 1.0, "weekend": 0.7}

    # Generate data based on the points.
    for i in range(energy_points):
        # Get the timestamp for the current hour
        timestamp = start_timestamp + timedelta(hours=i)

        # Determine the season, time of day and weekday/weekend
        season = determine_season(timestamp.date())
        time_of_day = determine_time_of_day(timestamp)
        weekday_or_weekend = "weekend" if timestamp.weekday() >= 5 else "weekday"

        # Determine the power consumption of the device for the current hour
        base_consumption = (
                base_power_rating * time_of_day_factors[time_of_day] * seasonal_factors[season] *
                weekday_factors[weekday_or_weekend])

        # Add random noise to the power consumption
        power_consumption = add_minimum_randomness_to_base_power_rating(base_consumption)

        # Append the data to the dataframe
        data.append({
            "timestamp": timestamp,
            "season": season,
            "time_of_day": time_of_day,
            "weekday_or_weekend": weekday_or_weekend,
            "base_consumption": base_consumption,
            "noise": power_consumption - base_consumption,
            "power_consumption": power_consumption
        })
    return pd.DataFrame(data)


generated_days = 365
save_dataframe_in_csv(
    generate_data_based_on_days(days=generated_days), str(generated_days)
    , "data"
)
