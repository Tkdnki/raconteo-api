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
    
    # Prompt optimisé pour la créativité, la longueur et le sens
    prompt = f"""
    Écris une histoire longue et immersive pour un enfant de 5 ans sur le thème : {topic}.
    
    Instructions strictes pour la narration :
    - Commence directement par une action ou une description poétique du lieu.
    - Ne présente jamais le personnage par une phrase basique du type "Nom est un Adjectif Nom". 
    - Exemple de style attendu : "Sous les rayons de la lune, le vent murmurait des secrets à nos oreilles."
    - La narration doit être riche, détaillée et captivante. Développe l'intrigue avec des péripéties intéressantes.
    - Sois créatif, surprenant et immersif. Évite les structures scolaires trop prévisibles.
    - Intègre une morale profonde et bienveillante à la fin, amenée naturellement par l'histoire.
    - Langage : Mots simples et concrets, mais avec un vocabulaire évocateur.
    - Contrainte technique : Pas d'émojis dans le texte.
    - Longueur : L'histoire doit être substantielle et bien développée.
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
