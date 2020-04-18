# COVID19-India API

A volunteer-driven database for COVID-19 stats & patient tracing in India.

## API

| Data                                                  | URL                                                   |
| ----------------------------------------------------- | ----------------------------------------------------- |
| National time series, statewise stats and test counts | https://api.covid19india.org/data.json                |
| State-district-wise                                   | https://api.covid19india.org/state_district_wise.json |
| State-district-wise V2                                | https://api.covid19india.org/v2/state_district_wise.json |
| Travel history (No more updated)                      | https://api.covid19india.org/travel_history.json      |
| Raw data                                              | https://api.covid19india.org/raw_data.json            |
| States Daily changes                                  | https://api.covid19india.org/states_daily.json        |
| States Daily in csv                                   | http://api.covid19india.org/states_daily_csv/confirmed.csv |
|                                                       | https://api.covid19india.org/states_daily_csv/deceased.csv |
|                                                       | https://api.covid19india.org/states_daily_csv/recovered.csv   |
| Deaths and Recoveries                                 | https://api.covid19india.org/deaths_recoveries.json   |
| Essentials and resources                              | https://api.covid19india.org/resources/resources.json  |
| Google sheets in csv                                  | https://api.covid19india.org/csv/                      |


## Projects Using This API

- [INDIA COVID-19 TRACKER](https://www.covid19india.org/) (Dashboard)
- [INDIA COVID-19 Google Map TRACKER](https://goo.gl/maps/U32Ex1gWQxmc6Aot8)

Telegram Channels
- [covid19india.org Ops Channel](https://t.me/covid19indiaorg) (News and Updates from covid19india.org Team)
- [Telegram Instant Updates](https://t.me/covid19indiaorg_updates) (Instant Updates from covid19india.org Team)

Telegram Bots
- [CoVID19 India Patients Analyzer and Alerts](https://github.com/xsreality/covid19)
- [CoVID19 Live Stats](https://github.com/Tele-Bots/CovidBot)
- [covid19indiatracker_bot](https://github.com/cibinjoseph/covid19indiatracker_bot)


## Quick Links

- [Telegram](https://telegra.ph/CoVID-19--India-Ops-03-24)
- [Patient Database](http://patientdb.covid19india.org/) (Google Drive)

## How this works

- This repo is merely a bridge to the main source of Data ([Google Sheets](https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml))
- Volunteers collect data from trusted sources and update the sheet
- This repo periodically fetches relevant data from the Sheet and create/update static json/csv.


## Contributing

- Contributions to new data formats are welcome
- Please raise an issue before submitting a PR
- Report issues with Place names in the [Main Site repo](https://github.com/covid19india/covid19india-react/issues)
- DO NOT change json or csv directly. They get replaced automatically

## Notes
- Do not use the "Current Status" in raw_data.json as we are rarely able to map the status to exact patient anymore. This will soon be deprecated in a future version of the API.
