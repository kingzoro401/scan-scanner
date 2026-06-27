from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -------------------------------
# AI SCAM DETECTION
# -------------------------------
def detect_scam_ai(text):
    prompt = f"""
    Analyze this message and determine if it is a scam.

    Message: "{text}"

    Respond ONLY with:
    - SAFE
    - SUSPICIOUS
    - SCAM
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content.strip()

    if "SCAM" in result:
        return "🚨 SCAM DETECTED", "red"
    elif "SUSPICIOUS" in result:
        return "⚠️ SUSPICIOUS", "orange"
    else:
        return "✅ SAFE", "green"


# -------------------------------
# HOME
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
# SCAN
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
        <a href="/">Try again</a>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)