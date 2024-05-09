from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)


# Load the knowledge base and intents from JSON files
try:
    with open("data/knowledge_base.json", "r") as file:
        knowledge_base = json.load(file)
    with open("data/intents.json", "r") as file:
        intents = json.load(file)
except json.JSONDecodeError as e:
    print(f"Error loading JSON files: {e}")

# Function to handle intent-based responses
def handle_intent(intent_tag: str) -> str:
    """Handle intent-based responses"""
    for intent in intents["intents"]:
        if intent["tag"] == intent_tag:
            return random.choice(intent["responses"])
    return "Sorry I didn't understood."

# Function to find answer based on user input
def find_answer(user_input: str) -> str:
    """Find answer based on user input"""
    for item in knowledge_base["questions"]:
        if user_input.lower() in item["question"].lower():
            return item["answer"]
    return "Sorry I didn't understood."


# Function to classify user input and generate bot response
def classify_and_respond(user_input: str) -> str:
    """Classify user input and generate bot response"""
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input.lower():
                return handle_intent(intent["tag"])
    return find_answer(user_input)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    return jsonify({"reply": classify_and_respond(msg)})

if __name__ == '__main__':
    app.run(debug=True)