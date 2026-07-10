@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        api_key = os.environ.get("GEMINI_API_KEY")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Écris une histoire pour enfant sur : {topic}. Fais 200 mots."}]}],
            "safetySettings": [ # On assouplit les filtres de sécurité
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            ]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # Vérification si 'candidates' existe avant d'essayer de l'utiliser
        if 'candidates' in response_data:
            story = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"story": story})
        else:
            # Si pas de 'candidates', on renvoie TOUTE la réponse pour comprendre
            return jsonify({"error": f"Réponse inattendue de Google : {str(response_data)}"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erreur fatale : {str(e)}"}), 500
