from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
import datetime

app = Flask(__name__)
CORS(app)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/release_architect_db")
client = MongoClient(mongo_uri)
db = client.get_database()
releases_collection = db.releases

# =================
# App Methods
# =================

# AI helped with this function
def ai_assisted_note_parser(raw_input_text):
    """
    Helper text-processing logic developed with AI assistance.
    Categorizes raw developer bullets into standardized buckets for clean rendering.
    """
    features = []
    bug_fixes = []
    maintenance = []

    lines = [line.strip() for line in raw_input_text.split('\n') if line.strip()]

    for line in lines:
        clean_line = line.lstrip('-*• ').strip()
        lower_line = clean_line.lower()
    
        if any(keyword in lower_line for keyword in ['fix', 'bug', 'issue', 'resolve', 'error', 'crash']):
            bug_fixes.append(clean_line[0].upper() + clean_line[1:])
        elif any(keyword in lower_line for keyword in ['add', 'feat', 'create', 'new', 'implement', 'ui', 'page']):
            features.append(clean_line[0].upper() + clean_line[1:])
        else:
            maintenance.append(clean_line[0].upper() + clean_line[1:])
    
    if not features and not bug_fixes and not maintenance:
        features.append("Internal codebase optimizations and minor upgrades implemented.")
    
    return {
        "features": features,
        "bug_fixes": bug_fixes,
        "maintenance": maintenance
    }

# Helper function to convert MongoDB BSON objects to JSON 
def serialize_release(doc):
    if not doc:
        return None
    doc['_id'] = str(doc['_id'])
    return doc

# =================
# Rest API Routes
# =================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flask backend and MongoDB collection layers are live!"}), 200

# Create
@app.route('/api/releases', methods=['POST'])
def create_release():
    data = request.get_json()

    if not data or 'version' not in data or 'title' not in data or 'raw_input' not in data:
        return jsonify({"error": "Missing required data properties (version, title, raw_input)."}), 400
    
    structured_changelog = ai_assisted_note_parser(data['raw_input'])

    new_release = {
        "version": data['version'],
        "title": data['title'],
        "raw_input": data['raw_input'],
        "changelog": structured_changelog,
        "is_published": False,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    result = releases_collection.insert_one(new_release)
    new_release['_id'] = str(result.inserted_id)

    return jsonify(new_release), 201

# Read
@app.route('/api/releases', methods=['GET'])
def get_all_releases():
    try:
        cursor = releases_collection.find().sort("created_at", -1)
        releases_list = [serialize_release(doc) for doc in cursor]
        return jsonify(releases_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read: For the Published Notes Only
@app.route('/api/releases/published', methods=['GET'])
def get_published_releases():
    try:
        cursor = releases_collection.find({"is_published": True}).sort("created_at", -1)
        releases_list = [serialize_release(doc) for doc in cursor]
        return jsonify(releases_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Update
@app.route('/api/releases/<string:release_id>', methods=['PUT'])
def update_release_status(release_id):
    data = request.get_json()
    if not data or 'is_published' not in data:
        return jsonify({"error": "Missing 'is_published' boolean flag parameter."}), 400
    
    try:
        result = releases_collection.update_one(
            {"_id": ObjectId(release_id)},
            {"$set": {"is_published": data['is_published']}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Target release note document not found."}), 404

        return jsonify({"message": "Document status updated successfully.", "id": release_id}), 200
    except Exception as e:
        return jsonify({"error": "Invalid document ID format or database failure."}), 400

# Delete
@app.route('/api/releases/<string:release_id>', methods=['DELETE'])
def delete_release(release_id):
    try:
        result = releases_collection.delete_one({"_id": ObjectId(release_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Target release note document not found."}), 404

        return jsonify({"message": "Release log permanently cleared.", "id": release_id}), 200
    except Exception as e:
        return jsonify({"error": "Invalid document ID format or database failure."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)