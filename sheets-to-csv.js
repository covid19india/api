const fetch = require('node-fetch');
const moment = require('moment-timezone');
var fs = require('fs');

var dir = './csv/';
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
}

const now = moment().unix()
var date = moment.unix(now);
formated_date = date.tz("Asia/Kolkata").format("YYYY-MM-DD");

var today_dir = dir + formated_date;
var latest_dir = dir + "latest";
if (!fs.existsSync(today_dir)) {
    fs.mkdirSync(today_dir);
}
if (!fs.existsSync(latest_dir)) {
    fs.mkdirSync(latest_dir);
}

const PUBLISHED_SHEET_ID = "2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4";

const all_sheets = [
    ["raw_data", "0"],
    ["death_and_recovered", "200733542"],
    ["state_wise", "1896310216"],
    ["state_wise_daily", "1395461826"],
    ["sources_list", "704389477"],
    ["statewise_tested_numbers_data", "486127050"],
    ["case_time_series", "387368559"],
    ["tested_numbers_icmr_data", "2143634168"],
    ["travel_history", "1532084277"]
];

all_sheets.forEach(element => {
    console.log("Reading: "+element[0]);
    var temp_url = "https://docs.google.com/spreadsheets/d/e/" + PUBLISHED_SHEET_ID + "/pub?gid=" + element[1] + "&single=false&output=csv";
    console.log(temp_url);
    url = encodeURI(temp_url);
    let settings = { method: "Get" };
    fetch(url, settings).then(res => res.text())
        .then(csv => {
            fs.writeFileSync(today_dir + "/"+element[0]+".csv", csv);
            fs.writeFileSync(latest_dir + "/"+element[0]+".csv", csv);
            console.log("Write completed: "+element[0]);
        });
});
