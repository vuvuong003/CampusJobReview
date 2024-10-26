// content.js
const jobElement = document.querySelector("h2.ce-jazzhr-title");
if (jobElement) {
  const jobTitle = jobElement.textContent.trim();
  chrome.runtime.sendMessage({ jobTitle });
  console.log("Job title sent to background.js:", jobTitle);
} else {
  console.error("Job title element not found on the page.");
}
