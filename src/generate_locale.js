const fs = require('fs');
const locales = require('../tmp/locales.json');

var dir = './tmp/locales/';
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}


console.log(locales.locales[0]);
all_files = {};

for (key in locales.locales[0]) {
    all_files[key] = {};
}

locales.locales.forEach(element => {
    for (key in element) {
        all_files[key][element["english"]] = element[key];
    }

});

for (key in all_files){
    fs.writeFileSync("./tmp/locales/locale_"+key+".json", JSON.stringify(all_files[key], null, 2));
}