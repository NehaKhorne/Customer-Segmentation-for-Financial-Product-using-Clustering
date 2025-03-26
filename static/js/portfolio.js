// portfolio.js

document.addEventListener("DOMContentLoaded", function () {
    let addStockBtn = document.getElementById("addStockBtn");
    let stockSymbolInput = document.getElementById("stockSymbol");
    let stockPriceDisplay = document.getElementById("stockPrice");

    if (addStockBtn) {
        addStockBtn.addEventListener("click", function () {
            let stockSymbol = stockSymbolInput.value.toUpperCase();
            let quantity = document.getElementById("stockQuantity").value;

            if (!stockSymbol || !quantity) {
                alert("Please enter a stock symbol and quantity!");
                return;
            }

            fetch("/api/add_stock", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ symbol: stockSymbol, quantity: parseInt(quantity) })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("Stock added successfully!");
                    updatePortfolioUI();
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }

    // Fetch real-time stock price
    if (stockSymbolInput) {
        stockSymbolInput.addEventListener("input", async function () {
            let symbol = this.value.toUpperCase();
            if (symbol.length < 2) return;

            try {
                let response = await fetch(`/api/stock_price?symbol=${symbol}`);
                let data = await response.json();
                if (data.price) {
                    stockPriceDisplay.innerText = `₹${data.price}`;
                }
            } catch (error) {
                console.error("Error fetching stock price:", error);
            }
        });
    }

    // Update portfolio UI dynamically
    function updatePortfolioUI() {
        fetch("/api/portfolio")
        .then(response => response.json())
        .then(data => {
            let portfolioTable = document.getElementById("portfolioTable");
            portfolioTable.innerHTML = "<tr><th>Stock</th><th>Quantity</th><th>Price</th><th>Total Value</th></tr>";

            data.stocks.forEach(stock => {
                let row = `<tr>
                            <td>${stock.name}</td>
                            <td>${stock.quantity}</td>
                            <td>₹${stock.price.toFixed(2)}</td>
                            <td>₹${(stock.quantity * stock.price).toFixed(2)}</td>
                        </tr>`;
                portfolioTable.innerHTML += row;
            });
        });
    }
});
