# download_nltk.py
import nltk

# List of resources needed for your chatbot
RESOURCES = [
    "punkt",        # tokenizer
    "punkt_tab",    # required for Python 3.12+
    "stopwords",    # stop words list
    "wordnet"       # WordNet for synonyms/lemmatizer
]

def check_and_download():
    print("\n--- Checking NLTK Resources ---\n")
    for resource in RESOURCES:
        try:
            nltk.data.find(f"corpora/{resource}")  # most are corpora
            print(f"[OK] {resource} already installed.")
        except LookupError:
            try:
                print(f"[...] {resource} not found → downloading...")
                nltk.download(resource)
                print(f"[DONE] {resource} installed.")
            except Exception as e:
                print(f"[ERROR] Failed to download {resource}: {e}")
    print("\n--- Resource check complete ---\n")

if __name__ == "__main__":
    check_and_download()
