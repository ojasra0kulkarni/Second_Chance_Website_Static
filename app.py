import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
# Enable CORS
CORS(app)

# Supabase Setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client only if credentials exist
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Successfully connected to Supabase.")
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
else:
    print("WARNING: SUPABASE_URL and SUPABASE_KEY environment variables are not set.")

@app.route('/api/submit', methods=['POST'])
def submit_profile():
    if not supabase:
        return jsonify({"error": "Database connection not configured. Please set Supabase environment variables."}), 500

    data = request.json
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    required_fields = ['full_name', 'email', 'age', 'gender', 'height', 'weight', 'caste', 'religion', 'mother_tongue', 'phone', 'state', 'city', 'marital_status', 'children', 'occupation', 'education', 'bio', 'expectations']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Prepare data for insertion
        insert_data = {
            "full_name": data['full_name'],
            "email": data['email'],
            "age": int(data['age']),
            "gender": data['gender'],
            "height": data['height'],
            "weight": int(data['weight']),
            "caste": data['caste'],
            "religion": data['religion'],
            "mother_tongue": data['mother_tongue'],
            "phone": data['phone'],
            "state": data['state'],
            "city": data['city'],
            "marital_status": data['marital_status'],
            "children": data['children'],
            "num_children": int(data.get('num_children')) if data.get('num_children') else None,
            "occupation": data['occupation'],
            "education": data['education'],
            "bio": data['bio'],
            "expectations": data['expectations']
        }

        # Insert into Supabase table 'profiles'
        response = supabase.table("profiles").insert(insert_data).execute()
        
        return jsonify({"status": "success", "message": "Profile submitted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
