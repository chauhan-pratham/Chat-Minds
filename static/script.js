const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const suggestionBox = document.querySelector(".suggestion-box"); // Select suggestion box

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;

// --- SUGGESTION DATA ---
const suggestionsMap = {
    // --- SKILLS & TECH ---
    "skill": ["What are Pratham's technical skills?", "What is his tech stack?"],
    "tech": ["What is his tech stack?", "Does he know Python?"],
    "code": ["What programming languages does he know?", "Does he know C++?"],
    "lang": ["What programming languages does he know?", "Does he know Python?"],
    "python": ["Does he know Python?", "What projects use Python?"],
    "cpp": ["Does he know C++?", "What is his tech stack?"],
    "sql": ["Does he know SQL?", "What is his tech stack?"],
    "dbms": ["Does he know Database Management?", "What is his tech stack?"],
    "data": ["Does he know Database Management?", "What is his tech stack?"],
    "flas": ["Does he know Flask?", "Tell me about ChatMinds."],
    "nlp": ["What NLP projects has he done?", "Tell me about the Spam Classifier."],
    "nat": ["What NLP projects has he done?", "Tell me about the Spam Classifier."],
    "scikit": ["Does he know Scikit-learn?", "Tell me about the Spam Classifier."],
    "nltk": ["Does he know NLTK?", "Tell me about the Spam Classifier."],
    "ml": ["What ML models has he used?", "Tell me about the Spam Classifier."],
    "machine": ["What ML models has he used?", "Tell me about the Spam Classifier."],
    "learn": ["What ML models has he used?", "What programming languages does he know?"],
    "hack": ["Does he know ethical hacking?", "What was the MITM attack project?"],
    "linux": ["Does he know Linux?", "What is his tech stack?"],
    "os": ["Does he know Operating Systems?", "What is his tech stack?"],
    "oper": ["Does he know Operating Systems?", "What is his tech stack?"],
    "syst": ["Does he know Operating Systems?", "What is his tech stack?"],
    "net": ["Does he know Computer Networks?", "What is his tech stack?"],
    "comp": ["Does he know Computer Networks?", "What is his tech stack?"],
    "cyber": ["Does he know cybersecurity?", "Tell me about his time at Acmegrade."],
    "secu": ["What were his responsibilities at Acmegrade?", "Does he know cybersecurity?"],

    // --- PROJECTS ---
    "proj": ["What projects has Pratham built?", "Tell me about ChatMinds."],
    "spam": ["How does the SMS Spam Classifier work?", "What accuracy did the spam model achieve?"],
    "classi": ["How does the SMS Spam Classifier work?", "Tell me about his NLP project."],
    "chat": ["Tell me more about ChatMinds.", "How was this chatbot built?"],
    "bot": ["Tell me more about ChatMinds.", "Who created you?"],

    // --- INTERNSHIPS ---
    "work": ["Describe Pratham's internship experience.", "What did he do at TIET?"],
    "exp": ["Describe Pratham's internship experience.", "What did he do at Acmegrade?"],
    "intern": ["Describe Pratham's internship experience.", "Tell me about the Solana project."],
    "solan": ["What did he do with Solana?", "What is the Secure Logging prototype?"],
    "block": ["Could you elaborate on Pratham's blockchain internship?", "What is Merkle tree batching?"],
    "merk": ["What is Merkle tree batching?", "Tell me about the Solana project."],
    "acme": ["What did he do at Acmegrade?", "What was the MITM attack project?"],
    "mitm": ["What was the MITM attack project?", "Did he succeed in HSTS hijacking?"],

    // --- EDUCATION ---
    "edu": ["Where does Pratham study?", "What is his CGPA?"],
    "study": ["Where does Pratham study?", "What degree is he pursuing?"],
    "coll": ["Where does Pratham study?", "What degree is he pursuing?"],
    "univ": ["Where does Pratham study?", "What is his CGPA?"],
    "deg": ["What degree is he pursuing?", "Where does he study?"],
    "btech": ["What degree is he pursuing?", "Where does he study?"],
    "be": ["What degree is he pursuing?", "Where does he study?"],
    "bach": ["What degree is he pursuing?", "Where does he study?"],
    "engin": ["What degree is he pursuing?", "What is his tech stack?"],
    "sci": ["What does he study?", "What is his tech stack?"],
    "comp": ["What does he study?", "What is his tech stack?"],
    "thapar": ["What does he study at Thapar Institute?", "What is his CGPA?"],
    "tiet": ["What does he study at TIET?", "What is his CGPA?"],
    "cgpa": ["What is his CGPA?", "Tell me about his academic improvement."],
    "gpa": ["What is his CGPA?", "Tell me about his academic improvement."],
    "grade": ["What is his CGPA?", "Tell me about his academic improvement."],

    // --- ACHIEVEMENTS & CERTIFICATIONS ---
    "achiev": ["What are Pratham's biggest achievements?", "Tell me about his academic improvement."],
    "cert": ["What certifications has Pratham earned?", "Does he have AWS certifications?"],
    "aws": ["What certifications has Pratham earned?", "Tell me about his AWS Academy certs."],
    "kara": ["Is he good at sports?", "Tell me about his Karate medal."],
    "sport": ["Is he good at sports?", "Tell me about his Karate medal."],
    "play": ["What extra-curriculars does he do?", "Tell me about his theater experience."],
    "lead": ["Can you describe any leadership experiences?", "Tell me about the Alumni Meet."],

    // --- LINKS & SOCIAL ---
    "git": ["What is his GitHub profile?", "What projects has he built?"],
    "link": ["What is his LinkedIn profile?", "How can I contact him?"],
    "resum": ["Where can I see his Resume?", "What is his tech stack?"],
    "cv": ["Where can I see his CV?", "What is his educational background?"],
    "port": ["Where can I see his Portfolio?", "What projects has he built?"],
    "prof": ["What are his professional profiles?", "Where can I see his work?"],

    // --- HIRING ---
    "hire": ["Is Pratham available for work?", "When can he start?"],
    "job": ["Is Pratham available for work?", "What roles is he looking for?"],
    "avail": ["Is Pratham available for internships?", "When can he start?"],
    "role": ["What roles is he looking for?", "Is he interested in backend dev?"],

    // --- GENERIC ---
    "pratham": ["Who is Pratham Chauhan?", "Tell me about yourself.", "What is his tech stack?"],
    "chauhan": ["Who is Pratham Chauhan?", "How can I contact him?"],
    "name": ["Who is Pratham Chauhan?", "Tell me about yourself."],
    "cont": ["How can I contact Pratham?", "What is his email?"],
    "mail": ["What is his email?", "How can I contact Pratham?"],
    "phone": ["What is his phone number?", "How can I contact Pratham?"],
    "who": ["Who is Pratham Chauhan?", "Tell me about yourself."]
};

// --- RENDER SUGGESTIONS ---
const showSuggestions = (text) => {
    suggestionBox.innerHTML = ""; // Clear existing
    if (!text) return;

    const lowerText = text.toLowerCase();
    let foundSuggestions = [];

    // Find matches (Smart Autocomplete)
    for (const [key, questions] of Object.entries(suggestionsMap)) {
        // Match if:
        // 1. Key starts with Input (User types "li" -> Match "link")
        // 2. Input contains Key (User types "linkedin" -> Match "link")
        if (key.startsWith(lowerText) || lowerText.includes(key)) {
            foundSuggestions.push(...questions);
        }
    }

    // Remove duplicates and limit to 3
    foundSuggestions = [...new Set(foundSuggestions)].slice(0, 3);

    // Create Chips
    foundSuggestions.forEach(question => {
        const chip = document.createElement("div");
        chip.classList.add("suggestion-item");
        chip.textContent = question;

        // Click to ask
        chip.addEventListener("click", () => {
            chatInput.value = question;
            handleChat(); // Auto-send
            suggestionBox.innerHTML = ""; // Clear suggestions after sending
        });

        suggestionBox.appendChild(chip);
    });
};

// The conflicting linkify() function has been PERMANENTLY removed.

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;

    // Use textContent for user messages for security
    if (className === "outgoing") {
        chatLi.querySelector("p").textContent = message;
    }

    return chatLi;
}

const generateResponse = (chatElement) => {
    const API_URL = "/get";
    const messageElement = chatElement.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `msg=${encodeURIComponent(userMessage)}`
    };

    fetch(API_URL, requestOptions)
        .then(response => response.json())
        .then(data => {
            // ==================================================================
            // FINAL LOGIC: The backend now sends perfect HTML every time.
            // The frontend's only job is to render it using .innerHTML.
            // ==================================================================
            messageElement.innerHTML = data.reply;
        })
        .catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again.";
        })
        .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

// --- Event Listeners ---
chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
    showSuggestions(chatInput.value); // <--- Trigger Suggestions
});
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});
sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));