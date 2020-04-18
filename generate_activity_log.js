const fs = require('fs');
const fetch = require('node-fetch');
const moment = require('moment-timezone');
const data = require('./data.json');
const data_prev = require('./data_prev.json');

update_log_file = './updatelog/log.json';
var update_log = require(update_log_file);
BOT_TOKEN = process.argv[2];


statewise_new = data.statewise.reduce((arr, row)=>{
    arr[row.state] = row;
    return arr;
},{});

var conf_text;
var recov_text;
var death_text;
var full_text = "";
var tg_full_text = "";
var isChanged = false;


data_prev.statewise.forEach(element => {
    if(element.state=="Total"){
        return;
    }
    isChanged = false;
    conf_text = null;
    recov_text = null;
    death_text = null;
    text = null;
    if(parseInt(element.confirmed) < parseInt(statewise_new[element.state].confirmed)){
        confirmed_diff = statewise_new[element.state].confirmed - element.confirmed;
        conf_text = confirmed_diff + " new case"+(confirmed_diff==1?"":"s");
        isChanged=true;
    }
    if(parseInt(element.recovered) < parseInt(statewise_new[element.state].recovered)){
        recovered_diff = statewise_new[element.state].recovered - element.recovered;
        recov_text = recovered_diff + " recover"+(recovered_diff==1?"y":"ies");
        isChanged=true;
    }
    if(parseInt(element.deaths) < parseInt(statewise_new[element.state].deaths)){
        death_diff = statewise_new[element.state].deaths - element.deaths;
        death_text = death_diff + " death"+(death_diff==1?"":"s");
        isChanged=true;
    }
    
    if(isChanged){
        text=(conf_text?conf_text+", ":"")+(recov_text?recov_text+", ":"")+(death_text?death_text+", ":"");
        arr = text.split(", ");
        if(arr.length>2){
            arr = text.split(", ");
            arr = arr.slice(0, -1);
            arr_last = arr[arr.length-1];
            arr = arr.slice(0,-1);
            text = arr.join(", ");
            text = text + " and "+arr_last
        }else{
            arr = arr.slice(0,-1);
            text = arr.join();
        }
        text = text +" in "+element.state
        full_text = full_text + text + "\n"
        
        total = statewise_new["Total"];
        tg_full_text = full_text + "\n"
            + "``` Total cases: (↑" + total.deltaconfirmed + ") " + total.confirmed
            + "\n" + " Recovered  : (↑" + total.deltarecovered + ") " + total.recovered
            + "\n" + " Deaths     : (↑" + total.deltadeaths + ") " + total.deaths + "```";
    }   
});

if (full_text!=""){
    console.log(full_text);
    
    const now = moment().unix()
    entry = {};
    entry.update = full_text;
    entry.timestamp = now;
    update_log.push(entry);
    update_log = update_log.slice(-50)
    
    fs.writeFileSync(update_log_file, JSON.stringify(update_log, null, 2));

    var date = moment.unix(now);
    formated_time = date.tz("Asia/Kolkata").format("MMMM DD, hh:mm A");
    console.log(formated_time)
    

    url = encodeURI("https://api.telegram.org/bot"+BOT_TOKEN+"/sendmessage?disable_web_page_preview=true&parse_mode=Markdown&chat_id=-1001449683810&text=_"
        +formated_time+"_\n\n"
        +tg_full_text
        +"\n\n*www.covid19india.org*");
    // console.log(url);
    let settings = { method: "Get" };
    fetch(url, settings).then(res => res.json())
	.then(json => console.log(json));
    
}else{
    console.log("No updates this time!");
}

