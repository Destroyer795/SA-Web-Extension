chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzeSentiment",
    title: "Analyze Sentiment",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId !== "analyzeSentiment") return;

  chrome.storage.local.set({ lastSelection: info.selectionText });

  // Open the extension popup programmatically
  chrome.action.openPopup();
});
