from flask import Flask, request, jsonify
import requests
import os

# Initialisation de l'application Flask (essentiel pour Vercel)
app = Flask(__name__)

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        # Récupération sécurisée du sujet
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # Appel à l'API Google via REST
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Raconte une histoire complète et immersive pour un enfant de 5 ans sur le thème suivant : {topic}. Structure : Intro, Aventure avec péripéties, Morale constructive. Minimum 250 mots. Pas d'émojis."}]}],
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            ]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # Vérification si la réponse contient bien l'histoire
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            story = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"story": story})
        else:
            # En cas d'erreur de contenu ou de blocage par Google
            return jsonify({"error": f"Erreur de génération : {str(response_data)}"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erreur fatale : {str(e)}"}), 500

# Point d'entrée nécessaire pour certains environnements
if __name__ == '__main__':
    app.run()
