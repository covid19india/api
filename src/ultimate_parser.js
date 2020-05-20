console.log("Ultimate parser start")

const {STATE_CODES_ARRAY, STATE_CODES_REVERSE} = require('../lib/constants');

const fs = require('fs');

const {parse, format, formatISO} = require('date-fns');
const {produce} = require('immer');
const ultimateParser = (
  statesDailyResponse,
  zonesResponse,
  data,
  stateDistrictWiseResponse,
  stateTestData
) => {
  let ICMR = {};

  data.tested.map((testObj) => {
    ICMR = produce(ICMR, (draftICMR) => {
      let timestamp = null;
      try {
        timestamp = format(
          parse(testObj.updatetimestamp, 'dd/MM/yyyy HH:mm:ss', new Date()),
          'yyyy-MM-dd'
        );
      } catch (error) {}
      if (timestamp) {
        draftICMR[timestamp] = {
          samples: +testObj.totalsamplestested,
          source: testObj.source,
        };
      }
    });
  });

  let tested = {TT: ICMR};

  stateTestData.states_tested_data.map((testObj) => {
    tested = produce(tested, (draftState) => {
      draftState[STATE_CODES_REVERSE[testObj.state]] = produce(
        draftState[STATE_CODES_REVERSE[testObj.state]] || {},
        (draftTest) => {
          draftTest[
            format(
              parse(testObj.updatedon, 'dd/MM/yyyy', new Date()),
              'yyyy-MM-dd'
            )
          ] = {
            samples: +testObj.totaltested,
            source: testObj.source1,
          };
        }
      );
    });
  });

  let timeseries = {};

  statesDailyResponse.states_daily.map((dailyObj) => {
    timeseries = produce(timeseries, (draftTS) => {
      STATE_CODES_ARRAY.map((state) => {
        draftTS[state.code] = produce(
          draftTS[state.code] || {},
          (draftDate) => {
            const date = format(
              parse(dailyObj.date, 'dd-LLL-yy', new Date()),
              'yyyy-MM-dd'
            );
            let testedDict = null;
            try {
              testedDict = tested[state.code][date] || null;
            } catch (error) {}
            draftDate[date] = produce(
              draftDate[date] || {tested: testedDict},
              (draftType) => {
                draftType[dailyObj.status.toLowerCase()] =
                  +dailyObj[state.code.toLowerCase()];
              }
            );
          }
        );
      });
    });
  });

  let statewise = {};
  data.statewise.map((state) => {
    statewise = produce(statewise, (draftState) => {
      let latestTestObj = null;
      const latestTestDate = null;
      try {
        const latestTestDate = Object.keys(tested[state.statecode])[
          Object.keys(tested[state.statecode]).length - 1
        ];
        latestTestObj = tested[state.statecode][latestTestDate];
      } catch (error) {}
      draftState[state.statecode] = {
        total: {
          confirmed: +state.confirmed,
          recovered: +state.recovered,
          deceased: +state.deaths,
          tested: produce(latestTestObj || null, (draftTestObj) => {
            if (draftTestObj) {
              draftTestObj['last_updated'] = Object.keys(
                tested[state.statecode]
              )[Object.keys(tested[state.statecode]).length - 1];
            }
          }),
        },
        delta: {
          confirmed: +state.deltaconfirmed,
          recovered: +state.deltarecovered,
          deceased: +state.deltadeaths,
        },
        timeseries: timeseries[state.statecode],
        notes: state.statenotes,
        last_updated:
          formatISO(
            parse(state.lastupdatedtime, 'dd/MM/yyyy HH:mm:ss', new Date())
          ).slice(0, 19) + '+05:30',
      };
    });
  });

  const zones = zonesResponse.zones;
  zones.push({
    statecode: 'TT',
  });
  let states = {};

  zones.map((zone) => {
    states = produce(states, (draftState) => {
      draftState[zone.statecode] = produce(
        draftState[zone.statecode] || {
          timeseries: timeseries[zone.statecode],
          districts: {},
          total: statewise[zone.statecode].total,
          delta: statewise[zone.statecode].delta,
          notes: statewise[zone.statecode].notes,
          last_updated: statewise[zone.statecode].last_updated,
        },
        (draftDistricts) => {
          if (zone.statecode === 'TT') {
            draftDistricts['districts'] = null;
          } else {
            draftDistricts['districts'][zone.district] = {
              delta: {
                confirmed:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].delta.confirmed,
                recovered:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].delta.recovered,
                deceased:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].delta.deceased,
              },
              total: {
                confirmed:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].confirmed,
                recovered:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].recovered,
                deceased:
                  +stateDistrictWiseResponse[zone.state].districtData[
                    zone.district
                  ].deceased,
              },
              zone: {
                status: zone.zone,
                last_updated: format(
                  parse(zone.lastupdated, 'dd/MM/yyyy', new Date()),
                  'yyyy-MM-dd'
                ),
              },
              notes:
                stateDistrictWiseResponse[zone.state].districtData[
                  zone.district
                ].notes,
            };
          }
        }
      );
    });
  });
  return states;
};

const data = require('../tmp/data.json');
const stateDistrictWiseResponse = require('../tmp/state_district_wise.json');
const stateTestData = require('../tmp/state_test_data.json');
const statesDailyResponse = require('../tmp/states_daily.json');
const zonesResponse = require('../tmp/zones.json');

const new_data = ultimateParser(
  statesDailyResponse,
  zonesResponse,
  data,
  stateDistrictWiseResponse,
  stateTestData
);

fs.writeFileSync('./tmp/v2/data.json', JSON.stringify(new_data, null, 2));
fs.writeFileSync('./tmp/v2/data.min.json', JSON.stringify(new_data, null, 0));

console.log("Ultimate parser end")