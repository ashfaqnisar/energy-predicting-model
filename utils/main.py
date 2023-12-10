from datetime import datetime

from pandas import DataFrame


# Determine the season of a given date based on the indian timezone
# Input: datetime.date object
# Output: string representing the season
def determine_season(date: datetime.date) -> str:
    # Winter: December to February
    if date.month == 12 or 1 <= date.month <= 2:
        return "winter"
    # Spring: March to April
    elif 3 <= date.month <= 4:
        return "spring"
    # Summer: May to July
    elif 5 <= date.month <= 7:
        return "summer"
    # Monsoon: August to November
    elif 8 <= date.month <= 11:
        return "monsoon"
    else:
        # Throw error if invalid date
        raise ValueError("Invalid date")


def determine_time_of_day(date: datetime.date) -> str:
    if 6 <= date.hour <= 11:
        return "morning"
    elif 12 <= date.hour <= 16:
        return "afternoon"
    elif 17 <= date.hour <= 19:
        return "evening"
    elif 20 <= date.hour <= 23:
        return "night"
    elif 0 <= date.hour <= 5:
        return "midnight"
    else:
        # Throw error if invalid date
        raise ValueError("Invalid date")


def save_dataframe_in_csv(
        data_to_save: DataFrame,
        file_name: str,
        data_path=("data/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
):
    # Store the data in a CSV file with the timestamp in the name of the file and create the filePath if not exists
    import os
    data_path = data_path + "/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    file_path = data_path + file_name + ".csv"
    data_to_save.to_csv(file_path, index=False)
