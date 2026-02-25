from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, get_db_connection
import os
import sqlite3

app = Flask(__name__)
# Enable CORS for local development matching the frontend
CORS(app)

# Initialize the database and table if they don't exist
init_db()

@app.route('/api/submit', methods=['POST'])
def submit_profile():
    data = request.json
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    required_fields = ['full_name', 'email', 'age', 'gender', 'height', 'weight', 'caste', 'religion', 'mother_tongue', 'phone', 'state', 'city', 'marital_status', 'children', 'occupation', 'education', 'bio', 'expectations']
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO profiles (
                full_name, email, age, gender, height, weight, caste, religion, 
                mother_tongue, phone, state, city, marital_status, children, 
                num_children, occupation, education, bio, expectations
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['full_name'], data['email'], int(data['age']), data['gender'], 
            data['height'], int(data['weight']), data['caste'], data['religion'], 
            data['mother_tongue'], data['phone'], data['state'], data['city'], 
            data['marital_status'], data['children'], 
            data.get('num_children'), # Can be None/null if no children
            data['occupation'], data['education'], data['bio'], data['expectations']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Profile submitted successfully"}), 201

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use port 5000 by default but respect PORT environment variable (for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
