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
    
    # Prompt optimisé pour garantir une structure complète et une longueur suffisante
    prompt = f"""
    Écris une histoire complète et structurée pour un enfant de 5 ans sur le thème : {topic}.
    
    La structure doit impérativement contenir :
    1. Une introduction poétique qui présente le personnage et son univers.
    2. Une aventure avec une péripétie intéressante où le héros fait preuve de réflexion ou d'entraide.
    3. Une conclusion avec une morale bienveillante et constructive.
    
    L'histoire doit faire au moins 150 mots. Utilise un langage simple, imagé et immersif.
    Contrainte technique : Pas d'émojis dans le texte pour faciliter la lecture.
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
