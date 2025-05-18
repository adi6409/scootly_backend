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
        baseurl = row['Auto-Discovery URL'].split('/gbfs.json')[:-1]
        # combine the list into a string
        gbfs_url = ''.join(baseurl)
        providers.append({
            "id": row['System ID'],
            "name": row['Name'],
            "icon": DEFAULT_ICON,
            # for gbfs endpoint, we take the URL and remove the last part (split by / and find the lase) and put the rest
            "gbfsEndpoint": gbfs_url,
            "gbfsEndpoints": DEFAULT_ENDPOINTS,
            "features": DEFAULT_FEATURES,
            "addJson": True if ".json" in row['Auto-Discovery URL'] else False,
        })

    return jsonify({
        "statusCode": 200,
        "data": providers
    })

@app.route("/api/getProvider", methods=['GET'])
def get_provider():
    provider_id = request.args.get('id', '')
    if not provider_id:
        return jsonify({"statusCode": 400, "data": [], "error": "Missing 'id' parameter"}), 400

    filtered = df[df['System ID'].str.lower() == provider_id.lower()]
    if filtered.empty:
        return jsonify({"statusCode": 404, "data": [], "error": "Provider not found"}), 404

    row = filtered.iloc[0]
    baseurl = row['Auto-Discovery URL'].split('/gbfs.json')[:-1]
    gbfs_url = ''.join(baseurl)

    provider = {
        "id": row['System ID'],
        "name": row['Name'],
        "icon": DEFAULT_ICON,
        "gbfsEndpoint": gbfs_url,
        "gbfsEndpoints": DEFAULT_ENDPOINTS,
        "features": DEFAULT_FEATURES,
        "addJson": True if ".json" in row['Auto-Discovery URL'] else False,
    }

    return jsonify({
        "statusCode": 200,
        "data": provider
    })

if __name__ == '__main__':
    app.run(debug=True, port=5555)
