import pandas as pd

import config
import constants
import fitbitApi


class Nutrition(fitbitApi.FitbitApi):
    def __init__(self, access_token, user_id="-"):
        self.user_id = user_id
        super().__init__(access_token, self.user_id)

    def getWaterLog(self, date: str) -> dict:
        """Retrieves a summary and list of a user's water log entries for a
           given day.

        Args:
            date: Date of water log entry, YYYY-MM-DD

        Returns:
            dict: Water log entries of amount of water consumed in ounce

        """
        url = f"/foods/log/water/date/{date}.json"
        resp = self.request(url)

        # Change units of water to ounces for summary and entries
        tmp_df = pd.DataFrame(resp["water"])
        tmp_df["amount"] = tmp_df["amount"] / 29.57344

        water_log = {
            "total": resp["summary"]["water"] / 29.57344,
            "water": tmp_df.to_dict("records"),
        }

        return water_log

    def getNutritionByDate(self, resource="water", date="today", period="1d"):
        """Retrieves the food and water consumption data for a given resource
           over a period of time by specifying a date and time period.

        Args:
            resource: Data to be returned, "caloriesIn" or "water"
            date: End date of the period specified in "YYYY-MM-DD" or "today"
            period: Range for which data will be returned

        Returns:
            dict: Resource entry of consumed resource
        """
        if resource not in constants.SUPPORTED_RESOURCE:
            print(f"Resource {resource} not supported: {constants.SUPPORTED_RESOURCE}")
            return None

        if period not in constants.SUPPORTED_RANGE:
            print(f"Period {period} not supported: {constants.SUPPORTED_RANGE}")
            return None

        url = f"/foods/log/water/date/{date}/{period}.json"
        resp = self.request(url)

        return resp

    def getNutritionDateRange(
        self, resource="water", start_date="today", end_date="today"
    ):
        """Retrieves the food and water consumption data for a given resource
           over a period of time by specifying a date range. The response will
           include only the daily summary values.

        Args:
            resource: Data to be returned, "caloriesIn" or "water"
            start_date: When to start the range entries, YYYY-MM-DD
            end_date: When to end the range entries, YYYY-MM-DD

        Returns:
            dict: Resource entry of consumed resource
        """
        if resource not in constants.SUPPORTED_RESOURCE:
            print(f"Resource {resource} not supported: {constants.SUPPORTED_RESOURCE}")
            return None

        url = f"/foods/log/{resource}/date/{start_date}/{end_date}.json"
        resp = self.request(url)

        # Change units of water to ounces for entries
        if resource == "water":
            tmp_df = pd.DataFrame(resp["foods-log-water"])
            tmp_df["value"] = tmp_df["value"].astype(float) / 29.57344
            resp = {
                "foods-log-water": tmp_df.to_dict("records"),
            }

        return resp


if __name__ == "__main__":
    nutrition = Nutrition(config.ACCESS_TOKEN)
    water_log = nutrition.getWaterLog("2022-01-06")
    nutrition_by_date = nutrition.getNutritionByDate()
    nutrition_by_range = nutrition.getNutritionDateRange(
        resource="caloriesIn", start_date="2022-01-04", end_date="2022-01-08"
    )
    breakpoint()
