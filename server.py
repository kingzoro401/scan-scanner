from flask import Flask, request
import openai
import os

app = Flask(__name__)

# -------------------------------
# SET API KEY
# -------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
# AI SCAM DETECTION FUNCTION
# -------------------------------
def detect_scam_ai(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a scam detection AI."},
                {"role": "user", "content": f"Is this a scam? Answer SAFE, SUSPICIOUS, or SCAM only:\n{text}"}
            ]
        )

        result = response["choices"][0]["message"]["content"].strip()

        if "SCAM" in result:
            return "🚨 SCAM DETECTED", "red"
        elif "SUSPICIOUS" in result:
            return "⚠️ SUSPICIOUS", "orange"
        else:
            return "✅ SAFE", "green"

    except Exception as e:
        return f"Error: {str(e)}", "white"


# -------------------------------
# HOME PAGE
# -------------------------------
@app.route("/")
def home():
    return """
    <html>
    <body style="font-family: Arial; text-align:center; background:#0f172a; color:white; margin-top:50px;">
        <h1>🤖 AI Scam Scanner</h1>
        <form action="/scan" method="post">
            <input name="message" style="width:60%; padding:10px;" placeholder="Paste message..." required>
            <br><br>
            <button type="submit">Scan</button>
        </form>
    </body>
    </html>
    """


# -------------------------------
# SCAN ROUTE
# -------------------------------
@app.route("/scan", methods=["POST"])
def scan():
    message = request.form.get("message")

    result, color = detect_scam_ai(message)

    return f"""
    <html>
    <body style="text-align:center; background:#020617; color:white; margin-top:50px;">
        <h2 style="color:{color};">{result}</h2>
        <p>{message}</p>
        <br>
        <a href="/" style="color:lightblue;">Try again</a>
    </body>
    </html>
    """


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)