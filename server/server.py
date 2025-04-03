from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
import sys
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data', methods=['GET'])
def get_data():
    """Return processed monthly sales data"""
    try:
        # Read the CSV data
        store_sales = pd.read_csv('../public/train.csv')
        
        # Process the data (similar to your Python script)
        store_sales = store_sales.drop(['store', 'item'], axis=1)
        store_sales['date'] = pd.to_datetime(store_sales['date'])
        store_sales['date'] = store_sales['date'].dt.to_period("M")
        monthly_sales = store_sales.groupby('date').sum().reset_index()
        monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
        
        # Convert to list of dictionaries for JSON response
        data = []
        for _, row in monthly_sales.iterrows():
            data.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'sales': float(row['sales'])
            })
            
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/forecast', methods=['POST'])
def forecast():
    """Generate sales forecast using the specified model"""
    try:
        params = request.get_json()
        model_type = params.get('model', 'linear')  # Default to linear regression
        timeframe = params.get('timeframe', 12)     # Default to 12 months
        
        # Option 1: Import your script directly (if importable)
        # import sales_forecast
        # result = sales_forecast.run_forecast(model_type, timeframe)
        
        # Option 2: Run as subprocess
        # result = subprocess.run(
        #     ['python', '../sales_forecast.py', '--model', model_type, '--timeframe', str(timeframe)],
        #     capture_output=True,
        #     text=True
        # )
        
        # For demo purposes, we'll generate fake forecast data
        # In a real implementation, you would use the results from your ML models
        
        # Read and process data (as above)
        store_sales = pd.read_csv('../public/train.csv')
        store_sales = store_sales.drop(['store', 'item'], axis=1)
        store_sales['date'] = pd.to_datetime(store_sales['date'])
        store_sales['date'] = store_sales['date'].dt.to_period("M")
        monthly_sales = store_sales.groupby('date').sum().reset_index()
        monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
        
        # Get the last date in the data
        last_date = monthly_sales['date'].max()
        last_sales = monthly_sales.loc[monthly_sales['date'] == last_date, 'sales'].values[0]
        
        # Generate forecast based on model type
        forecast_data = []
        for i in range(timeframe):
            # Add one month to the last date for each prediction
            pred_date = last_date + pd.DateOffset(months=i+1)
            
            # Different growth rates based on model
            if model_type == 'linear':
                pred_sales = last_sales * (1 + 0.05 * (i/12) + np.random.normal(0, 0.02))
            elif model_type == 'xgboost':
                pred_sales = last_sales * (1 + 0.08 * (i/12) + np.random.normal(0, 0.05))
            else:  # LSTM
                pred_sales = last_sales * (1 + 0.06 * (i/12) + np.random.normal(0, 0.015))
            
            forecast_data.append({
                'date': pred_date.strftime('%Y-%m-%d'),
                'sales': float(pred_sales)
            })
        
        # Calculate some metrics
        metrics = {
            'mse': float(np.random.uniform(2000, 3000)),
            'mae': float(np.random.uniform(30, 50)),
            'r2': float(np.random.uniform(0.8, 0.95))
        }
        
        return jsonify({
            'status': 'success',
            'forecast': forecast_data,
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/items', methods=['GET'])
def top_items():
    """Return top selling items"""
    try:
        # In a real implementation, you would analyze your data
        # For demo purposes, we'll return fake data
        items = [
            {'item': 'Product A', 'sales': 125000, 'growth': 12.5},
            {'item': 'Product B', 'sales': 98000, 'growth': 8.2},
            {'item': 'Product C', 'sales': 76500, 'growth': -3.7},
            {'item': 'Product D', 'sales': 65200, 'growth': 5.1},
            {'item': 'Product E', 'sales': 42800, 'growth': 15.8}
        ]
        
        return jsonify({
            'status': 'success',
            'items': items
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)