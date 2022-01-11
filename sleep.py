from collections import Counter

import config
import fitbit

class Sleep(fitbit.FitbitApi):
    def __init__(self, access_token, user_id="-"):
        self.user_id = user_id
        super().__init__(access_token, self.user_id)

    def getSleepLogByDate(self, date: str) -> dict:
        """Returns a list of a user's sleep log entries for a given date

        Args:
            date: date of sleep log entry as YYYY-MM-DD

        Returns:
            A dict of the sleep log entry
        """
        url = f"/sleep/date/{date}.json"
        sleep_logs = self.request(url)
        sleep_logs = self.parseSleepLogs(sleep_logs)

        return sleep_logs

    def getSleepLogByDateRange(self, start_date: str, end_date: str):
        """Returns a list of a user's sleep log entries for a given date range.

        Args:
            start_date: Where to start the sleep log entries, YYYY-MM-DD
            end_date: Where to end the sleep log entries, YYYY-MM-DD

        Returns:
            A dict of the sleep log entries
        """
        url = f"/sleep/date/{start_date}/{end_date}.json"
        sleep_logs = self.request(url)
        sleep_logs = self.parseSleepLogs(sleep_logs)

        return sleep_logs

    def getSleepLogList(
        self, before_date=None, after_date=None, sort="asc", limit=1, offset=0
    ):
        """Returns a list of a user's sleep log entries before or after a given
           date specifying offset, limit and sort order. This is similar to
           `getSleepLogByDateRange()` but offers pagination on large entries.

        Args:
            after_date: Where to start the sleep log entries, YYYY-MM-DD
            before_date: Where to end the sleep entries, YYYY-MM-DD
            sort: Either ascending ("asc") or descending ("desc")
            limit: Maximum number of sleep logs to be returned, less than 100
            offset: Request the next and previous links in the pagination response

        Returns:
            A dict of the sleep log entries on success,
            None on error
        """
        if before_date and after_date:
            date_range = f"beforeDate={before_date}&afterDate={after_date}&"
        elif before_date and after_date is None:
            date_range = f"beforeDate={before_date}&"
        elif before_date is None and after_date:
            date_range = f"afterDate={after_date}&"
        else:
            print("Before date or after date is required")
            return None

        if limit > 100:
            print("Limit needs to be less than 100: {limit}")
            return None

        url = (
            f"/sleep/list.json?"
            f"{date_range}"
            f"sort={sort}&"
            f"offset={offset}&"
            f"limit={limit}"
        )
        sleep_logs = self.request(url)
        sleep_logs = self.parseSleepLogs(sleep_logs)

        return sleep_logs

    def parseSleepLogs(self, data: dict, use_short_data=False) -> list:
        """Parse regular sleep log, to get short sleep logs set
           `use_short_data` as True.

        Args:
            data: Dictionary level sleep logs containing "data" and "shortData"

        Returns:
            List of sleep entries as DataFrame
        """
        entry_level = "data" if not use_short_data else "shortData"
        sleep_logs = []
        for d in data.get("sleep"):
            levels = d["levels"]
            sleep_stats = self.sleepStats(levels[entry_level])
            sleep_logs.append(sleep_stats)

        return sleep_logs

    def sleepStats(self, sleep_logs: dict) -> dict:
        """Calculates the total time slept in seconds and amount of time and
           percent in each stage

        Args:
            sleep_logs: Sleep logs containing the entries

        Returns:
            dict: updated log entries with time spent sleeping and time/percent
                  at each stage `{"entries": [<ENTRIES>], "stages": {<STAGES>}}`
        """
        previous_sec = 0
        sleep_stats = {
            "entries":[], "stages": Counter()
        }

        # Calculate amount of time slept
        for entry in sleep_logs:
            if entry["level"] != "wake":
                previous_sec += entry["seconds"]
            entry["seconds_slept"] = previous_sec

            sleep_stats["entries"].append(entry)
            sleep_stats["stages"][entry["level"]] += entry["seconds"]

        # Calculate average time in each stage
        total_time_spent = sum(sleep_stats["stages"].values())
        for label, spent in sleep_stats["stages"].items():
            sleep_stats["stages"][label] = [spent, (spent / total_time_spent)]

        return sleep_stats


if __name__ == "__main__":
    sleep_log = Sleep(config.ACCESS_TOKEN)
    log_by_date = sleep_log.getSleepLogByDate("2022-01-05")
    date_by_range = sleep_log.getSleepLogByDateRange("2022-01-04", "2022-01-08")
    log_list = sleep_log.getSleepLogList(before_date="2022-01-10", limit=10)
    breakpoint()
