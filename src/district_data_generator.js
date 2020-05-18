const fs = require('fs');
const rawDistData = require('../tmp/district_wise.json');
const moment = require('moment-timezone');
// console.log(rawDistData.districts[1]);

const StateDistrictWiseData = rawDistData.districts.reduce((acc, row) => {
    if (row.district == 'Unknown' && +row.confirmed == 0 && +row.recovered == 0 && +row.deceased == 0) {
        return acc;
    }
    let stateName = row.state;
    if (!acc[stateName]) {
        acc[stateName] = {
            districtData: {},
            statecode: row.statecode
        };
    }
    let districtName = row.district;
    if (!acc[stateName].districtData[districtName]) {
        acc[stateName].districtData[districtName] = {
            notes: "",
            active: 0,
            confirmed: 0,
            deceased: 0,
            recovered: 0,
            delta: {
                confirmed: 0,
                deceased: 0,
                recovered: 0
            }
        };
    }
    const currentDistrict = acc[stateName].districtData[districtName];
    currentDistrict.notes = row.districtnotes;
    currentDistrict.active = +row.active;
    currentDistrict.confirmed = +row.confirmed;
    currentDistrict.recovered = +row.recovered;
    currentDistrict.deceased = +row.deceased;
    currentDistrict.delta.confirmed = +row.deltaconfirmed;
    currentDistrict.delta.deceased = +row.deltadeceased;
    currentDistrict.delta.recovered = +row.deltarecovered;
    return acc;

}, {});

let stateDistrictWiseDataV2 = Object.keys(StateDistrictWiseData).map(state => {
    let districtData = StateDistrictWiseData[state].districtData;
    return {
        state,
        statecode: StateDistrictWiseData[state].statecode,
        districtData: Object.keys(districtData).map(district => {
            return { district, ...districtData[district] };
        })
    }
});
var main_data = JSON.stringify(StateDistrictWiseData, null, 2);
fs.writeFileSync('./tmp/state_district_wise.json', main_data);
fs.writeFileSync('./tmp/v2/state_district_wise.json', JSON.stringify(stateDistrictWiseDataV2, null, 2));

const now = moment().unix()
var date = moment.unix(now);
formated_date = date.tz("Asia/Kolkata").format("YYYY-MM-DD");

var dir = './tmp/districts_daily/';
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}

var today_dir = dir + formated_date;
var latest_dir = dir + "latest";
if (!fs.existsSync(today_dir)) {
    fs.mkdirSync(today_dir);
}
if (!fs.existsSync(latest_dir)) {
    fs.mkdirSync(latest_dir);
}
fs.writeFileSync(today_dir + "/state_district_wise.json", main_data);
fs.writeFileSync(latest_dir + "/state_district_wise.json", main_data);
