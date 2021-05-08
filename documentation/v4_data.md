# v4/data.min.json

## Description

This is a comprehensive API that provides state and details as of the current day.

## Structure

```json
{
 "StateCode": {
  "delta": {
   "confirmed": <deltaConfirmedForState>",
   "deceased": <deltaDeceasedForState>",
   "recovered": <deltaRecoveredForState>",
   "vaccinated": <deltaVaccinatedForState>"
  },
  "delta7":{
     "confirmed": <7DmaConfirmedForState>",
     "deceased": <7DmaDeceasedForState>",
     "recovered": <7DmaRecoveredForState>",
     "vaccinated": <7DmaVaccinatedForState>""
  },
  "districts": {
   "District1": {
    "delta":{
     "confirmed": <deltaConfirmedForDistrict>",
     "deceased": <deltaDeceasedForDistrict>",
     "recovered": <deltaRecoveredForDistrict>",
     "vaccinated": <deltaVaccinatedForDistrict>"
    },
    "delta7":{
     "confirmed": <7DmaConfirmedForDistrict>",
     "deceased": <7DmaDeceasedForDistrict>",
     "recovered": <7DmaRecoveredForDistrict>",
     "vaccinated": <7DmaVaccinatedForDistrict>""
    },
    "meta": {
     "population": <districtPopulation>,
     "tested": {
      "last_updated": "yyyy-mm-dd",
      "source": "uri",
     },
     "notes": "notesForDistrict"
    },
    "total": {
     "confirmed": <cumulativeConfirmedNumberForDistrict>,
     "deceased": <cumulativeDeceasedNumberForDistrict>,
     "recovered": <cumulativeRecoveredNumberForDistrict>,
     "tested": <cumulativeTestedNumberForDistrict>,
     "vaccinated": <cumulativeVaccinatedNumberForDistrict>
    }
   },
   .
   .
   .
  },
  "meta": {
   "last_updated": "yyyy-mm-ddHH24:M:S+GMT",
   "population": <statePopulation>,
   "tested": {
    "last_updated": "yyyy-mm-dd",
    "source": "uri"
   },
   "notes": "notesForState"
  },
  "total": {
   "confirmed": <cumulativeConfirmedNumberForState>,
   "deceased": <cumulativeDeceasedNumberForState>,
   "recovered": <cumulativeRecoveredNumberForState>,
   "tested": <cumulativeConfirmedNumberForState>,
   "vaccinated": <cumulativeVaccinatedNumberForState>
  }
 },
 .
 .
 .
}

```

- The API is an object with keys corresponding to the two letter StateCode for each state.
- Each State object has the following keys: __districts__, __delta__, __delta7__, __meta__ and __total__. The districts object is a hash object where the keys represent individual districts in the state. The remaing three keys have the save behaviour across states and district objects. They are explained below:
- meta: This substructure provides the following details:
  - last_updated: This tells when the current state/district value was updated.
  - population: This gives the population of the state (based on NCP projections) and districts (based on 2011 census)
  - tested: This has the source and last_updated values for the testing data of the current State/District.
  - notes: This gives any special notes added at the State/District level.
- delta: This substructure contains the confirmed, deceased and recovered cases for the current day for the current State/District.
- delta7: This substructure contains the seven day moving average (7DMA) for confirmed, deceased and recovered cases calculated wrt the current day for the current State/District.
- total: This substructure contains the confirmed, deceased and recovered cases till today for the current State/District.

## Usage and Caveats

- This API has data that corresponds to the data seen on the website as of today. This includes, cumulative, delta and testing numbers across states and districts.
- The keys under __delta__, __meta__ and __total__ are present only if there is a corresponding value for the same. Example, if a specific district does not see any change in recovery numbers for today, the __recovered__ key under __delta__ for that district will not be present.
