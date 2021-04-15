const data = require('../tmp/data.json')

var total = data.statewise[0]
var err = false
if (total.deltaconfirmed > 230000) {
  console.error('Delta confirmed is greater than the limit. Please verify')
  err = true
}

if (err) {
  console.error('Sanity check failed. Not committing!')
  process.exit(1)
} else {
  console.log('No known data errors. Proceeding to commit!')
}
