async function submitQuery() {
    const userInputEl = document.getElementById('user-input');
    const submitButtonEl = document.getElementById('submit-button');
    const loadingEl = document.getElementById('loading');
    const analysisContentEl = document.getElementById('analysis-content');
    const genericResponseEl = document.getElementById('generic-response');
    const errorMessageEl = document.getElementById('error-message');

    const userInput = userInputEl.value.trim();

    if (!userInput) {
        errorMessageEl.textContent = "Please enter a query.";
        errorMessageEl.style.display = 'block';
        return;
    }

    errorMessageEl.style.display = 'none';
    userInputEl.disabled = true;
    submitButtonEl.disabled = true;
    loadingEl.style.display = 'block';
    analysisContentEl.classList.add('hidden');
    genericResponseEl.classList.add('hidden');

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: userInput }),
        });

        const rawData = await response.json();
        console.log("🌟 Raw data received:", rawData);

        const responseData = rawData.response;

        if (responseData && responseData.ticker && responseData.financial_summary_table) {
            console.log("🔍 Structured financial response detected. Updating UI.");

            const handleNaN = (value) => {
                if (value === "N/A") return "N/A";
                if (value === undefined || value === null || value === '') {
                    console.log("Warning: Missing value for", value);
                    return 'N/A';
                }
                return isNaN(value) ? 'N/A' : value;
            };

            const updateUI = (data, rawData) => {
                console.log('Updating UI with analysis:', data);

                const ticker = rawData.response.ticker;
                console.log("Ticker:", ticker);
                document.getElementById('ticker').textContent = ticker;

                const financialSummary = rawData.response.financial_summary_table;
                if (financialSummary && financialSummary.length > 0) {
                    const firstYearData = financialSummary[0];

                    document.getElementById('revenue').textContent = `$${handleNaN(firstYearData.Revenue).toLocaleString()}`;
                    document.getElementById('eps').textContent = handleNaN(firstYearData["EPS Diluted"]).toFixed(2);
                    document.getElementById('free-cash-flow').textContent = `$${handleNaN(firstYearData["Free Cash Flow"]).toLocaleString()}`;
                    document.getElementById('ebitda').textContent = `$${handleNaN(firstYearData.EBITDA).toLocaleString()}`;
                    document.getElementById('roe').textContent = `${handleNaN(firstYearData["ROE (%)"]).toFixed(2)}%`;
                    document.getElementById('pe-ratio').textContent = handleNaN(firstYearData["P/E Ratio"]).toFixed(2);
                    document.getElementById('debt-to-equity').textContent = handleNaN(firstYearData["Debt to Equity"]).toFixed(2);
                } else {
                    throw new Error('Financial summary data is missing.');
                }

                document.getElementById('bullish-text').innerHTML = data.bullish || "N/A";
                document.getElementById('bearish-text').innerHTML = data.bearish || "N/A";
                document.getElementById('recommendation-text').innerHTML = data.recommendation || "N/A";

                document.getElementById('investment-score-value').textContent = data.investment_score || "N/A";
                document.getElementById('file-saved').textContent = `📁 Excel file saved: ${rawData.response.file_saved}`;

                // Remove 'hidden' and add 'visible' to trigger fade-in effect
                analysisContentEl.classList.remove('hidden');
                analysisContentEl.classList.add('visible');
            };

            // Call the function to update UI with financial data
            updateUI(responseData.analysis, rawData);

        } else {
            console.log("📝 Generic response detected. Showing simple text.");
            
            // Hide the analysis content and show the generic response
            analysisContentEl.classList.add('hidden');
            const genericText = typeof rawData.response === 'string' ? rawData.response : JSON.stringify(rawData.response, null, 2);
            genericResponseEl.innerText = genericText;
            genericResponseEl.classList.remove('hidden');
        }

    } catch (error) {
        console.error(error);
        alert('An error occurred: ' + error.message);
    } finally {
        loadingEl.style.display = 'none';
        userInputEl.disabled = false;
        submitButtonEl.disabled = false;
    }
}

// Listen for "Enter" key to trigger submit
document.getElementById('user-input').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        submitQuery();
    }
});