from flask import Flask, request, jsonify
import requests
import os

# --- L'objet 'app' doit être ici, tout en haut ---
app = Flask(__name__)

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # URL simplifiée pour le modèle
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Raconte une histoire complète d'au moins 250 mots sur : {topic}. Pas d'émojis."}]}]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        if 'candidates' in response_data:
            story = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"story": story})
        else:
            return jsonify({"error": str(response_data)}), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
