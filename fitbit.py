import json

import requests

import config

class FitbitApi:
    def __init__(self, access_token, user_id="-"):
        self.user_id = user_id
        self.header = {"Authorization": f"Bearer {access_token}"}

    def request(self, uri, user_id="-"):
        try:
            url = f"{config.BASE_URL}/{user_id}/{uri}"
            resp = requests.get(url, headers=self.header)
            return json.loads(resp.text)
        except Exception as e:
            print(f"Uh oh! A fucko wucko happen with URL '{url}': {e}")
            return None


if __name__ == "__main__":
    fitbit = FitbitApi(config.ACCESS_TOKEN)
    resp = fitbit.request("activities/heart/date/2022-01-04/2022-01-08.json")
