async function submitQuery() {
  const userInput = document.getElementById("user-input").value;
  const modelOverride = document.getElementById("model-select").value;

  const responseDiv = document.getElementById("response");
  responseDiv.classList.remove("hidden");
  responseDiv.innerHTML = "<p>⏳ Processing...</p>";

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        input: userInput,
        model_override: modelOverride
      }),
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();

    if (data.response) {
      const res = data.response;
      responseDiv.innerHTML = `
        <div>
          ${res.bullish ? `<h3>📈 Bullish</h3><p>${res.bullish}</p>` : ""}
          ${res.bearish ? `<h3>📉 Bearish</h3><p>${res.bearish}</p>` : ""}
          ${res.recommendation || ""}
          <p><strong>Investment Score:</strong> ${res.investment_score || "N/A"}</p>
        </div>
      `;
    } else {
      responseDiv.innerHTML = `<p>Error: ${JSON.stringify(data)}</p>`;
    }
  } catch (err) {
    responseDiv.innerHTML = "<p>❌ Error submitting request</p>";
    console.error(err);
  }
}