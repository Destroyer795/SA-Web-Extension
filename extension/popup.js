const API_URL = "https://destroyer795-sentiment-analyzer-extension.hf.space/predict";

chrome.storage.local.get(["lastSelection"], (res) => {
  if (res.lastSelection) runAnalysis(res.lastSelection);
});

async function runAnalysis(text) {
  if (!text) return;

  document.getElementById("empty-state").classList.add("hidden");
  document.getElementById("results").classList.add("hidden");
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("selected-text").innerText = text;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();
    updateUI(data);
  } catch (e) {
    document.getElementById("loading").innerHTML =
      '<p>Connection error</p>';
  }
}

function updateUI(data) {
  document.getElementById("loading").classList.add("hidden");

  const results = document.getElementById("results");
  results.classList.remove("hidden");

  // trigger smooth animation
  results.offsetHeight;
  results.classList.add("visible");

  const badge = document.getElementById("sentiment-badge");
  const bar = document.getElementById("confidence-bar");
  const icon = document.getElementById("sentiment-icon");
  const flag = document.getElementById("flag-tag");
  const statusDot = document.getElementById("status-dot");

  const rawScore = data.score || 0;
  const displayScore = (rawScore * 100).toFixed(1);

  badge.innerText = data.sentiment;
  badge.className = "badge";
  statusDot.className = "status-dot";

  if (data.sentiment.toLowerCase() === "positive") {
    icon.src = "4.jpeg";
    badge.classList.add("pos");
    statusDot.classList.add("pos");
  } else if (data.sentiment.toLowerCase() === "negative") {
    icon.src = "5.jpeg";
    badge.classList.add("neg");
    statusDot.classList.add("neg");
  } else {
    icon.src = "3.jpeg";
    badge.classList.add("neu");
    statusDot.classList.add("neu");
  }

  setTimeout(() => {
    bar.style.width = displayScore + "%";
  }, 100);

  document.getElementById("score-text").innerText = displayScore + "%";
  flag.innerText = (data.confidence_flag || "Normal") + " certainty";
}
