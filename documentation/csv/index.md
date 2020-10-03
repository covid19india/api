# COVID19-India API

## CSV

Sometimes, having files in a spreadsheet format is more useful for analysts and scientists. We have provided the files as downloadable csv files as below.

### Files available

Latest data from the google sheet (10-20 minutes delayed) is available through the `latest` end-point.
These are the files available

#### Raw Data

| Status        | Sheet Name | Link to CSV                                              | Description            |
| ------------- | ---------- | -------------------------------------------------------- | ---------------------- |
| :green_heart: | raw_data1  | <https://api.covid19india.org/csv/latest/raw_data1.csv>  | Till Apr 19th          |
| :green_heart: | raw_data2  | <https://api.covid19india.org/csv/latest/raw_data2.csv>  | Apr 20th to Apr 26th   |
| :green_heart: | raw_data3  | <https://api.covid19india.org/csv/latest/raw_data3.csv>  | April 27th to May 9th  |
| :green_heart: | raw_data4  | <https://api.covid19india.org/csv/latest/raw_data4.csv>  | May 10th to May 23rd   |
| :green_heart: | raw_data5  | <https://api.covid19india.org/csv/latest/raw_data5.csv>  | May 24th to June 4th   |
| :green_heart: | raw_data6  | <https://api.covid19india.org/csv/latest/raw_data6.csv>  | June 5th to June 19th  |
| :green_heart: | raw_data7  | <https://api.covid19india.org/csv/latest/raw_data7.csv>  | June 20th to June 30th |
| :green_heart: | raw_data8  | <https://api.covid19india.org/csv/latest/raw_data8.csv>  | July 1st to July 7th   |
| :green_heart: | raw_data9  | <https://api.covid19india.org/csv/latest/raw_data9.csv>  | July 8th to July 13th  |
| :green_heart: | raw_data10 | <https://api.covid19india.org/csv/latest/raw_data10.csv> | July 14th to July 17th |
| :green_heart: | raw_data11 | <https://api.covid19india.org/csv/latest/raw_data11.csv> | July 18th to July 22nd |
| :green_heart: | raw_data12 | <https://api.covid19india.org/csv/latest/raw_data12.csv> | July 23th to Aug 06th  |
| :green_heart: | raw_data13 | <https://api.covid19india.org/csv/latest/raw_data13.csv> | Aug 07th to Aug 21st   |
| :green_heart: | raw_data14 | <https://api.covid19india.org/csv/latest/raw_data14.csv> | Aug 22nd to Sep 05th   |
| :green_heart: | raw_data15 | <https://api.covid19india.org/csv/latest/raw_data15.csv> | Sep 06th to Sep 21st   |
| :green_heart: | raw_data16 | <https://api.covid19india.org/csv/latest/raw_data16.csv> | Sep 22nd onwards       |

#### Other Sheets

| Status        | Sheet Name                    | Link to CSV                                                                 | Description                                                                                     |
| ------------- | ----------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| :green_heart: | case_time_series              | <https://api.covid19india.org/csv/latest/case_time_series.csv>              | Time series of Confirmed, Recovered and Deceased cases in India
| :green_heart: | state_wise                    | <https://api.covid19india.org/csv/latest/state_wise.csv>                    | The latest State-wise situation                                                                 |                                        |
| :green_heart: | district_wise                 | <https://api.covid19india.org/csv/latest/district_wise.csv>                 | The latest District-wise  situation                                                      |
| :green_heart: | state_wise_daily              | <https://api.covid19india.org/csv/latest/state_wise_daily.csv>              | Statewise timeseries of Confirmed, Recovered and Deceased numbers.  
| :green_heart: | states                        | <https://api.covid19india.org/csv/latest/states.csv>                        | Statewise timeseries of Confirmed, Recovered and Deceased numbers in long format  
| :green_heart: | districts                        | <https://api.covid19india.org/csv/latest/districts.csv>                  | Districtwise timeseries of Confirmed, Recovered and Deceased numbers in long format                           |
| :green_heart: | statewise_tested_numbers_data | <https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv> | Number of tests conducted in each state, ventilators and hospital bed information reported in state bulletins |
| :green_heart: | tested_numbers_icmr_data      | <https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv>      | Number of tests reported by ICMR                                                                |
| :green_heart: | icmr_labs_statewise      | <https://api.covid19india.org/csv/latest/icmr_labs_statewise.csv>      | Number of Labs in each state as per ICMR                                                                |

| :green_heart: | sources_list                  | <https://api.covid19india.org/csv/latest/sources_list.csv>                  | List of sources that we are using.                                                              |

#### Note

- Use raw data files only if you need to analyze the demographics or Notes related at a patient level
- Always try to use the aggregated numbers above as they have been treated for discrepancies

#### How to

If you prefer working on a Google Sheet instead of downloading the files and would like the data to reflect the latest version - below is an example to live fetch this CSV to a spreadsheet.
> :rocket: Quick example : Apply the formula `=IMPORTDATA("https://api.covid19india.org/csv/latest/state_wise.csv")` in A1 cell of a Google Sheets to get the state data for analysis :)

#### Contributing

- If you notice issues, have questions or want to suggest enhancements, please raise an issue in the repo.

#### Quick Links

If you're looking for the json files

- [API](https://api.covid19india.org)

A more detailed note of the columns present in the data may be found in the json documentation

- [Documentation](https://api.covid19india.org/documentation)
