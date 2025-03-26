var socket = io.connect("http://localhost:5000");

// Listen for stock price updates from the server
socket.on("stock_update", function(data) {
    document.getElementById("stock_price").innerText = data.price;
    document.getElementById("stock_volume").innerText = data.volume;
});

// Fallback AJAX call every 5 seconds
function fetchStockData() {
    fetch('/get_stock_data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("stock_price").innerText = data.price;
        document.getElementById("stock_volume").innerText = data.volume;
    });
}

setInterval(fetchStockData, 5000);
