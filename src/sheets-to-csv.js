const fetch = require('node-fetch')
var fs = require('fs')

var dir = './tmp/csv/'
if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir, { recursive: true })
}

var latestDir = dir + 'latest'

if (!fs.existsSync(latestDir)) {
  fs.mkdirSync(latestDir)
}

// Published sheets
const PUBLISHED_SHEET_ID_1 = '2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4'
const PUBLISHED_SHEET_ID_2 = '2PACX-1vRodtoTyQwXckfuvuQllkMhGC_gruigaaizVc8I6-BZWeetYpmRyexnO75ep7rnSxFICd8c9dfpwU8I'
const PUBLISHED_SHEET_ID_3 = '2PACX-1vR_17UovavD4X7m_pqzmXjA_kCjGxIapemdWpRhDELHR1LbLJ-EVbxjKgeQat489BFRZ9bqMf-ILe_H'
const PUBLISHED_SHEET_ID_4 = '2PACX-1vSeAoAk_iMv7cQ0tldZC7aivJmGKM5Wpc5VVr37Nzv-geTmtr6pDMb-oDK59RS21Om80-SYR3jRp6qq'
const PUBLISHED_SHEET_ID_5 = '2PACX-1vSEikAgjAB9x7yhx4zNOUGLIx8Zfy2mAzRv0K1tbw08g73MO88-bbWCsgmhJ0uXa0gtuUlLMOnE9h26'
const PUBLISHED_SHEET_ID_6 = '2PACX-1vQQmgjCktQknnTPy-s4OFycu-imtoMCrWY5M2Lqig3nhGyy6W5E27xbCyaaKV9lGaDWmTzGWVzPH9-S'
const PUBLISHED_SHEET_ID_7 = '2PACX-1vR6blqV85tiBO-9u4MCW72qXALS3f7yQD0iV47MbsmIcKrvBDTorIVrUJ96QrxUj7iwAviYiecjp8VU'
const PUBLISHED_SHEET_ID_8 = '2PACX-1vR1zl3JStozuCgPsPol19f9k_io1ABmHS_mOl9gzWxiDd2_WvWhdfhePXBFZIUFjpW-gPfPwE9m7AA_'
const PUBLISHED_SHEET_ID_9 = '2PACX-1vRb4AsEPrV4b0S4j2vQku-J5XHnh8c_8fzmIhD2S2aMc2if7g6bLwJNYOPV8UmrrNR-Bv0C0yjcUnU3'
const PUBLISHED_SHEET_ID_10 = '2PACX-1vQyBRow24Pc7Wm_mSjU3JDy_Ua5mFByz6zE7-vFguBvUOdcr-90PgNcTBOCL-nTa40WrghiAN-kSFVX'
const PUBLISHED_SHEET_ID_11 = '2PACX-1vTd_tTI33CBI4obGaKTo0dfw1cNu5dUz4OIIhdbWJVmZJlEVslMyWzky1ifb9uRmV0siVxneBW4iBwi'
const PUBLISHED_SHEET_ID_12 = '2PACX-1vRCvn9X8LdOLYpiq_8U8Ihw8m_q0Lrl0Gkx4kJ22dhxX9Biy-Bhc0KWWxFQ9Fk2oS5pjgPNEd4I4XHD'
const PUBLISHED_SHEET_ID_13 = '2PACX-1vT6RKqvY0VzMaN7pKyYPyVXvUYR5cu3L5Z0sTeayDRE72xCXqVU-rhgyAucjGMJDDG5rXRKInPChqrJ'
const PUBLISHED_SHEET_ID_14 = '2PACX-1vQujsobkf1XNHg60LutKI8SXXITPGEtSx7F2sR0rBIm_FnFqXKfhz1MnZ1hIAyVAyhbPXbaf5NLXG-Q'
const PUBLISHED_SHEET_ID_15 = '2PACX-1vTsiPxkxMFJWmQQegSkpZgf3dNLqY7gc4msrnCbARgdNrr0wa9dbEDmtW9OzCrGeAmLDL1idbxU_gUk'
const PUBLISHED_SHEET_ID_16 = '2PACX-1vTDdjG51mUgQXFlBigDAF5QTpA9YL9XbhVZzjKSMqcsrD3dx9LeJfGdyBabsReECgyazhCNd3YOHQOa'
const PUBLISHED_SHEET_ID_17 = '2PACX-1vTWUT8wCTjJvROykckn6C30jNt2YVqS6zWyxKs4t0YtKfNAzJ7hxh7OggnZ3RjRokxYqSgvYEON9icz'

const SHEETS_V1 = [
  ['raw_data1', '0'],
  ['death_and_recovered1', '200733542']
]

const SHEETS_V2 = [
  ['raw_data2', '0'],
  ['death_and_recovered2', '200733542']
]

const SHEETS_V3 = [
  ['raw_data3', '0'],
  ['districts_26apr_gospel', '1964493192']
]

const SHEETS_V4 = [
  ['raw_data4', '0']
]

const SHEETS_V5 = [
  ['raw_data5', '0']
]

const SHEETS_V6 = [
  ['raw_data6', '0']
]

const SHEETS_V7 = [
  ['raw_data7', '0']
]

const SHEETS_V8 = [
  ['raw_data8', '0']
]

const SHEETS_V9 = [
  ['raw_data9', '0']
]

const SHEETS_V10 = [
  ['raw_data10', '0']
]

const SHEETS_V11 = [
  ['raw_data11', '0']
]

const SHEETS_V12 = [
  ['raw_data12', '0']
]

const SHEETS_V13 = [
  ['raw_data13', '0']
]

const SHEETS_V14 = [
  ['raw_data14', '0']
]

const SHEETS_V15 = [
  ['raw_data15', '0']
]

const SHEETS_V16 = [
  ['raw_data16', '0']
]

const SHEETS_V17 = [
  ['raw_data17', '0'],
  ['state_wise', '1896310216'],
  ['state_wise_daily', '1395461826'],
  ['sources_list', '704389477'],
  ['district_wise', '227379561'],
  ['statewise_tested_numbers_data', '486127050'],
  ['case_time_series', '387368559'],
  ['tested_numbers_icmr_data', '2143634168'],
  //     ["travel_history", "1532084277"],
  ['district_list', '1207378023'],
  ['district_testing', '458610673'],
  ['icmr_labs_statewise','847799380'],
  ['icmr_rtpcr_tests_daily','1032515506'],
]

async function sheetsToCSV (sheets, pubId) {
  for (var element of sheets) {
    console.log('Reading: ' + element[0])
    var tempUrl = 'https://docs.google.com/spreadsheets/d/e/' + pubId + '/pub?gid=' + element[1] + '&single=false&output=csv'
    console.log(tempUrl)
    var url = encodeURI(tempUrl)
    const settings = { method: 'Get' }
    await fetch(url, settings).then(res => res.text())
      .then(csv => {
        if (csv.includes('</html>')) {
          console.error('probably not csv!')
          process.exit(1)
        } else {
          // fs.writeFileSync(today_dir + "/" + element[0] + ".csv", csv);
          fs.writeFileSync(latestDir + '/' + element[0] + '.csv', csv)
          console.log('Write completed: ' + element[0])
        }
      })
  };
}

(async function main () {
  // uncomment below and run when changes in v1 sheet
  // await sheetsToCSV(SHEETS_V1, PUBLISHED_SHEET_ID_1)
  // await sheetsToCSV(SHEETS_V2, PUBLISHED_SHEET_ID_2)
  // await sheetsToCSV(SHEETS_V3, PUBLISHED_SHEET_ID_3)
  // await sheetsToCSV(SHEETS_V4, PUBLISHED_SHEET_ID_4)
  // await sheetsToCSV(SHEETS_V5, PUBLISHED_SHEET_ID_5)
  // await sheetsToCSV(SHEETS_V6, PUBLISHED_SHEET_ID_6)
  // await sheetsToCSV(SHEETS_V7, PUBLISHED_SHEET_ID_7)
  // await sheetsToCSV(SHEETS_V8, PUBLISHED_SHEET_ID_8)
  // await sheetsToCSV(SHEETS_V9, PUBLISHED_SHEET_ID_9)
  // await sheetsToCSV(SHEETS_V10, PUBLISHED_SHEET_ID_10)
  // await sheetsToCSV(SHEETS_V11, PUBLISHED_SHEET_ID_11)
  // await sheetsToCSV(SHEETS_V12, PUBLISHED_SHEET_ID_12)
  // await sheetsToCSV(SHEETS_V13, PUBLISHED_SHEET_ID_13)
  // await sheetsToCSV(SHEETS_V14, PUBLISHED_SHEET_ID_14)
  // await sheetsToCSV(SHEETS_V15, PUBLISHED_SHEET_ID_15)
  await sheetsToCSV(SHEETS_V16, PUBLISHED_SHEET_ID_16)
  await sheetsToCSV(SHEETS_V17, PUBLISHED_SHEET_ID_17)
})()
