from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load CSV at startup
csv_path = "systems.csv"
df = pd.read_csv(csv_path)

# Mock data (to simplify, icon and feature list are hardcoded)
DEFAULT_ICON = "https://downloadr2.apkmirror.com/wp-content/uploads/2018/07/5b47c64218d9b.png"
DEFAULT_ENDPOINTS = [
    "FREE_BIKE_STATUS",
    "GBFS_VERSIONS",
    "GEOFENCING_ZONES",
    "STATION_INFORMATION",
    "STATION_STATUS",
    "SYSTEM_INFORMATION",
    "SYSTEM_PRICING_PLANS",
    "SYSTEM_REGIONS",
    "VEHICLE_TYPES"
]
DEFAULT_FEATURES = ["BOOKING"]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Scootly API!"})

@app.route('/api/example', methods=['GET'])
def example_endpoint():
    return jsonify({"example": "This is an example endpoint"})

@app.route('/api/getCities', methods=['GET'])
def get_cities():
    unique_cities = df['Location'].dropna().unique().tolist()
    return jsonify({
        "statusCode": 200,
        "data": unique_cities
    })

@app.route('/api/getProviders', methods=['GET'])
def get_providers():
    city = request.args.get('city', '')
    if not city:
        return jsonify({"statusCode": 400, "data": [], "error": "Missing 'city' parameter"}), 400

    filtered = df[df['Location'].str.lower() == city.lower()]
    providers = []
    for _, row in filtered.iterrows():
        providers.append({
            "id": row['System ID'],
            "name": row['Name'],
            "icon": DEFAULT_ICON,
            "gbfsEndpoint": row['Auto-Discovery URL'],
            "gbfsEndpoints": DEFAULT_ENDPOINTS,
            "features": DEFAULT_FEATURES,
            "addJson": True
        })

    return jsonify({
        "statusCode": 200,
        "data": providers
    })

if __name__ == '__main__':
    app.run(debug=True)
