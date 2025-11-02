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

    // Used 4.jpg for positive, 5.jpg for negative, 3.jpg for neutral
    let iconFile = "3.jpg";
    if (data.sentiment === "Positive") {
      iconFile = "4.jpg";
    } else if (data.sentiment === "Negative") {
      iconFile = "5.jpg";
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
      iconUrl: "3.jpg",
      title: "Error",
      message: "Failed to analyze sentiment. Please try again."
    });
  }
}
