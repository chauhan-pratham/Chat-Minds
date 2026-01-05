# ChatMinds 🧠💬

**ChatMinds** is an intelligent portfolio chatbot designed to showcase professional skills, projects, and experiences interactively. **Now improved with AI-powered Semantic Search**, it understands the *meaning* of user queries rather than just matching keywords, ensuring highly reliable and context-aware responses.

## 🚀 Features

*   **✨ Semantic Search (New):** Uses **Vector Embeddings** (`sentence-transformers`) to match user questions with the Knowledge Base by meaning, not just exact words.
*   **Intent Recognition:** accurately identifies user intent (e.g., greetings, goodbyes) using regex patterns for instant responses.
*   **Smart Fallback:** If the AI is unsure (low confidence score), it gracefully admits it doesn't know rather than guessing.
*   **Robust & Secure:** Handles edge cases like gibberish, mixed case, and punctuation. Includes basic security sanitization.
*   **Efficiency:** Uses the lightweight `all-MiniLM-L6-v2` model, optimized for fast CPU performance.

## 🛠️ Tech Stack

*   **Backend:** Python 3, Flask
*   **AI/NLP:** Sentence-Transformers (Hugging Face), NumPy
*   **Frontend:** HTML5, CSS3, JavaScript (Chat Interface)
*   **Data:** JSON (`intents.json`, `questions.json`)
*   **Deployment:** Configured for Vercel

## 📂 Project Structure

```bash
Chat-Minds/
├── app.py                # Main Flask application and AI Logic
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
├── testing.md            # Detailed testing and validation report (Legacy NLTK tests)
├── data/
│   ├── intents.json      # Definitions for broad intent matching
│   └── questions.json    # Knowledge base for specific Q&A
├── static/               # CSS and JS files for the frontend
├── templates/            # HTML templates (chat.html)
```

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd Chat-Minds
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you run the app, it will download the AI model (~80MB). This is normal.*

## 🏃 Usage

1.  **Start the Flask Server**
    ```bash
    python app.py
    ```

2.  **Access the Chatbot**
    Open your web browser and navigate to:
    `http://127.0.0.1:5000/`

## 🧪 Testing

The logic has been upgraded to use **Cosine Similarity**.
*   **High Reliability:** "Coding", "Programming", and "Dev" are now treated as related concepts.
*   **Thresholding:** The bot filters out low-confidence matches to avoid hallucinations.

## ☁️ Deployment

This project includes a `vercel.json` configuration file.
**Important:** When deploying to serverless platforms (like Vercel), ensure the instance has enough memory to load the `sentence-transformers` model, or consider pre-downloading the model.

---
*Generated for ChatMinds Project*