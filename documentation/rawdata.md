# raw_data{n}.json

## Description

raw_data{n}.json represents the rows entered into the google sheets by the data ops team. The data present in raw_data json file are either - individual records or district level records. Some of these district level records might have district name as empty or Unknown. These are due to state bulletins not having enough details about district splits.

## Structure

- `agebracket`  
 This provides the age of the case. This is applicable only for rows that represent individual records.
- `backupnotes` 
 This was used during initial days to record additional information. The usage of this has been discontinued.
- `contractedfromwhichpatientsuspected`
 This field gives the patient id from whom the current patient is believed to have contracted the virus. This is based on state bulletins. As of July 10th, this field is used only for Karnataka records.
- `currentstatus`  
 This can have: Hospitalized, Recovered, Deceased or Migrated_Others as values. These represent the status of the case. Migrated_Others is used as a place holder for those cases that are marked by states as having migrated to other states or have died due to non covid reasons.
- `dateannounced`
 This field gives the date on which the case(s) was reported by the state/central bulletin
- `detectedcity`
 This field gives the city where the case(s) were reported.
- `detecteddistrict`
 This field gives the district where the case(s) were reported.
- `detectedstate`
 This field gives the state where the case(s) were reported.
- `estimatedonsetdate`
 This field is not used.
- `gender`
 This provides the gender of the case. This is applicable only for rows that represent individual records.
- `nationality`
 This provides the nationality of the case. This is applicable only for rows that represent individual records.
- `notes`
 This provides the any notes regarding the case(s) that are reported.
- `numcases`
 This field can any integer value. This field denotes the following:
  - If the value is == 1 : The row indicates an individual record (age and gender info are subject to state bulletin releases).
  - If the value != 1 (greater than or less than 1) : The row indicates a district level record.
  - If the value > 0 and (detecteddistrict == '' or detecteddistrict == 'Unknown') : The row added without district details as state bulletin did not have district details at the point of data entry.
  - If the value < 0 and (detecteddistrict == '' or detecteddistrict == 'Unknown') : The row added to adjust a previously added bulk entry as stated above
  - If the value < 0 and (detecteddistrict != '' and detecteddistrict != 'Unknown') : The row added due to state bulletins providing a reduced count for that district/day/category combination.
  - If the value == 0 : Ingore the record. This would've been an entry made and ignored later due to clarifications from state bulletins.
- `patientnumber`
  - This field used to hold a global patient number for all patients being reported. This has been discontinued with the shift to district level entries.
- `source1`
  - Source for the current row.
- `source2`
  - Additional source for the current row.
- `source3`
  - Additional source for the current row.
- `statecode`
  - A two letter code to represent the state/UT.
- `statepatientnumber`
  - A field to represent the state patient number if the state bulletin provided a state patient number.
- `statuschangedate`
  - A field to represent the change of status of patients from Hospitalized -> Recovered or Hospitalized -> Deceased. This field has been discontiuned with district level records.

## Usage and caveats

- raw_data json api should be used only when the relevant details are not available through the other APIs provided for state/districts. raw data apis have evolved over time. The data present in some of the earlier versions of raw_data json are not completely clean since there was a lot of inconsistency in the reporting by state governments. Please exercise caution while using raw_data json APIs.
- numcases column it's significance and handling of bulk negatives:
 As pointed in the description, the numcases can have a varied set of values. Most important to note while dealing with numcases are those rows with bulk +ve/-ve values without a district value present. These are entries which represent data that has no district level information. However, sometimes the states release these details at a later point in time. In events as such, a bulk -ve is added to the same state/date/category combination to negate out the previous bulk entry and district splits are added to the state/date/category combination. In technical terms - if you were to write an SQL query with count on numcases column and a group by on districtname, statename, dateannounced and currentstatus, you should get proper values for all districts for that state for those days where data is present. The output of a query as such might also yeild rows with empty or unknown districts. These are the cases for which district details were not announced by the state govts. Examples: DL, TS both have a large number of unknown districts for all three categories.
 Some rows might have district name and might have a negative value for numcases. These are genuine reductions due to state bulletin numbers. These should be consumed as is.
