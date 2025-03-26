# Customer-Segmentation-for-Financial-Product-using-Clustering
This project focuses on customer segmentation in the stock market by clustering investors based on their financial behavior. It uses machine learning models (K-means, DBSCAN, LSTM) for clustering and stock prediction, providing personalized stock recommendations to users. 

LINK:- https://customer-segmentation-for-financial.onrender.com/home

---------------------------------------------------------------------------------------------------------------------

🎯 Objectives
Customer Segmentation:
  Use K-means and DBSCAN clustering algorithms to segment customers based on their investment behavior.
  Group customers by annual income, investment risk, and preferred sectors.

Real-time Portfolio Management:
  Allow users to add and manage their stock portfolios.
  Display live stock prices and track profit/loss dynamically.
  Provide real-time portfolio value updates using WebSockets.

Stock Recommendations:
  Recommend top 4-5 Indian stocks based on:
  The user’s portfolio value.
  Stocks they have already invested in.
  Clustering insights to offer personalized suggestions.

Interactive Data Visualization:
  Display portfolio performance trends using interactive charts.
  Visualize clustering results with dynamic graphs.
  Real-time stock price updates and portfolio tracking.

---------------------------------------------------------------------------------------------------------------------

🚀 Key Features
📊 1. *Portfolio Management*
  Add stocks to the portfolio by entering:
    Stock symbol, quantity, and purchase price.
  Display:
    The number of owned stocks.
    The current portfolio value.
    Profit/Loss calculations in real-time.
    Real-time stock price updates using WebSockets.

🔥 2. *Real-time Stock Data*
Live stock prices fetched using yfinance.
Automatic portfolio value updates.
Display of current stock prices and total investment value.

📈 3. *Clustering & Segmentation*
K-means and DBSCAN algorithms to segment customers.
Clustering based on:
  Annual income
  Investment risk
  Preferred sectors
  Display clusters in interactive visualizations.

💡 4. *Stock Recommendations*
Recommend top 4-5 Indian stocks based on:
  Portfolio value.
  Stocks already owned.
  Clustering analysis insights.
  Real-time updates to offer personalized recommendations.

📊 5. *Data Visualization*
Interactive charts to display portfolio value trends.
Clustering visualizations showing grouped customer segments.
Real-time updates using Chart.js and Plotly.

🌐 6. *Responsive Frontend*
Modern UI with Flask templates (Jinja2) and Bootstrap.
Mobile-friendly and responsive design.
User-friendly navigation and dynamic content rendering.

---------------------------------------------------------------------------------------------------------------------

🔥 Technology Stack
  💻 Backend
    Python (Flask)
    MongoDB (NoSQL Database)
    Flask-SocketIO (WebSockets)
    Gunicorn + Eventlet (Production server)
    Threading for concurrent data fetching

  🌐 Frontend
    HTML5, CSS3, JavaScript
    Bootstrap (for styling)
    Chart.js / Plotly (for visualizations)

  📊 Data Science Libraries
    Pandas, NumPy (Data manipulation)
    Scikit-learn (Clustering models)
    yfinance (Real-time stock data fetching)
    Matplotlib (Data visualization)

---------------------------------------------------------------------------------------------------------------------

*SCREENSHOT*

*Home Page* :-
![image](https://github.com/user-attachments/assets/c74cfdf8-d9aa-48be-b65f-347589056ade)

*Dashboard Page*:-
![image](https://github.com/user-attachments/assets/efe5bf53-62c7-4fd7-ae78-26d2c4a21a39)

*Live market-data*:-
![image](https://github.com/user-attachments/assets/3052bbca-16c0-4dbd-b705-4083393cc6c9)
![image](https://github.com/user-attachments/assets/d395d10f-d473-4780-8988-d5e100edfe03)

*Portfolio*:-
![image](https://github.com/user-attachments/assets/8b808fb4-b494-4a7b-8696-1c5620647d07)
![image](https://github.com/user-attachments/assets/c009144d-2b04-4d1f-b5f3-fc1708cb6bc3)
![image](https://github.com/user-attachments/assets/40be2db8-746a-4ac9-a48c-1e8d1e881162)
![image](https://github.com/user-attachments/assets/bc3a6ad0-e0d8-46a6-832c-566cf1e07f12)
![image](https://github.com/user-attachments/assets/579c87d1-9d42-4261-a92f-42d46211221f)

*Stock Clustering*:-
![image](https://github.com/user-attachments/assets/abf8ea07-c60e-43ae-8230-a11bb482ead2)
![image](https://github.com/user-attachments/assets/0db3428a-a295-460b-bd73-0c1511a75287)
![image](https://github.com/user-attachments/assets/9c2510ad-d1cf-47ce-9d7a-e4a7fc34004c)

*Recommendation System*
![image](https://github.com/user-attachments/assets/6ce2f9ba-4622-4111-a3a7-01b70f528feb)
![image](https://github.com/user-attachments/assets/1157e479-ad1f-4eda-b0d0-4919fb00dc24)

*SIP Calculator*:-
![image](https://github.com/user-attachments/assets/32064059-68ea-44ec-b9c6-c57b73f56fc0)
![image](https://github.com/user-attachments/assets/59915dd3-5598-43b1-bcb4-c22476e606be)
![image](https://github.com/user-attachments/assets/b4db8255-1503-4379-a772-a853bc9d858f)









