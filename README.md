# Sales Forecast Dashboard

A React dashboard for visualizing sales data and machine learning predictions.

## Features

- 📊 Interactive charts for historical and forecasted sales data
- 🧠 Multiple machine learning models visualization (Linear Regression, XGBoost, LSTM)
- 📈 Seasonality analysis
- 🏆 Top selling items tracking
- 📉 Model performance metrics
- 🐍 Python integration with your existing sales_forecast.py script

## Prerequisites

- Node.js (v14+)
- npm or yarn
- Python 3.6+ (for the backend/ML models)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

3. Place your CSV data file in the `public` folder:

```bash
cp train.csv public/
```

## Running the Application

### Start the React Frontend

```bash
npm start
```

The application will be available at http://localhost:3000

### Setting up the Python Backend (Optional)

For full functionality, you'll want to create a backend API that runs your sales_forecast.py script:

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the necessary packages:

```bash
pip install flask pandas numpy matplotlib xgboost scikit-learn tensorflow flask-cors
```

3. Create a simple API wrapper for your script (example in `server.py`)

4. Run the Flask server:

```bash
python server.py
```

## Connecting the Frontend to the Python Backend

The dashboard is set up to call the backend API when the "Run ML Models" button is clicked. By default, it simulates this functionality, but you can modify the code in the `runPythonScript` function in `App.js` to make actual API calls.

## Customization

- **Models**: You can add or remove models by modifying the `generatePredictions` function
- **Timeframes**: Edit the timeframe dropdown in the controls section
- **Styling**: Customize the appearance by editing the CSS files

## Project Structure

- `src/App.js` - Main application component
- `src/App.css` - Styling for the dashboard
- `public/train.csv` - Your sales data
- `sales_forecast.py` - Your existing Python ML script

## Future Enhancements

- Add more sophisticated ML models
- Implement anomaly detection
- Create store-level dashboards
- Add data export functionality
- Implement user authentication

## License

MIT
