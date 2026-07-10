from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurez votre clé API via une variable d'environnement sur Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    data = request.json
    topic = data.get('topic', 'une aventure magique')
    
    # Configuration du modèle
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt optimisé pour les enfants
    prompt = f"""
    Écris une histoire courte et bienveillante pour enfants en 3 ou 4 paragraphes sur le thème suivant : {topic}.
    Utilise un ton joyeux, ajoute quelques émojis et assure-toi que l'histoire soit captivante.
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"story": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()