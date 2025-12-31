/**
 * Sentiment Analyzer Pro - Background Script
 * ------------------------------------------
 * Handles context menu creation and interaction with the backend API.
 * It sends selected text to the analysis server and displays the result via notifications.
 */

// Register the context menu item when the extension is installed
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeSentiment",
    title: "Analyze Sentiment",
    contexts: ["selection"]
  });
});

// Event listener for context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeSentiment" && info.selectionText) {
    analyzeSentiment(info.selectionText);
  }
});

/**
 * Sends the selected text to the backend API for sentiment analysis
 * and displays the result in a Chrome notification.
 * 
 * @param {string} text - The text selected by the user.
 */
async function analyzeSentiment(text) {
  try {
    // Replace with your actual backend URL if different
    const response = await fetch("https://destroyer795-trial.hf.space/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    const scorePercent = (data.score * 100).toFixed(1);

    // Determine the appropriate icon based on sentiment
    // 4.jpeg = Positive, 5.jpeg = Negative, 3.jpeg = Neutral/Mixed
    let iconFile = "3.jpeg";
    if (data.sentiment === "Positive") {
      iconFile = "4.jpeg";
    } else if (data.sentiment === "Negative") {
      iconFile = "5.jpeg";
    }

    // Display the result
    chrome.notifications.create({
      type: "basic",
      iconUrl: iconFile,
      title: `Sentiment: ${data.sentiment}`,
      message: `Confidence Score: ${scorePercent}%`
    });
  } catch (error) {
    console.error("[Sentiment Analyzer] Error:", error);
    chrome.notifications.create({
      type: "basic",
      iconUrl: "3.jpeg",
      title: "Error",
      message: "Failed to analyze sentiment. Please try again."
    });
  }
}
