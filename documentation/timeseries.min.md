# v4/timeseries.min.json

## Description

This is a timeseries API that provides state level data.

## Structure

```json
{
  "StateCode": {
    "dates": {
        "YYYY-MM-DD":{
            "delta": {
                "confirmed": <specificDaysConfirmedDelta>,
                "recovered": <specificDaysRecoveredDelta>,
                "deceased": <specificDaysDeceasedDelta>,
                "tested": <specificDaysTestedDelta>,
                "vaccinated": <specificDaysVaccinatedDelta>
            },
            "delta7": {
                "confirmed": <7DmaConfirmedDelta>,
                "recovered": <7DmaRecoveredDelta>,
                "deceased": <7DmaDeceasedDelta>,
                "tested": <7DmaTestedDelta>,
                "vaccinated": <7DmaVaccinatedDelta>
            },
            "total": {
                "confirmed": <TotalConfirmedTillDate>,
                "recovered": <TotalRecoveredTillDate>,
                "deceased": <TotalDeceasedTillDate>,
                "tested": <TotalTestedTillDate>,
                "vaccinated": <TotalVaccinatedTillDate>
            }
        },
        .
        .
        .
        
    }
```
- 7dma is the seven day moving average for that state.
