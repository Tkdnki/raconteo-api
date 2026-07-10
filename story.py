from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/story', methods=['POST'])
def debug_models():
    # Cette ligne liste tous les modèles disponibles pour votre clé
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    return jsonify({"available_models": models})

if __name__ == '__main__':
    app.run()
