from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuration de la clé API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    try:
        # Sécurisation de la récupération des données
        data = request.get_json(silent=True) or {}
        topic = data.get('topic', 'une aventure magique')
        
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = f"""
        Écris une histoire complète et structurée pour un enfant de 5 ans sur le thème : {topic}.
        La structure doit impérativement contenir :
        1. Une introduction poétique.
        2. Une aventure avec une péripétie intéressante.
        3. Une conclusion avec une morale bienveillante.
        L'histoire doit faire au moins 200 mots. Langage simple, imagé et immersif.
        """
        
        response = model.generate_content(prompt)
        return jsonify({"story": response.text})
        
    except Exception as e:
        # En cas d'erreur, on renvoie une réponse JSON propre au lieu de planter
        return jsonify({"story": "Il était une fois une aventure magique qui attendait d'être racontée, mais le grimoire a besoin d'un peu de repos. Réessaie dans un instant !"}), 200

if __name__ == '__main__':
    app.run()
