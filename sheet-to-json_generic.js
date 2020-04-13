const { task, fetchData, writeData } = require("./lib");
const c = require("./lib/constants");
const moment = require("moment");

(async function main() {
  console.log("Running task on start...");
  
  var data = await fetchData({sheet:c.SHEET, tabs:{
    raw_data: c.SHEET_RAW_DATA
  }});
  data.last_updated_time = moment().utcOffset(330) + "";
  await writeData({file:c.FILE_RAW_DATA, data});

  await task({
    sheet: c.SHEET,
    tabs: {
      travel_history: c.SHEET_TRAVEL_HISTORY
    },
    file: c.FILE_TRAVEL_HISTORY
  });
  await task({
    sheet: c.SHEET,
    tabs: {
      factoids: c.SHEET_NAME_FACTOIDS, faq: c.SHEET_FAQ
    },
    file: c.FILE_WEBSITE_DATA
  });

  // need to remove objects with empty states or empty totaltested
  data = await fetchData({sheet:c.SHEET, tabs:{
    states_tested_data: c.SHEET_StateWise_Tested_Numbers_Data
  }});
  data.states_tested_data.forEach(function(item, index, object)  {
    if(!item.totaltested || !item.state){
      object.splice(index,1);
    }
  });
  await writeData({file:c.FILE_STATEWISE_TESTED_DATA, data});


  await task({
    sheet: c.SHEET,
    tabs: { states_daily: c.SHEET_DATE_WISE_DELTA },
    file: c.FILE_DATE_WISE_DELTA
  });
  await task({
    sheet: c.SHEET,
    tabs: {
      statewise: c.SHEET_STATEWISE_TAB,
      cases_time_series: c.SHEET_CASES_TIME_SERIES_TAB,
      tested: c.SHEET_Tested_Numbers_ICMR_Data,
    },
    file: c.FILE_DATA
  });
  await task({
    sheet: c.SHEET_RESOURCES,
    tabs: { resources: c.SHEET_RESOURCES_SHEET},
    file: c.FILE_RESOURCES_ESSENTIALS
  });
  await task({
    sheet: c.SHEET,
    tabs: { deaths_recoveries: c.SHEET_DEATHS_AND_RECOVERIES},
    file: c.FILE_DEATHS_RECOVERIES
  });
  console.log("End of sheet-to-json_generic");
})();

