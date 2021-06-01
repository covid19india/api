# COVID19-India API

## Announcement
**We have stopped capturing testing data at a district level. Please check the status of the API endpoints below.**

### Files available

- Aggregated sheets provide aggregated data at the district/state levels in csv format. 
- V4 json endpoints. These are the json apis that are used by the website to show all the statistics on the site. These can be used by developers and analysts who have knowledge of json parsing (recommended approach). All our v4 endpoints are actively developed and in use since this serves the frontend view [Documentation for the same](https://api.covid19india.org/documentation).
- Latest data from the google sheet (10-20 minutes delayed) is available through the `latest` end-point. These are present under the `raw files` section below. (Not recommended since the number of files is huge and there is no additional information present in these as compared to the above mentioned endpoints.)

### V4 JSON endpoints 

| Status        |  Link to API                                              | Description            |
| ------------- | -------------------------------------------------------- | ---------------------- |
| :green_heart: | <https://api.covid19india.org/v4/min/timeseries.min.json>  | Daily numbers across C,R,D and Tested per state (historical data).         |
| :green_heart: | <https://api.covid19india.org/v4/min/data.min.json>  | Current day numbers across districts and states.   |
| :green_heart: | <https://api.covid19india.org/v4/min/data-all.min.json>  | Per day numbers across districts and states - consider using timeseries in place of this. This is a huge file and is a mix of timeseries and data.min.json |

**Note**: Please consider using the above endpoints for all your data needs. All the data we show on the website is fuelled by the above endpoints.

#### Aggregated Sheets (CSV)

| Status        | Sheet Name                    | Link to CSV                                                                 | Description                                                                                     |
| ------------- | ----------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| :green_heart: | case_time_series              | <https://api.covid19india.org/csv/latest/case_time_series.csv>              | India level timeseries for Confirmed, Recovered and Deceased cases
| :green_heart: | states                        | <https://api.covid19india.org/csv/latest/states.csv>                        | Statewise timeseries of Confirmed, Recovered and Deceased numbers.   
| :green_heart: | districts                        | <https://api.covid19india.org/csv/latest/districts.csv>                  | Districtwise timeseries of Confirmed, Recovered and Deceased numbers.                            |
| :green_heart: | state_wise_daily              | <https://api.covid19india.org/csv/latest/state_wise_daily.csv>              | Statewise per day delta of Confirmed, Recovered and Deceased numbers.  
| :green_heart: | state_wise                    | <https://api.covid19india.org/csv/latest/state_wise.csv>                    | Statewise cumulative numbers till date.                                                                 |                                        
| :green_heart: | district_wise                 | <https://api.covid19india.org/csv/latest/district_wise.csv>                 | Districtwise Cumulative numbers till date. |
| :green_heart: | statewise_tested_numbers_data | <https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv> | Number of tests conducted in each state, ventilators ,hospital bed occupany reported in state bulletins |
| :green_heart: | tested_numbers_icmr_data      | <https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv>      | Number of tests reported by ICMR                                                                |
| :green_heart: | icmr_labs_statewise      | <https://api.covid19india.org/csv/latest/icmr_labs_statewise.csv>      | Number of Labs in each state as per ICMR                                                                |
| :green_heart: | sources_list                  | <https://api.covid19india.org/csv/latest/sources_list.csv>                  | List of sources that we are using.                                                              |
| :green_heart: | rtpcr_samples_collected       | <http://api.covid19india.org/csv/latest/icmr_rtpcr_tests_daily.csv>          | Number of RTPCR samples collected statewise in ICMR Application                             |
| :green_heart: | vaccine_doses_administered_statewise      | <http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv>  | Number of vaccine doses administered statewise - Collected from MOHFW daily bulletin                              |
| :green_heart: | cowin_vaccine_data_statewise      | <http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv>  | Key data points from CoWin database at a state level                              |
| :green_heart: | cowin_vaccine_data_districtwise      | <http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv>  | Key data points from CoWin database at a district level                           |



#### Raw Data
These endpoints should be avoided unless none of the above endpoints work for you.

| Status        | Sheet Name | Link to CSV                                              | Description            |
| ------------- | ---------- | -------------------------------------------------------- | ---------------------- |
| :green_heart: | raw_data1  | <https://api.covid19india.org/csv/latest/raw_data1.csv>  | Till Apr 19th          |
| :green_heart: | raw_data2  | <https://api.covid19india.org/csv/latest/raw_data2.csv>  | Apr 20th to Apr 26th   |
| :green_heart: | raw_data3  | <https://api.covid19india.org/csv/latest/raw_data3.csv>  | Apr 27th to May 9th    |
| :green_heart: | raw_data4  | <https://api.covid19india.org/csv/latest/raw_data4.csv>  | May 10th to May 23rd   |
| :green_heart: | raw_data5  | <https://api.covid19india.org/csv/latest/raw_data5.csv>  | May 24th to Jun 4th    |
| :green_heart: | raw_data6  | <https://api.covid19india.org/csv/latest/raw_data6.csv>  | Jun 05th to Jun 19th   |
| :green_heart: | raw_data7  | <https://api.covid19india.org/csv/latest/raw_data7.csv>  | Jun 20th to Jun 30th   |
| :green_heart: | raw_data8  | <https://api.covid19india.org/csv/latest/raw_data8.csv>  | Jul 01st to Jul 7th    |
| :green_heart: | raw_data9  | <https://api.covid19india.org/csv/latest/raw_data9.csv>  | Jul 08th to Jul 13th   |
| :green_heart: | raw_data10 | <https://api.covid19india.org/csv/latest/raw_data10.csv> | Jul 14th to Jul 17th   |
| :green_heart: | raw_data11 | <https://api.covid19india.org/csv/latest/raw_data11.csv> | Jul 18th to Jul 22nd   |
| :green_heart: | raw_data12 | <https://api.covid19india.org/csv/latest/raw_data12.csv> | Jul 23th to Aug 06th   |
| :green_heart: | raw_data13 | <https://api.covid19india.org/csv/latest/raw_data13.csv> | Aug 07th to Aug 21st   |
| :green_heart: | raw_data14 | <https://api.covid19india.org/csv/latest/raw_data14.csv> | Aug 22nd to Sep 05th   |
| :green_heart: | raw_data15 | <https://api.covid19india.org/csv/latest/raw_data15.csv> | Sep 06th to Sep 21st   |
| :green_heart: | raw_data16 | <https://api.covid19india.org/csv/latest/raw_data16.csv> | Sep 22nd to Oct 08th   |
| :green_heart: | raw_data17 | <https://api.covid19india.org/csv/latest/raw_data17.csv> | Oct 09th to Oct 26th   |
| :green_heart: | raw_data18 | <https://api.covid19india.org/csv/latest/raw_data18.csv> | Oct 27th to Nov 12th   |
| :green_heart: | raw_data19 | <https://api.covid19india.org/csv/latest/raw_data19.csv> | Nov 13th to Nov 30th   |
| :green_heart: | raw_data20 | <https://api.covid19india.org/csv/latest/raw_data20.csv> | Dec 01st to Dec 19th   |
| :green_heart: | raw_data21 | <https://api.covid19india.org/csv/latest/raw_data21.csv> | Dec 20th to Jan 08th   |
| :green_heart: | raw_data22 | <https://api.covid19india.org/csv/latest/raw_data22.csv> | Jan 09th to Jan 31st   |
| :green_heart: | raw_data23 | <https://api.covid19india.org/csv/latest/raw_data23.csv> | Feb 01st to Feb 27st   |
| :green_heart: | raw_data24 | <https://api.covid19india.org/csv/latest/raw_data24.csv> | Feb 28th to Mar 31st   |
| :green_heart: | raw_data25 | <https://api.covid19india.org/csv/latest/raw_data25.csv> | Apr 01st to Apr 20th   |
| :green_heart: | raw_data26 | <https://api.covid19india.org/csv/latest/raw_data26.csv> | Apr 21st to May 04th   |
| :green_heart: | raw_data27 | <https://api.covid19india.org/csv/latest/raw_data27.csv> | May 05th to May 17th   |
| :green_heart: | raw_data28 | <https://api.covid19india.org/csv/latest/raw_data28.csv> | May 18th onwards       |


#### Note

- Avoid using raw sheets. The only reason to use raw sheets would be to refer to demographics (rarely available) or to sources of numbers
- Always try to use the aggregated numbers above as they have been treated for discrepancies

#### Contributing

- If you notice issues, have questions or want to suggest enhancements, please raise an issue in the repo.

#### Quick Links

A more detailed note of the columns present in the data may be found in the json documentation

- [Documentation](https://api.covid19india.org/documentation)

...................................................
