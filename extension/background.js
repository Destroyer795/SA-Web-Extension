// Registering context menu on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeSentiment",
    title: "Analyze Sentiment",
    contexts: ["selection"]
  });
});

// Handle context menu click
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzeSentiment" && info.selectionText) {
    analyzeSentiment(info.selectionText);
  }
});

// Function to call backend and show result
async function analyzeSentiment(text) {
  try {
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

    // Used 4.jpeg for positive, 5.jpeg for negative, 3.jpeg for neutral
    let iconFile = "3.jpeg";
    if (data.sentiment === "Positive") {
      iconFile = "4.jpeg";
    } else if (data.sentiment === "Negative") {
      iconFile = "5.jpeg";
    }

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
