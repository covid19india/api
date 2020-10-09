const SHEET_V1 = process.env.SHEET_ID_v1
const SHEET_V2 = process.env.SHEET_ID_v2
const SHEET_V3 = process.env.SHEET_ID_v3
const SHEET_V4 = process.env.SHEET_ID_v4
const SHEET_V5 = process.env.SHEET_ID_v5
const SHEET_V6 = process.env.SHEET_ID_v6
const SHEET_V7 = process.env.SHEET_ID_v7
const SHEET_V8 = process.env.SHEET_ID_v8
const SHEET_V9 = process.env.SHEET_ID_v9
const SHEET_V10 = process.env.SHEET_ID_v10
const SHEET_V11 = process.env.SHEET_ID_v11
const SHEET_V12 = process.env.SHEET_ID_v12
const SHEET_V13 = process.env.SHEET_ID_v13
const SHEET_V14 = process.env.SHEET_ID_v14
const SHEET_V15 = process.env.SHEET_ID_v15
const SHEET_V16 = process.env.SHEET_ID_v16
const SHEET_V17 = process.env.SHEET_ID_v17

const SHEET = process.env.SHEET_ID_v17

const SHEET_RESOURCES = process.env.RESOURCES_SHEET_ID
const SHEET_LOCALE = process.env.SHEET_LOCALE

// Sheet IDs can be obtained here: https://spreadsheets.google.com/feeds/worksheets/<HIDDEN>/private/full
const SHEET_RESOURCES_SHEET = 'otcvog0'
const SHEET_RAW_DATA = 'od6'
const SHEET_STATEWISE_TAB = 'ovd0hzm'
const SHEET_CASES_TIME_SERIES_TAB = 'o6emnqt'
const SHEET_KEY_VALUES_TAB = 'owlnkho'
const SHEET_TESTED_NUMBERS_ICMR_DATA = 'ozg9iqq'
const SHEET_STATEWISE_TESTED_NUMBERS_DATA = 'o81fdow'
const SHEET_FAQ = 'oknbjsw'
const SHEET_NAME_FACTOIDS = 'ooka3he'
const SHEET_TRAVEL_HISTORY = 'opc5w4v'
const SHEET_DATE_WISE_DELTA = 'on2tlaw'
const SHEET_DEATHS_AND_RECOVERIES = 'o3biev0'
const SHEET_SOURCES_LIST = 'obndi9r'
const SHEET_DISTRICT_WISE = 'o3rdj1v'
const SHEET_ZONES = 'oo4bpj4'
const SHEET_STATES_META_DATA = 'o3t26de'
const SHEET_DISTRICTS_META_DATA = 'ocicunx'
const SHEET_DISTRICT_TESTING_DATA = 'o7l1lwr'
const SHEET_TWITTER_QUERIES = 'oidib2z'

const DIR = './tmp/'

const FILE_RAW_DATA_1 = '/raw_data1.json'
const FILE_RAW_DATA_2 = '/raw_data2.json'
const FILE_RAW_DATA_3 = '/raw_data3.json'
const FILE_RAW_DATA_4 = '/raw_data4.json'
const FILE_RAW_DATA_5 = '/raw_data5.json'
const FILE_RAW_DATA_6 = '/raw_data6.json'
const FILE_RAW_DATA_7 = '/raw_data7.json'
const FILE_RAW_DATA_8 = '/raw_data8.json'
const FILE_RAW_DATA_9 = '/raw_data9.json'
const FILE_RAW_DATA_10 = '/raw_data10.json'
const FILE_RAW_DATA_11 = '/raw_data11.json'
const FILE_RAW_DATA_12 = '/raw_data12.json'
const FILE_RAW_DATA_13 = '/raw_data13.json'
const FILE_RAW_DATA_14 = '/raw_data14.json'
const FILE_RAW_DATA_15 = '/raw_data15.json'
const FILE_RAW_DATA_16 = '/raw_data16.json'
const FILE_RAW_DATA_17 = '/raw_data17.json'
const FILE_DEATHS_RECOVERIES_1 = '/deaths_recoveries1.json'
const FILE_DEATHS_RECOVERIES_2 = '/deaths_recoveries2.json'
const FILE_DISTRICTS = '/district_wise.json'
const FILE_DISTRICT_TESTING_DATA = '/district_testing_data.json'
const FILE_TWITTER_QUERIES = '/twitter_queries.json'
const FILE_DATA = '/data.json'
const FILE_FAQ = '/faq.json'
const FILE_WEBSITE_DATA = '/website_data.json'
const FILE_TRAVEL_HISTORY = '/travel_history.json'
const FILE_DATE_WISE_DELTA = '/states_daily.json'
const FILE_STATEWISE_TESTED_DATA = '/state_test_data.json'
const FILE_RESOURCES_ESSENTIALS = '/resources/resources.json'
const FILE_ZONES = '/zones.json'
const FILE_MISC = '/misc.json'

const FILE_SOURCES_LIST = '/sources_list.json'

module.exports = {
  SHEET_STATES_META_DATA,
  SHEET_DISTRICTS_META_DATA,
  SHEET,
  SHEET_v1: SHEET_V1,
  SHEET_v2: SHEET_V2,
  SHEET_v3: SHEET_V3,
  SHEET_v4: SHEET_V4,
  SHEET_v5: SHEET_V5,
  SHEET_v6: SHEET_V6,
  SHEET_v7: SHEET_V7,
  SHEET_v8: SHEET_V8,
  SHEET_v9: SHEET_V9,
  SHEET_v10: SHEET_V10,
  SHEET_v11: SHEET_V11,
  SHEET_v12: SHEET_V12,
  SHEET_v13: SHEET_V13,
  SHEET_v14: SHEET_V14,
  SHEET_v15: SHEET_V15,
  SHEET_v16: SHEET_V16,
  SHEET_v17: SHEET_V17,
  SHEET_RESOURCES,
  SHEET_LOCALE,
  SHEET_RAW_DATA,
  SHEET_STATEWISE_TAB,
  SHEET_CASES_TIME_SERIES_TAB,
  SHEET_KEY_VALUES_TAB,
  SHEET_Tested_Numbers_ICMR_Data: SHEET_TESTED_NUMBERS_ICMR_DATA,
  SHEET_FAQ,
  SHEET_NAME_FACTOIDS,
  SHEET_TRAVEL_HISTORY,
  SHEET_DATE_WISE_DELTA,
  SHEET_StateWise_Tested_Numbers_Data: SHEET_STATEWISE_TESTED_NUMBERS_DATA,
  SHEET_DEATHS_AND_RECOVERIES,
  SHEET_SOURCES_LIST,
  SHEET_DISTRICT_WISE,
  SHEET_ZONES,
  SHEET_DISTRICT_TESTING_DATA,
  SHEET_TWITTER_QUERIES,
  DIR,
  // FILE_RAW_DATA,
  FILE_RAW_DATA_1,
  FILE_RAW_DATA_2,
  FILE_RAW_DATA_3,
  FILE_RAW_DATA_4,
  FILE_RAW_DATA_5,
  FILE_RAW_DATA_6,
  FILE_RAW_DATA_7,
  FILE_RAW_DATA_8,
  FILE_RAW_DATA_9,
  FILE_RAW_DATA_10,
  FILE_RAW_DATA_11,
  FILE_RAW_DATA_12,
  FILE_RAW_DATA_13,
  FILE_RAW_DATA_14,
  FILE_RAW_DATA_15,
  FILE_RAW_DATA_16,
  FILE_RAW_DATA_17,
  // FILE_DEATHS_RECOVERIES,
  FILE_DEATHS_RECOVERIES_1,
  FILE_DEATHS_RECOVERIES_2,
  SHEET_RESOURCES_SHEET,
  FILE_DATA,
  FILE_FAQ,
  FILE_WEBSITE_DATA,
  FILE_TRAVEL_HISTORY,
  FILE_DATE_WISE_DELTA,
  FILE_STATEWISE_TESTED_DATA,
  FILE_RESOURCES_ESSENTIALS,
  FILE_SOURCES_LIST,
  FILE_DISTRICTS,
  FILE_ZONES,
  FILE_MISC,
  FILE_DISTRICT_TESTING_DATA,
  FILE_TWITTER_QUERIES
}
