from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # Appel direct à l'API Google via REST (plus robuste)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Raconte une histoire complète d'au moins 250 mots sur : {topic}. Structure : Intro, Aventure, Morale. Pas d'émojis."}]
            }]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # Extraction du texte
        story = response_data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"story": story})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
