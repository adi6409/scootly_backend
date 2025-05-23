from flask import Flask, jsonify, request
from database import get_database

app = Flask(__name__)

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
    collection = get_database()
    unique_cities = collection.distinct("location")
    return jsonify({
        "statusCode": 200,
        "data": unique_cities
    })

@app.route('/api/getProviders', methods=['GET'])
def get_providers():
    city = request.args.get('city', '')
    if not city:
        return jsonify({"statusCode": 400, "data": [], "error": "Missing 'city' parameter"}), 400

    collection = get_database()
    providers_data = collection.find({"location": {"$regex": f"^{city}$", "$options": "i"}})
    
    providers = []
    for provider in providers_data:
        providers.append({
            "id": provider["system_id"],
            "name": provider["name"],
            # use icon_url from the provider, or default icon if not present
            "icon": provider["icon_url"] if "icon_url" in provider else DEFAULT_ICON,
            "gbfsEndpoint": provider["gbfs_url"],
            "gbfsEndpoints": DEFAULT_ENDPOINTS,
            "features": DEFAULT_FEATURES,
            "addJson": provider["add_json"],
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

    collection = get_database()
    provider = collection.find_one({"system_id": {"$regex": f"^{provider_id}$", "$options": "i"}})
    
    if not provider:
        return jsonify({"statusCode": 404, "data": [], "error": "Provider not found"}), 404

    return jsonify({
        "statusCode": 200,
        "data": {
            "id": provider["system_id"],
            "name": provider["name"],
            "icon": DEFAULT_ICON,
            "gbfsEndpoint": provider["gbfs_url"],
            "gbfsEndpoints": DEFAULT_ENDPOINTS,
            "features": DEFAULT_FEATURES,
            "addJson": provider["add_json"],
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5555)
