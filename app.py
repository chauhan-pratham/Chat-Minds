from flask import Flask, render_template, request, jsonify
import json
import random
import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --- CONFIGURATION ---
INTENTS_FILE = "data/intents.json"
KNOWLEDGE_BASE_FILE = "data/questions.json"


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


# --- AI MODEL SETUP (TF-IDF Lightweight) ---
print("Initializing TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer()
print("Vectorizer Ready.")


# --- PRE-COMPUTE EMBEDDINGS ---
# We encode all questions once at startup to make the chat instant
kb_questions = []
kb_answers = []
kb_embeddings = None

if knowledge_base_data:
    for qa in knowledge_base_data.get("questions", []):
        kb_questions.append(qa.get("question"))
        kb_answers.append(qa.get("answer"))

    if kb_questions:
        print(f"Fitting TF-IDF on {len(kb_questions)} Knowledge Base questions...")
        kb_embeddings = vectorizer.fit_transform(kb_questions)
        print("Knowledge Base Vectorized and Ready.")


# --- INTENT HANDLING (REGEX) ---
def handle_intent(intent_tag: str) -> str:
    if not intents_data:
        return "Error: Intents file not loaded."
    for intent in intents_data.get("intents", []):
        if intent.get("tag") == intent_tag:
            return random.choice(intent.get("responses", ["No response found."]))
    return "Intent tag not found."


# --- SEMANTIC SEARCH LOGIC ---
def semantic_search(user_input, threshold=0.15):
    """
    Convert query to vector and find best match in Knowledge Base using TF-IDF.
    Threshold: Lower than embeddings because TF-IDF is sparse.
    """
    if kb_embeddings is None or len(kb_questions) == 0:
        return None

    # Transform the user's query
    query_vec = vectorizer.transform([user_input])

    # Calculate Cosine Similarity
    # This returns an array [[similarity_1, similarity_2, ...]]
    similarities = cosine_similarity(query_vec, kb_embeddings).flatten()

    # Find the best match
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
        
    print(f"\n[AI DEBUG] Query: '{user_input}'")
    print(f"[AI DEBUG] Match: '{kb_questions[best_idx]}'")
    print(f"[AI DEBUG] Score: {best_score:.4f}")

    if best_score >= threshold:
        return kb_answers[best_idx]
    else:
        print("[AI DEBUG] Score below threshold -> Ignoring match.")

    return None


# --- MAIN CLASSIFICATION LOGIC ---
def classify_and_respond(user_input: str) -> str:
    print(f"\n--- New Request: '{user_input}' ---")

    # 1. CHECK INTENTS (Regular Expressions)
    # Good for simple greetings, goodbyes, or specific commands
    matched_intent = None
    if intents_data:
        for intent in intents_data.get("intents", []):
            for pattern in intent.get("patterns", []):
                # Word boundaries \b ensure we don't match partial words
                if re.search(r"\b" + re.escape(pattern.lower()) + r"\b", user_input.lower()):
                    matched_intent = intent
                    break
            if matched_intent:
                break
    
    # If it's a greeting or a simple name mention but the sentence is long, 
    # it's likely a real question (e.g., "Hi, what is python?" or "Tech stack of Pratham")
    # So we skip these generic intents and let the AI handle it.
    
    ignore_match = False
    if matched_intent:
        word_count = len(user_input.split())
        if matched_intent["tag"] == "greeting" and word_count > 4:
            ignore_match = True
        elif matched_intent["tag"] == "self_name" and word_count > 3:
            ignore_match = True

    if ignore_match:
        print(f"[INFO] Complex input detected for '{matched_intent['tag']}'. Checking Knowledge Base instead.")
        matched_intent = None

    if matched_intent:
        print(f"[INFO] Matched intent '{matched_intent['tag']}' via Regex.")
        return handle_intent(matched_intent["tag"])


    # 2. SEMANTIC SEARCH (AI)
    # If no simple intent matched, use the brain
    print("[INFO] searching Knowledge Base via Semantic Search...")
    ai_answer = semantic_search(user_input)
    if ai_answer:
        return ai_answer


    # 3. FALLBACK
    print("[INFO] No match found. Returning 'unknown' intent.")
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
    
    # Run Flask
    app.run(debug=True)
