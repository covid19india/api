const { task, fetchData, writeData } = require("../lib");
const c = require("../lib/constants");


(async function main() {
  console.log("Running task on start...");
  await task({
    sheet: "12iFd_SP6BHK5TMKindlH4uXGPTF7tTkUzY_OBc_EQpc",
    tabs: { locales: "od6" },
    file: "/locales.json"
  });

  await task({
    sheet: "12iFd_SP6BHK5TMKindlH4uXGPTF7tTkUzY_OBc_EQpc",
    tabs: { locales_progress: "ou6ga5q" },
    file: "/locales_progress.json"
  });

  

  //   uncomment below if v1 sheet has updates
  await task({
    sheet: c.SHEET_v1,
    tabs: { raw_data: c.SHEET_RAW_DATA },
    file: c.FILE_RAW_DATA_1
  });
  await task({
    sheet: c.SHEET_v2,
    tabs: { raw_data: c.SHEET_RAW_DATA },
    file: c.FILE_RAW_DATA_2
  });
  await task({
    sheet: c.SHEET_v3,
    tabs: { raw_data: c.SHEET_RAW_DATA },
    file: c.FILE_RAW_DATA_3
  });

  await task({
    sheet: c.SHEET_v4,
    tabs: { raw_data: c.SHEET_RAW_DATA },
    file: c.FILE_RAW_DATA_4
  });

  // uncomment below if v1 sheet has updates
  await task({
    sheet: c.SHEET_v1,
    tabs: { deaths_recoveries: c.SHEET_DEATHS_AND_RECOVERIES },
    file: c.FILE_DEATHS_RECOVERIES_1
  });

  await task({
    sheet: c.SHEET_v2,
    tabs: { deaths_recoveries: c.SHEET_DEATHS_AND_RECOVERIES },
    file: c.FILE_DEATHS_RECOVERIES_2
  });

  


  await task({
    sheet: c.SHEET,
    tabs: {
      districts: c.SHEET_DISTRICT_WISE
    },
    file: c.FILE_DISTRICTS
  });

  // await task({
  //   sheet: c.SHEET,
  //   tabs: {
  //     travel_history: c.SHEET_TRAVEL_HISTORY
  //   },
  //   file: c.FILE_TRAVEL_HISTORY
  // });

  await task({
    sheet: c.SHEET,
    tabs: {
      factoids: c.SHEET_NAME_FACTOIDS, faq: c.SHEET_FAQ
    },
    file: c.FILE_WEBSITE_DATA
  });

  // need to remove objects with empty states or empty totaltested
  var data = await fetchData({
    sheet: c.SHEET, tabs: {
      states_tested_data: c.SHEET_StateWise_Tested_Numbers_Data
    }
  });
  data.states_tested_data.forEach(function (item, index, object) {
    if (!item.totaltested || !item.state) {
      object.splice(index, 1);
    }
  });
  await writeData({ file: c.FILE_STATEWISE_TESTED_DATA, data });

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
    sheet: c.SHEET,
    tabs: { sources_list: c.SHEET_SOURCES_LIST },
    file: c.FILE_SOURCES_LIST
  });

  await task({
    sheet: c.SHEET_RESOURCES,
    tabs: { resources: c.SHEET_RESOURCES_SHEET },
    file: c.FILE_RESOURCES_ESSENTIALS
  });

  await task({
    sheet: c.SHEET,
    tabs: { zones: c.SHEET_ZONES },
    file: c.FILE_ZONES
  });

  console.log("End of sheet-to-json_generic");
})();
