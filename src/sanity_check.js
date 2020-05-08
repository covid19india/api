const fs = require('fs');
const fetch = require('node-fetch');
const moment = require('moment-timezone');
const data = require('../tmp/data.json');
const data_prev = require('../tmp/data_prev.json');

var total = data.statewise[0];
var err = false;
if (total.deltaconfirmed > 10000) {
    console.log("Delta confirmed is greater than 10k");
    err = true;
}

if (err) {
    console.log("Data error. No committing!");
    process.exit(1);
}
else {
    console.log("No known data errors. Proceeding to commit!");
}