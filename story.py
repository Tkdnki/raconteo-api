from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuration de la clé API via la variable d'environnement sur Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    # Récupération des données envoyées par l'application
    data = request.json
    topic = data.get('topic', 'une aventure magique')
    
    # Configuration du modèle
    model = genai.GenerativeModel(model_name='models/gemini-3.5-flash')
    
    # Nouveau prompt optimisé pour des histoires plus travaillées
    prompt = f"""
    Écris une histoire courte pour enfants sur le thème : {topic}.
    
    Instructions de style :
    - Structure l'histoire en exactement 4 paragraphes bien distincts.
    - Utilise un vocabulaire riche, des descriptions sensorielles (couleurs, odeurs, sons) et une narration immersive.
    - Ton : Doux, bienveillant et inspirant.
    - Évite les expressions clichés ou trop enfantines.
    - Termine l'histoire par une réflexion poétique sur la morale ou la beauté de cette aventure.
    - Ajoute quelques émojis pertinents pour agrémenter le texte.
    """
    
    try:
        # Appel à l'API Gemini
        response = model.generate_content(prompt)
        # Retourne le résultat au format JSON
        return jsonify({"story": response.text})
    except Exception as e:
        # En cas d'erreur, on retourne le message pour le débogage
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
