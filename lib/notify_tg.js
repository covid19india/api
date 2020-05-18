const fetch = require('node-fetch');
CHAT_ID = "-1001363035222";
e = process.argv[3]
if (e=="success"){
    return;
}
BOT_TOKEN = process.argv[2];
var temp_url = "https://api.telegram.org/bot" + BOT_TOKEN + 
"/sendmessage?disable_web_page_preview=true&chat_id="+CHAT_ID+"&text=GitHub Action Status: "+e+"\n\nhttps://github.com/covid19india/api/actions";
url = encodeURI(temp_url);
let settings = { method: "Get" };
fetch(url, settings).then(res => res.json())
    .then(json => {});
