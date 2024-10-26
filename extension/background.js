// background.js
let jobTitle = null;

// Listen for messages from content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.jobTitle) {
    jobTitle = message.jobTitle; // Store the job title in a variable
    console.log("Job title received in background.js:", jobTitle);
  }
});

// Allow popup.js to request the stored job title
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "getJobTitle") {
    sendResponse({ jobTitle });
  }
});
