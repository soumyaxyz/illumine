// background.js

// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
  // Send a message to the active tab
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, {"message": "clicked_browser_action"});
  });
});



chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "open_new_tab" ) {
      chrome.tabs.create({"url": request.url});
    }
  }
);

//handle user clicking other tab or window and comming back

chrome.tabs.onActivated.addListener(function(request, sender, sendResponse) {
      chrome.browserAction.setIcon({path: "t1.png"});
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "page_refocussed"});
      });
  });


chrome.windows.onFocusChanged.addListener(function(request, sender, sendResponse) {
      chrome.browserAction.setIcon({path: "t1.png"});
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "page_refocussed"});
      });
  });

// change button icon

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "change_colour_open_access" ) {
      console.log("change_colour_open_access");
      chrome.browserAction.setIcon({path: "t3.png"});
    }
  }
);


chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "change_colour_access_restricted" ) {
      console.log("change_colour_access_restricted");
      chrome.browserAction.setIcon({path: "t2.png"});
    }
  }
);

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "change_colour_default" ) {
      chrome.browserAction.setIcon({path: "t1.png"});
    }
  }
);

