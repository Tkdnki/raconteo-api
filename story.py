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
    
    # Configuration du modèle (vérifié dans la liste de votre compte)
    model = genai.GenerativeModel(model_name='models/gemini-3.5-flash')
    
    # Prompt optimisé pour les enfants
    prompt = f"""
    Écris une histoire courte et bienveillante pour enfants en 3 ou 4 paragraphes sur le thème suivant : {topic}.
    Utilise un ton joyeux, ajoute quelques émojis et assure-toi que l'histoire soit captivante.
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
