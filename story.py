from flask import Flask, request, jsonify
from google import genai  # Nouveau package
import os

app = Flask(__name__)

# Initialisation du client avec le nouveau SDK
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        
        # Le prompt reste structuré comme on l'a défini
        prompt = f"""
        Écris une histoire complète et structurée pour un enfant de 5 ans sur le thème : {topic}.
        La structure doit impérativement contenir :
        1. Une introduction poétique.
        2. Une aventure avec une péripétie intéressante.
        3. Une conclusion avec une morale bienveillante.
        L'histoire doit faire au moins 200 mots. Utilise un langage simple, imagé et immersif.
        Pas d'émojis.
        """
        
        # Appel avec le nouveau client genai
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Utilisation du modèle actuel recommandé
            contents=prompt
        )
        
        return jsonify({"story": response.text})
        
    except Exception as e:
        return jsonify({"story": "Le grimoire est un peu fatigué, réessaie dans un instant !"}), 200

if __name__ == '__main__':
    app.run()
