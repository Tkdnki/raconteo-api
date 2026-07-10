from flask import Flask, request, jsonify
import requests
import os

# Initialisation de l'application
app = Flask(__name__)

# La route doit correspondre au chemin Flutter
@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Raconte une histoire complète et immersive pour un enfant de 5 ans sur : {topic}. Structure : Intro, Aventure, Morale. Minimum 250 mots. Pas d'émojis."}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            ]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            story = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"story": story})
        else:
            return jsonify({"error": f"Erreur Google : {str(response_data)}"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erreur code : {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
