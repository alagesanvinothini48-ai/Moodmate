from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# ==============================
# CONVERSATION MEMORY
# ==============================

conversation_memory = {
    "name": None
}


# ==============================
# MOOD DETECTION
# ==============================

def detect_mood(message):
    message = message.lower()

    happy_words = [
        "happy", "great", "good", "awesome",
        "excited", "wonderful", "amazing",
        "glad", "joy"
    ]

    sad_words = [
        "sad", "unhappy", "lonely", "upset",
        "cry", "depressed", "hurt", "down"
    ]

    angry_words = [
        "angry", "mad", "furious",
        "annoyed", "irritated", "hate"
    ]

    stressed_words = [
        "stress", "stressed", "exam",
        "pressure", "tired", "worried",
        "anxious", "nervous"
    ]

    for word in happy_words:
        if word in message:
            return "happy"

    for word in sad_words:
        if word in message:
            return "sad"

    for word in angry_words:
        if word in message:
            return "angry"

    for word in stressed_words:
        if word in message:
            return "stressed"

    return "neutral"


# ==============================
# CHATBOT RESPONSE
# ==============================

def generate_response(message):

    text = message.lower().strip()

    # ==============================
    # NAME MEMORY
    # ==============================

    if "my name is " in text:

        name = text.split("my name is ", 1)[1].strip()

        if name:
            conversation_memory["name"] = name.title()

            return (
                f"Nice to meet you, {conversation_memory['name']}! 😊 "
                "I'll remember your name during this conversation."
            ), "neutral"


    if (
        "what is my name" in text
        or "do you know my name" in text
        or "remember my name" in text
    ):

        if conversation_memory["name"]:

            return (
                f"Your name is {conversation_memory['name']}! 💙 "
                "I remember you!"
            ), "neutral"

        else:

            return (
                "You haven't told me your name yet. 😊"
            ), "neutral"


    # ==============================
    # MOOD
    # ==============================

    mood = detect_mood(text)


    # ==============================
    # GREETING
    # ==============================

    if any(word in text for word in ["hello", "hi", "hey"]):

        responses = [
            "Hey! 👋 I'm MoodMate. How are you feeling today?",
            "Hello! 😊 I'm here to chat with you.",
            "Hi there! 🌟 Tell me what's on your mind."
        ]

        return random.choice(responses), mood


    # ==============================
    # ABOUT CHATBOT
    # ==============================

    if "your name" in text or "who are you" in text:

        return (
            "I'm MoodMate AI 🤖. "
            "I'm a friendly chatbot designed to understand "
            "your mood and have helpful conversations with you."
        ), mood


    # ==============================
    # HOW ARE YOU
    # ==============================

    if "how are you" in text:

        return (
            "I'm doing great! 🤖 Thanks for asking. "
            "More importantly, how are YOU feeling?"
        ), mood


    # ==============================
    # HAPPY
    # ==============================

    if mood == "happy":

        responses = [
            "That's wonderful to hear! 🌟 What made your day better?",
            "Yay! 😊 Keep that positive energy going!",
            "I'm happy that you're feeling good! 💙"
        ]

        return random.choice(responses), mood


    # ==============================
    # SAD
    # ==============================

    if mood == "sad":

        responses = [
            "I'm sorry you're having a difficult moment. 💙 "
            "You don't have to solve everything at once.",

            "It sounds like you're going through a tough time. "
            "I'm here to listen.",

            "You can tell me what happened if you'd like to talk about it."
        ]

        return random.choice(responses), mood


    # ==============================
    # ANGRY
    # ==============================

    if mood == "angry":

        responses = [
            "It sounds like something really frustrated you. "
            "Taking a short pause may help.",

            "I understand that you're feeling angry. "
            "What happened?",

            "Sometimes putting the problem into words "
            "can make it easier to handle."
        ]

        return random.choice(responses), mood


    # ==============================
    # STRESSED
    # ==============================

    if mood == "stressed":

        responses = [
            "It sounds like you're under some pressure. 🧘 "
            "Try taking one small task at a time.",

            "When everything feels overwhelming, "
            "pause for a moment and focus on one simple step.",

            "You don't need to solve everything at once. 🌱"
        ]

        return random.choice(responses), mood


    # ==============================
    # THANKS
    # ==============================

    if "thank you" in text or "thanks" in text:

        return (
            "You're very welcome! 😊 "
            "I'm always happy to chat."
        ), mood


    # ==============================
    # HELP
    # ==============================

    if "help" in text:

        return (
            "Of course! 🤝 You can talk to me about "
            "your day, feelings, goals, stress, "
            "or anything you'd like to discuss."
        ), mood


    # ==============================
    # TIME
    # ==============================

    if "time" in text:

        current_time = datetime.now().strftime("%I:%M %p")

        return (
            f"The current time is {current_time} ⏰"
        ), mood


    # ==============================
    # MOTIVATION
    # ==============================

    if (
        "motivate" in text
        or "motivation" in text
        or "give up" in text
    ):

        responses = [
            "Small progress is still progress. 🌱 "
            "Keep moving one step at a time.",

            "You don't need to be perfect. "
            "Just keep moving forward. 💪",

            "Every small step counts. ✨"
        ]

        return random.choice(responses), mood


    # ==============================
    # DEFAULT RESPONSE
    # ==============================

    responses = [
        "That's interesting. Tell me a little more about it.",

        "I understand. What would you like to do about it?",

        "Thanks for sharing that with me. 😊",

        "I hear you. Tell me more about what's happening.",

        "That sounds important. Tell me more.",

        "Let's think about it together. What happened next?"
    ]

    return random.choice(responses), mood


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template("index.html")


# ==============================
# CHAT API
# ==============================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:

        return jsonify({
            "response": "Please enter a message.",
            "mood": "neutral"
        })


    message = data["message"]

    if not message.strip():

        return jsonify({
            "response": "Please type something first 😊",
            "mood": "neutral"
        })


    response, mood = generate_response(message)


    return jsonify({
        "response": response,
        "mood": mood
    })


# ==============================
# START APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )