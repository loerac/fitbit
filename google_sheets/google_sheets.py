from pprint import pprint

import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

creds = sac.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheets = client.open("sleep_log")

worksheet = sheets.get_worksheet(0)
sleep_logs = worksheet.get_all_records()

worksheet = sheets.get_worksheet(1)
stage_stats = worksheet.get_all_records()

pprint(sleep_logs)
pprint(stage_stats)
