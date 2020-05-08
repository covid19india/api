# COVID19-India API

A volunteer-driven, crowdsourced database for COVID-19 stats & patient tracing in India

[https://github.com/covid19india/api](https://github.com/covid19india/api)

## Update [27 April]

Due to the growing size of the raw data, and the fact that regions like DL, MH, TG are only providing district level information, we have made a change in our data collection.
Now, raw data is available in three parts :

`api.covid19india.org/raw_data1.json` (Data till EoD Apr 19th)<br>
`api.covid19india.org/raw_data2.json` (Data till EoD Apr 26th)<br>
`api.covid19india.org/raw_data3.json` (Live 🚀)<br>

Also, there are some structural difference in raw_data3.json :
When a new report/bulletin is released from a state regarding confirmed cases :

1. If patient level information is available (from several states like KA,KL,BH etc.), that is captured.
2. If only districtwise information is available, one row is entered for each district, and "numcases" field mentions the number of cases in that district
3. If only statewise information is available, one row is added added for the entire state (DL 👀)

4. Recoveries and Deceased information is also available through raw_data3.json now. Use the "Current Status" field to extract that information.

All other aggregate APIs retain the same behaviour.
CSV files for the same are also available through `api.covid19india.org/csv/latest/raw_data{n}.csv`

### JSON

| Status        | Data                                                                      | URL                                                      |
| ------------- | ------------------------------------------------------------------------- | -------------------------------------------------------- |
| :green_heart: | Patient Level : Raw Data Partition 1 (Till Apr 19)                        | https://api.covid19india.org/raw_data1.json              |
| :green_heart: | Patient Level : Raw Data Partition 2 (From Apr 20 to Apr 26)              | https://api.covid19india.org/raw_data2.json              |
| :green_heart: | Patient Level : Raw Data Partition 3 (From Apr 27 to Now)                 | https://api.covid19india.org/raw_data3.json              |
| :green_heart: | National Level :Time series, State-wise stats and Test counts             | https://api.covid19india.org/data.json                   |
| :green_heart: | State Level : has district-wise info                                      | https://api.covid19india.org/state_district_wise.json    |
| :green_heart: | State Level : has district-wise info V2 _(minor difference in structure)_ | https://api.covid19india.org/v2/state_district_wise.json |
| :green_heart: | State Level : Daily changes                                               | https://api.covid19india.org/states_daily.json           |
| :green_heart: | State Level : Testing data                                                | https://api.covid19india.org/state_test_data.json        |
| :green_heart: | District Level : Daily changes                                            | https://api.covid19india.org/districts_daily.json        |
| :green_heart: | District Level : Zones                                                    | https://api.covid19india.org/zones.json                  |
| :green_heart: | Essentials and resources                                                  | https://api.covid19india.org/resources/resources.json    |
| :end:         | Raw Data (Partition 1 + Partition 2. Frozen after Apr 26th)               | https://api.covid19india.org/raw_data.json               |
| :end:         | Deaths and Recoveries (Frozen after Apr 26th)                             | https://api.covid19india.org/deaths_recoveries.json      |
| :end:         | Travel history (No more updated)                                          | https://api.covid19india.org/travel_history.json         |

### CSV

Sometimes, having files in a spreadsheet format is more useful for analysts and scientists. We have provided the files as downloadable csv files in the following location.

| Data                 | URL                                                                    |
| -------------------- | ---------------------------------------------------------------------- |
| Google sheets in CSV | [https://api.covid19india.org/csv/](https://api.covid19india.org/csv/) |

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
- [Tracker](https://livecovid.in/) (by [@anamritraj ](https://github.com/anamritraj/livecovid.in-webapp))
- [India & World Tracker](http://tcovid19.herokuapp.com/) (by [@thecoducer](https://github.com/thecoducer))
- [COVID-19 Track](http://github.com/adarshbalu/covid_track/) (by [@adarshbalu](https://github.com/adarshbalu))
- [Maharashtra COVID-19 Dashboard/Tracker](http://covid.pranavsheth.com/) (by [@pranavs80](https://github.com/pranavs80))
- [COVID-19 India Tracker](https://covidindiatracker.netlify.app/) (by [@PrinceSumberia](https://github.com/PrinceSumberia))
- [COVID-19 Tracker/Visualizer](https://coronago.cf/) (by [@kaushikbhat07](https://github.com/kaushikbhat07))
- [Bihar COVID-19 Dashboard/Tracker](https://coronainbihar.github.io/) (by [@anandv01](https://github.com/anandv01))
- [COVID19 Tracker/Predictor](https://track-covid-19ind.herokuapp.com/) (by [@manoj](https://github.com/ManojNallusamy))
- [COVID-19 Tracker App](https://corona-india.live/) (by [@sandeshchoudhary](https://github.com/sandeshchoudhary))


**Telegram Bots**

- [CoVID19 India Patients Analyzer and Alerts](https://github.com/xsreality/covid19)
- [CovidBot: CoVID19 Live Stats Chatbot](https://github.com/Tele-Bots/CovidBot) (by [@gurrrung](https://github.com/gurrrung))
- [covid19indiatracker_bot](https://github.com/cibinjoseph/covid19indiatracker_bot)
- [INDIA COVID-19 Google Map TRACKER](https://goo.gl/maps/U32Ex1gWQxmc6Aot8)


**Chrome/Firefox Extensions**
- [Covid-19 Tracker](https://coronatrends.live) (by [@akanshgulati ](https://github.com/akanshgulati))

## Quick Links

- [Telegram Group](https://telegra.ph/CoVID-19--India-Ops-03-24)
- [Patient Database](http://patientdb.covid19india.org/)

## How this works

- Data in this repository is generated from Google Sheets (https://api.covid19india.org/csv)
- Volunteers collect data from trusted sources and update the sheet
- Using Github Actions this repo periodically fetches relevant data from the Sheet and update static json and csv files

## Contributing

- Contributions to new data formats are welcome. Please create a GH issue and discuss there before working on the same.
- Please raise an issue before submitting a PR
- Report issues regarding [covid19india.org](https://www.covid19india.org) website in the [react-site repository](https://github.com/covid19india/covid19india-react/issues)
- DO NOT change anything in `gh-pages` branch directly.They get replaced automatically

## Notes

- Do not use the "Current Status" in raw_data.json as we are rarely able to map the status to the exact patient anymore. This will soon be deprecated in a future version of the API.

..................
