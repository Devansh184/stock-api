from flask import Flask, request, jsonify
import pandas as pd
import os
from dotenv import load_dotenv
from glob import glob

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

# Load all Excel files from the current directory
dataframes = {}

for file_path in glob("*.xlsx"):
    ticker_name = os.path.splitext(os.path.basename(file_path))[0].upper()  # e.g., TCS from TCS.xlsx
    try:
        df = pd.read_excel(file_path)
        dataframes[ticker_name] = df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

@app.route("/")
def home():
    return "Welcome to FinQube Stock API"

@app.route("/get_stock_data", methods=["GET"])
def get_stock_data():
    key = request.args.get("api_key")
    ticker = request.args.get("ticker")

    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    ticker = ticker.upper()

    if ticker not in dataframes:
        return jsonify({"error": "Stock not found"}), 404

    data = dataframes[ticker]
    return data.to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
