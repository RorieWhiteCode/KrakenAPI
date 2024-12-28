const socket = io();

// Fetch and display portfolio data
async function fetchPortfolio() {
    const response = await fetch('/api/portfolio');
    const data = await response.json();
    document.getElementById('portfolio').innerText = JSON.stringify(data, null, 2);
}

// Fetch and display sentiment data
async function fetchSentiment() {
    const response = await fetch('/api/sentiment');
    const data = await response.json();
    document.getElementById('sentiment').innerText = JSON.stringify(data, null, 2);
}

// Fetch and display trade log
async function fetchTradeLog() {
    const response = await fetch('/api/trade_log');
    const data = await response.json();
    Plotly.newPlot('equity-curve', [{
        x: data.map(d => d.timestamp),
        y: data.map(d => d.profit_loss),
        type: 'scatter',
        mode: 'lines',
        name: 'Equity Curve'
    }]);
}

// Real-time updates
socket.on('connect', () => {
    console.log('Connected to dashboard server');
    fetchPortfolio();
    fetchSentiment();
    fetchTradeLog();
});
