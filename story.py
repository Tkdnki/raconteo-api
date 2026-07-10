from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

# Le client utilise automatiquement la variable d'environnement GEMINI_API_KEY
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        
        # Un prompt ultra-précis pour forcer la longueur
        prompt = f"""
        Raconte une histoire complète, immersive et détaillée pour un enfant de 5 ans sur le thème suivant : {topic}.
        
        Structure obligatoire :
        1. Une introduction poétique posant le décor.
        2. Une aventure avec au moins trois péripéties différentes.
        3. Une conclusion chaleureuse avec une morale constructive.
        
        Contraintes :
        - Fais environ 250 mots minimum.
        - Utilise un langage vivant, imagé et sans émojis.
        - Ne répète pas le sujet mot pour mot, intègre-le naturellement.
        """
        
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
            contents=prompt
        )
        
        return jsonify({"story": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
