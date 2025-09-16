from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

app = Flask(__name__)

# Set OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rule-based logic
def rule_based_response(user_input):
    responses = {
        "halo": "Halo juga! Ada yang bisa dibantu?",
        "siapa kamu": "Saya adalah chatbot sederhana buatanmu.",
        "terima kasih": "Sama-sama! 😊"
    }
    # Cari kata kunci sederhana
    for keyword in responses:
        if keyword in user_input.lower():
            return responses[keyword]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    # Rule-based first
    response = rule_based_response(user_input)
    if response:
        return jsonify({"reply": response})

    # Fallback to OpenAI API
    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        ai_reply = result.choices[0].message.content.strip()
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
