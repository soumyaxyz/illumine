// content.js
var url = 'https://ndl.iitkgp.ac.in/';

var state = 0; 
// 0 : inactive; 
// 1 : found;
// 2 : not found

//action triggered from backgrounf script, on extention button click
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
        console.log('Clicked by user. Attempting to load OA link');      
        
        if (url==null){
            console.log('Already Available in NDLI. Aborting!')
            return;
        }
        chrome.runtime.sendMessage({"message": "change_colour_default"});
        chrome.runtime.sendMessage({"message": "open_new_tab", "url": url});
    }else if ( request.message === "page_refocussed"){
        console.log('Updated icon.');
        switch (state){
            case 1: chrome.runtime.sendMessage({"message": "change_colour_open_access"});
                break;
            case 2: chrome.runtime.sendMessage({"message": "change_colour_access_restricted"});
                break;
            default:
                chrome.runtime.sendMessage({"message": "change_colour_default"});
        }
    }
  }
);


// executed on page load
runWhenLoaded()



function runWhenLoaded()
{
    var title = document.getElementsByTagName("center")[0].innerText;
    var author;     
    console.log("Title :  "+title);
    
    //checking document access status
    var subscribed = document.getElementsByClassName("panel-body")[0].childNodes[4].nodeValue;
    console.log(subscribed);
    if(subscribed == ' Open' || subscribed === ' NDLI')    {  
		console.log('Already Available in NDLI')
		chrome.runtime.sendMessage({"message": "change_colour_open_access"});
        state=1;
        url=null;
		return;
    }

    //reading metedata
    try{
    	var metadata 	= document.getElementById('metadata');
	    var metadata_A 	= metadata.childNodes[3].childNodes[5].childNodes[1].childNodes[1].childNodes[1].childNodes[1].childNodes;
	    var metadata_B 	= metadata.childNodes[3].childNodes[5].childNodes[3].childNodes[1].childNodes;
	   	
	   	author 				= get('Author', metadata_A)	   	
    		console.log("Author :  "+author);
	    var content_type 	= get('Content type', metadata_A)	
	    var file_format 	= get('File Format', metadata_A)	
	    var edu_level 		= get('Education Level', metadata_B)
	    console.log(content_type,file_format, edu_level);
	    
    }
    catch(err) {
		console.log(err.message);
		alert(err.message)
	}

    //checking if document is a research paper
    proceed = false;
    if(file_format.includes("PDF") && content_type.includes("Text")&& edu_level.includes("UG and PG") ) 
    {   
        console.log('Not Available in NDLI.\nSearching OA link')
        proceed = true;
    }
    if(proceed == false)
    {
        console.log('Type mismatch. Aborting!!')
        chrome.runtime.sendMessage({"message": "change_colour_default"});
        state = 0;
        return;
    }

    // querying  OA button for full-text
    var href;
    chrome.runtime.sendMessage({"message": "change_colour_access_restricted"});
    state = 2;
    url = open_access_button_API_call(title);
    console.log(url+ " "+ url==null)

    // full-text not found. Setting up manual search to google scholar
    if(url==null){
        url = get_google_scholar_query_string(title, author);
        console.log('Setting google scholar link = '+url);
        return;
    }

    // full-text not found through OA button.
    chrome.runtime.sendMessage({"message": "change_colour_open_access"});
    console.log('Setting OA link = '+url);
    state=1;
}

function get(field, metadata_obj){
    for (var i = 1; i< metadata_obj.length; i++) {
        if(metadata_obj[i].firstElementChild.innerText.includes(field) ){ 
            return metadata_obj[i].lastElementChild.innerText;
        }
    }
}

function open_access_button_API_call(query_str){
    var key = "dcf06ba5c24689948296823e053ab6"; 
    var url = "https://api.openaccessbutton.org/availability?url="+query_str;
    var data = JSON.parse(httpGet(url,key));
    var available = data['data']['availability'];    
    if (available == false){
    	console.log('Not available through OA button');
    	return null
    }
    return available[0]['url'];
}


function httpGet(url_api,key){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url_api, false);
    xmlHttp.setRequestHeader("x-apikey",key);
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(null);
    return xmlHttp.responseText;
}


function get_google_scholar_query_string(title, author){
    var base_url   ='https://scholar.google.co.in/scholar?hl=en&as_sdt=0%2C5&q='
    if (title.split(" ").length >5)
        return base_url+"\""+title;
    else
        return base_url+"\""+title+"\"+"+author.split("♦")[0];   
}
