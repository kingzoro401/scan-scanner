from flask import Flask, request

app = Flask(__name__)

# -------------------------------
# Scam Detection Logic
# -------------------------------
def detect_scam(text):
    scam_keywords = [
        "win money",
        "free cash",
        "click here",
        "urgent",
        "password",
        "bank",
        "claim now",
        "limited offer"
    ]

    for word in scam_keywords:
        if word in text.lower():
            return True
    return False


# -------------------------------
# HOME PAGE
# -------------------------------
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Scam Scanner</title>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h1>🔥 Scam Scanner</h1>
        <p>Paste a message below to check if it's a scam:</p>

        <form action="/scan" method="post">
            <input type="text" name="message" placeholder="Enter message..." style="width:300px; padding:10px;" required>
            <br><br>
            <button type="submit" style="padding:10px 20px;">Scan</button>
        </form>
    </body>
    </html>
    """


# -------------------------------
# SCAN FUNCTION
# -------------------------------
@app.route("/scan", methods=["POST"])
def scan():
    message = request.form.get("message")

    if detect_scam(message):
        result = "⚠️ This looks like a SCAM!"
        color = "red"
    else:
        result = "✅ This looks SAFE."
        color = "green"

    return f"""
    <html>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2 style="color:{color};">{result}</h2>
        <br>
        <a href="/">🔁 Scan another message</a>
    </body>
    </html>
    """


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)