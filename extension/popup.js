// popup.js
chrome.runtime.sendMessage({ action: "getJobTitle" }, (response) => {
    if (response && response.jobTitle) {
      document.getElementById("jobTitle").textContent = response.jobTitle;
    } else {
      document.getElementById("jobTitle").textContent = "Job title not found.";
    }
  });
  