from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuration de la clé API via la variable d'environnement sur Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def generate_story():
    # Récupération des données envoyées par l'application
    topic_raw = data.get('topic', 'une aventure magique')
    
    # Configuration du modèle
    model = genai.GenerativeModel(model_name='models/gemini-3.5-flash')
    
    # Prompt optimisé : extraction du personnage et consignes narratives
    prompt = f"""
    Tu es un auteur de contes pour enfants. Écris une histoire longue, riche et immersive pour un enfant de 5 ans.
    
    Sujet brut : {topic_raw}
    
    Instructions pour la gestion du personnage :
    - N'utilise pas toute la phrase utilisateur comme nom ou description. 
    - Identifie le personnage principal et son trait de caractère clé.
    - Exemple : Si le sujet est "Un chat qui s'appelle Ninimo et qui adore manger des groseilles", appelle-le "Ninimo, le petit chat gourmand" et utilise ce nom dans l'histoire.
    
    Instructions pour la narration :
    - Commence directement par une action ou une description poétique du lieu.
    - Ne présente jamais le personnage par une phrase basique du type "Nom est un Adjectif Nom".
    - Exemple de style : "Sous les rayons de la lune, le vent murmurait des secrets à nos oreilles."
    - La narration doit être détaillée. Développe l'intrigue avec des péripéties réelles.
    - Sois créatif, surprenant et immersif. Évite les structures scolaires trop prévisibles.
    - Intègre une morale profonde et bienveillante à la fin, amenée naturellement par l'histoire.
    - Langage : Mots simples, concrets, mais avec un vocabulaire évocateur.
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
