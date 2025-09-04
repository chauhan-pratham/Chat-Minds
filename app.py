from flask import Flask, render_template, request, jsonify
import json
import random
import os
import re

# --- NLTK ---
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# --- CONFIGURATION ---
INTENTS_FILE = "data/intents.json"
KNOWLEDGE_BASE_FILE = "data/questions.json"

lemmatizer = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words("english"))


# --- FILE LOADING ---
def load_json_file(file_path):
    if not os.path.exists(file_path):
        print(f"--- FATAL ERROR: The file '{file_path}' was not found. ---")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"--- Successfully loaded '{file_path}'. ---")
            return data
    except json.JSONDecodeError as e:
        print(f"--- FATAL ERROR: Syntax error in '{file_path}'. Details: {e} ---")
        return None


intents_data = load_json_file(INTENTS_FILE)
knowledge_base_data = load_json_file(KNOWLEDGE_BASE_FILE)


# --- PREPROCESSING ---
def preprocess(text: str):
    """Tokenize, lowercase, remove stopwords, and lemmatize."""
    tokens = word_tokenize(text.lower())
    filtered = [
        lemmatizer.lemmatize(tok)
        for tok in tokens
        if tok.isalnum() and tok not in STOP_WORDS
    ]
    return set(filtered)


def expand_with_wordnet(word):
    """Expand a word with its synonyms and lemma forms from WordNet."""
    synonyms = set([word])
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            # normalize each synonym by lemmatizing
            normalized = lemmatizer.lemmatize(lemma.name().lower())
            synonyms.add(normalized)
    return synonyms



# --- INTENT HANDLING ---
def handle_intent(intent_tag: str) -> str:
    if not intents_data:
        return "Error: Intents file not loaded."
    for intent in intents_data.get("intents", []):
        if intent.get("tag") == intent_tag:
            return random.choice(intent.get("responses", ["No response found."]))
    return "Intent tag not found."


# --- KNOWLEDGE BASE MATCHING ---
def search_kb(user_input, kb_data):
    """Search knowledge base for the best matching Q&A."""
    user_tokens = preprocess(user_input)

    # Expand user tokens with WordNet
    expanded_user_tokens = set()
    for token in user_tokens:
        expanded_user_tokens |= expand_with_wordnet(token)

    best_match = None
    best_score = 0

    print(f"\n[DEBUG] Searching KB for words: {expanded_user_tokens}")

    for qa in kb_data.get("questions", []):
        kb_question = qa.get("question", "")
        kb_tokens = preprocess(kb_question)

        score = len(expanded_user_tokens & kb_tokens)

        print(f"[DEBUG] Comparing with: '{kb_question[:50]}...' | Score: {score}")

        if score > best_score:
            best_score = score
            best_match = qa

    print(f"[DEBUG] Highest KB score: {best_score}")
    return best_match if best_score > 0 else None


# --- MAIN CLASSIFICATION LOGIC ---
def classify_and_respond(user_input: str) -> str:
    print(f"\n--- New Request: '{user_input}' ---")

    matched_intent = None

    # 1. Check for a matching intent
    if intents_data:
        for intent in intents_data.get("intents", []):
            for pattern in intent.get("patterns", []):
                if re.search(r"\b" + re.escape(pattern.lower()) + r"\b", user_input.lower()):
                    matched_intent = intent
                    break
            if matched_intent:
                break

    # 2. Greeting check
    if matched_intent and matched_intent["tag"] == "greeting" and len(user_input.split()) > 3:
        print("[INFO] Greeting intent matched but input is long → ignoring intent.")
    elif matched_intent:
        print(f"[INFO] Matched intent '{matched_intent['tag']}' with pattern. Responding.")
        return handle_intent(matched_intent["tag"])

    # 3. Search KB
    print("[INFO] No decisive intent, searching KB...")
    kb_match = search_kb(user_input, knowledge_base_data)
    if kb_match:
        return kb_match.get("answer", "I found something relevant, but no answer text provided.")

    # 4. Fallback
    print("[INFO] No match → fallback to 'unknown' intent.")
    return handle_intent("unknown")


# --- FLASK ROUTES ---
@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    if not msg.strip():
        return jsonify({"reply": "Please say something."})
    return jsonify({"reply": classify_and_respond(msg)})


if __name__ == "__main__":
    if not intents_data or not knowledge_base_data:
        print("\n--- APPLICATION WILL NOT RUN CORRECTLY DUE TO FILE LOADING ERRORS. ---")
    app.run(debug=True)
