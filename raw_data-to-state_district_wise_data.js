const fs = require('fs');
const rawData = require('./raw_data');

console.log('Starting district wise data processing');
try {
  const StateDistrictWiseData = rawData.raw_data.reduce((acc, row) => {
    let stateName = row.detectedstate;
      if(!stateName) {
        stateName = 'Unknown';
      }
    if(!acc[stateName]) {
      acc[stateName] = {districtData: {}};
    }
    let districtName = row.detecteddistrict;
      if(!districtName) {
        districtName = 'Unknown';
      }
    if(!acc[stateName].districtData[districtName]) {
      
      acc[stateName].districtData[districtName] = {
//         active: 0,
        confirmed: 0,
//         deaths: 0,
        lastupdatedtime: "",
        firstReported: "",
//         recovered: 0,
      };
    }
    const currentDistrict = acc[stateName].districtData[districtName];
  
    currentDistrict.confirmed++;
    if(currentDistrict.firstReported === ""){
      currentDistrict.firstReported =  row.dateannounced;
    }
    
//     if(row.currentstatus === 'Hospitalized') {
//       currentDistrict.active++;
//     } else if(row.currentstatus === 'Deceased') {
//       currentDistrict.deaths++;
//     } else if(row.currentstatus === 'Recovered') {
//       currentDistrict.recovered++;
//     }

    return acc;
  
  }, {});
  
  fs.writeFileSync('state_district_wise.json', JSON.stringify(StateDistrictWiseData, null, 2));
  console.log('Starting district wise data processing ...done');
} catch(err) {
  console.log('Error processing district wise data', err);
}
