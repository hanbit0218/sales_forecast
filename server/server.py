from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import sys
import os
import json
from datetime import datetime

# Import your existing sales_forecast module
# Alternatively you can run it as a subprocess
# import sales_forecast

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/run-model', methods=['POST'])
def run_model():
    data = request.get_json()
    model_type = data.get('model', 'linear')
    
    try:
        # Option 1: Import and call your module functions
        # result = sales_forecast.run_model(model_type)
        
        # Option 2: Run as subprocess (example)
        # import subprocess
        # result = subprocess.run(
        #    ['python', '../sales_forecast.py', '--model', model_type],
        #    capture_output=True, text=True
        # )
        
        # For this example, we'll simulate the response
        # In a real implementation, you would call your actual model
        
        # Read your CSV data
        try:
            store_sales = pd.read_csv('../public/train.csv')
            
            # Process similar to your sales_forecast.py script
            store_sales = store_sales.drop(['store', 'item'], axis=1)
            store_sales['date'] = pd.to_datetime(store_sales['date'])
            
            # Group by month
            store_sales['month'] = store_sales['date'].dt.to_period('M')
            monthly_sales = store_sales.groupby('month').sum().reset_index()
            monthly_sales['date'] = monthly_sales['month'].dt.to_timestamp()
            
            # Get the latest date for forecasting
            latest_date = monthly_sales['date'].max()
            
            # Generate forecast data based on model
            forecast_data = []
            start_sales = monthly_sales['sales'].values[-1]
            
            for i in range(12):
                # Apply different forecasting logic based on model type
                if model_type == 'linear':
                    predicted = start_sales * (1 + 0.05 * (i/12))
                    mse, mae, r2 = 2504, 42.3, 0.87
                elif model_type == 'xgboost':
                    predicted = start_sales * (1 + 0.07 * (i/12))
                    mse, mae, r2 = 2215, 36.8, 0.91
                else:  # lstm
                    predicted = start_sales * (1 + 0.06 * (i/12))
                    mse, mae, r2 = 2350, 39.2, 0.89
                
                # Add some random noise
                predicted *= (1 + np.random.normal(0, 0.02))
                
                forecast_data.append({
                    'date': (latest_date + pd.DateOffset(months=i+1)).strftime('%Y-%m-%d'),
                    'sales': float(predicted)
                })
            
            return jsonify({
                'status': 'success',
                'message': f'Successfully ran {model_type} model',
                'forecast': forecast_data,
                'metrics': {
                    'mse': mse,
                    'mae': mae,
                    'r2': r2
                }
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error processing data: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)