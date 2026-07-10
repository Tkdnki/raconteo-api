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
    
    # Prompt mis à jour pour un langage simple et structuré
    prompt = f"""
    Écris une histoire pour un enfant de 5 ans sur le thème : {topic}.
    
    Instructions strictes :
    - Langage : Utilise des mots simples et concrets. Phrases courtes et rythmées.
    - Structure : 
        1. Intro : Présente le héros et son désir.
        2. Histoire : Une aventure avec une petite difficulté résolue grâce à l'entraide ou la réflexion.
        3. Conclusion : Une morale bienveillante en une phrase.
    - Contrainte : PAS de mots compliqués. Pas de style trop littéraire. C'est une histoire pour être comprise par un tout-petit.
    - Pas d'émojis dans le texte (pour faciliter la lecture TTS).
    - INTERDICTION : Ne commence JAMAIS l'histoire par "Voici", "Il était une fois" ou "Voici l'histoire de". Commence directement par l'action ou le personnage.
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
