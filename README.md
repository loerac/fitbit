# fitbit
Access Fitbit activities and publish it to a Google Spreadsheet

## Authorization
### Fitbit
To get the access token, follow the steps in
[Fitbit OAuth tutorial](https://dev.fitbit.com/apps/oauthinteractivetutorial).

Expire time is in seconds, default is setup to a week; below is a couple of examples.
| Length  |  Seconds |
|---------|:--------:|
| 1 day   |   6400   |
| 1 week  |  604800  |
| 1 month |  2592000 |
| 1 year  | 31536000 |

### Google Sheets
To get the `cred.json`, follow the steps in
[Python gspread](https://github.com/burnash/gspread)
