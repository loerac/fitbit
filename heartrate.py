import config
import constants
import fitbit


class HeartRate(fitbit.FitbitApi):
    def __init__(self, access_token, user_id="-"):
        self.user_id = user_id
        super().__init__(access_token, self.user_id)

    def getHeartRate(self, date: str, period="1d") -> tuple:
        """Retrieves the heart rate time series data over a period of time by
           specifying a date and time period. The response will include only the
           daily summary values.

        Args:
            date: Date of heart rate entry, YYYY-MM-DD
            period: Heart rate entry over a period of time

        Returns:
            tuple:
                dict: heart rate activities
                dict: heart rate series
        """
        if period not in constants.SUPPORTED_RANGE:
            print(f"Period {period} not supported: {constants.SUPPORTED_RANGE}")
            return None

        url = f"/activities/heart/date/{date}/{period}.json"
        heart_activities = self.request(url)
        heart_activities = self.parseActivites(heart_activities)

        return heart_activities

    def getHeartRateRange(self, start_date: str, end_date: str) -> dict:
        """Retrieves the heart rate time series data over a period of time by
           specifying a date range. The response will include only the daily
           summary values.

        Args:
            start_date: When to start the range entries, YYYY-MM-DD
            end_date: When to end the range entries, YYYY-MM-DD

        Returns:
            dict: heart rate activities
        """
        url = f"/activities/heart/date/{start_date}/{end_date}.json"
        heart_activities_range = self.request(url)
        heart_activities_range = self.parseActivites(heart_activities_range)[0]

        return heart_activities_range

    def parseActivites(self, heart_activities):
        activities_heart_df = []
        activities_heart_intraday = []

        for h in heart_activities.get("activities-heart"):
            value = h["value"]
            zones = value["heartRateZones"]
            activities_heart_df.append(zones)

        intraday = heart_activities.get("activities-heart-intraday")
        if intraday:
            for dataset in intraday.get("dataset"):
                activities_heart_intraday.append(dataset)

        return activities_heart_df, activities_heart_intraday


if __name__ == "__main__":
    heart_rate = HeartRate(config.ACCESS_TOKEN)
    heart_rate_series = heart_rate.getHeartRate("2022-01-05")
    heart_range = heart_rate.getHeartRateRange("2022-01-04", "2022-01-08")
    breakpoint()
