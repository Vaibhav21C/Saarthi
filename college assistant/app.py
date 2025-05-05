from flask import Flask, render_template, request, jsonify, session
import requests
import secrets

app = Flask(__name__, static_folder='rasa-ui/static', static_url_path='/static')

# Securely generated secret key for session signing
app.secret_key = secrets.token_hex(16)

# Rasa server webhook endpoint
RASA_URL = "http://127.0.0.1:5005/webhooks/rest/webhook"



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form.get("message")

    if not user_message:
        return jsonify({"reply": "No message received."})

    payload = {"sender": "user", "message": user_message}

    try:
        response = requests.post(RASA_URL, json=payload)
        if response.status_code == 200:
            messages = response.json()
            bot_reply = " ".join([msg.get("text", "") for msg in messages])
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": "Bot did not respond properly."})
    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"Error connecting to Rasa: {str(e)}"})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
