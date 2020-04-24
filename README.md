# COVID19-India API

A volunteer-driven, crowdsourced database for COVID-19 stats & patient tracing in India

### JSON

|Status| Data                                                  | URL                                                   |
|----------------------------------------------------- |----------------------------------------------------- | ----------------------------------------------------- |
|:green_heart:| Patient Level : Raw Data | https://api.covid19india.org/raw_data.json  |
|:green_heart:| Patient Level : Deaths and Recoveries | https://api.covid19india.org/deaths_recoveries.json |
|:green_heart:| National Level :Time series, State-wise stats and Test counts | https://api.covid19india.org/data.json                |
|:green_heart:| State Level : has district-wise info  | https://api.covid19india.org/state_district_wise.json |
|:green_heart:| State Level : has district-wise info V2 _(minor difference in structure)_ | https://api.covid19india.org/v2/state_district_wise.json |
|:green_heart:| State Level : Daily changes | https://api.covid19india.org/states_daily.json  |
|:green_heart:| Essentials and resources  | https://api.covid19india.org/resources/resources.json  |
|:end:| Travel history (No more updated)  | https://api.covid19india.org/travel_history.json  |


### CSV
Sometimes, having files in a spreadsheet format is more useful for analysts and scientists. We have provided the files as downloadable csv files in the following location.

| Data                                                  | URL                                                   |
| ----------------------------------------------------- | ----------------------------------------------------- |
| Google sheets in csv                                  | https://api.covid19india.org/csv/                      |

> :rocket: Quick example : Apply the formula `=IMPORTDATA("https://api.covid19india.org/csv/latest/state_wise.csv")` in A1 cell of a Google Sheets to get the state data for analysis :)

## Projects Using This API

- [COVID-19 INDIA TRACKER](https://www.covid19india.org/) (Main Dashboard)


**Telegram Channels**
- [covid19india.org Ops Channel](https://t.me/covid19indiaorg) (News and Announcements from covid19india.org Team)
- [Telegram instant Updates](https://t.me/covid19indiaorg_updates) (Instant Updates from covid19india.org Team)

**Analysis**
- [State-wise key stats](https://docs.google.com/spreadsheets/d/e/2PACX-1vTkixJNsO3otK_yOz-7Ru--yNo9S3J9S6ENFIKU6rDuNwhVTAXJWuPH2mzTzBEt1vzhvzQ1Zxyy9ZAt/pubhtml) (by [@Ankan_Plotter](https://t.me/Ankan_Plotter))
- [Stats and viz in Google Data Studio](https://tinyurl.com/covid19indiadashboard) (by [@veeyeskay](https://t.me/veeyeskay))

**Other Trackers/Dashboards**
- [Tracker](https://covidstat.info/) (by [@skavinvarnan ](https://github.com/skavinvarnan))
- [Statistics and Predictive Analysis (India)](https://gnsp.in/covid19/) (by [@GnsP](https://github.com/GnsP))
- [TN Specific](https://covid19trackerbk.netlify.app/) - [Repo](https://github.com/dynamicbalaji/covid19-tracker)
- [COVID-19 Tracker (India)](https://acroinfer.in/) - (by [@Acroalias](https://github.com/BitanBhowmick))


**Telegram Bots**
- [CoVID19 India Patients Analyzer and Alerts](https://github.com/xsreality/covid19)
- [CoVID19 Live Stats](https://github.com/Tele-Bots/CovidBot)
- [covid19indiatracker_bot](https://github.com/cibinjoseph/covid19indiatracker_bot)
- [INDIA COVID-19 Google Map TRACKER](https://goo.gl/maps/U32Ex1gWQxmc6Aot8)


## Quick Links

- [Telegram Group](https://telegra.ph/CoVID-19--India-Ops-03-24)
- [Patient Database](http://patientdb.covid19india.org/)

## How this works

- This repo is merely a bridge to the main source of Data ([Google Sheets](https://docs.google.com/spreadsheets/d/e/2PACX-1vSc_2y5N0I67wDU38DjDh35IZSIS30rQf7_NYZhtYYGU1jJYT6_kDx4YpF-qw0LSlGsBYP8pqM_a1Pd/pubhtml))
- Volunteers collect data from trusted sources and update the sheet
- This repo periodically fetches relevant data from the Sheet and create/update static json/csv.
- We use Github Actions to fetch the data periodically and auto-commit. Thank you @Github :)


## Contributing

- Contributions to new data formats are welcome. Please create a GH issue and discuss there before working on the same.
- Please raise an issue before submitting a PR
- Report issues with regarding [covid19india.org](https://www.covid19india.org) website in the [react-site repository](https://github.com/covid19india/covid19india-react/issues)
- DO NOT change anything in `gh-pages` branch directly.They get replaced automatically

## Notes
- Do not use the "Current Status" in raw_data.json as we are rarely able to map the status to the exact patient anymore. This will soon be deprecated in a future version of the API.
