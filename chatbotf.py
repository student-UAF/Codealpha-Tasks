from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
faqs = [
    {
        "questions": [
            "What are your opening hours?",
            "When do you open?",
            "When do you close?",
            "What time are you open?",
            "What are you working hours?"
            ],
        
        "answer": "We are open from 9 AM to 5 PM, Monday to Friday."
    },

    {
        "questions": [
            "Where are you located?",
            "What is you location?",
            "Where is you office?",
            "Where can I find you?",
            "What is your address?"
        ],
        "answer": "We are located in Faisalabad."
    },

    {
        "questions": [
            "How can I contact you?",
            "How do I contact you?",
            "How can I reach you?",
            "What is your contact information?"
        ],
        "answer": "You can contact us by email or phone."
    },

    {
        "questions": [
            "What services do you provide?",
            "What services do you offer?",
            "What do you provide?",
            "What can you help me with?"
        ],
        "answer": "We provide AI and software development services."
    },

    {
        "questions": [
            "Do you provide online services?",
            "Are you services available online?",
            "Can I use you services online?"
        ],
        "answer": "Yes, we provide several services online."
    },

    {
        "questions": [
            "How can I place an order?",
            "How do I place an order?",
            "Where can I place an order?",
            "How can I order?"
        ],
        "answer": "You can place an order by contacting our support team."
    }
]
def find_answer(user_question):

    all_questions = []
    question_to_faq = []

    # Collect all alternative questions
    for faq in faqs:
        for question in faq["questions"]:
            all_questions.append(question)
            question_to_faq.append(faq)

    # Convert questions into numerical vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        stop_words="english"
    )

    faq_vectors = vectorizer.fit_transform(all_questions)
    user_vector = vectorizer.transform([user_question])

    # Calculate similarity
    similarities = cosine_similarity(user_vector, faq_vectors)

    # Find best match
    best_match_index = similarities.argmax()
    best_score = similarities[0][best_match_index]

    print("Similarity score:", best_score)

    # Minimum similarity requirement
    if best_score >= 0.25:
        return question_to_faq[best_match_index]["answer"]
    else:
        return "Sorry, I don't know the answer to that question."
    # ---------------- GUI ----------------
import customtkinter as ctk

# Appearance settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def add_to_chat(message):
    chat_box.configure(state="normal")
    chat_box.insert("end", message)
    chat_box.configure(state="disabled")
    chat_box.see("end")


def send_message():
    user_question = input_box.get().strip()

    if not user_question:
        return

    add_to_chat("You: " + user_question + "\n")

    answer = find_answer(user_question)

    add_to_chat("Chatbot: " + answer + "\n\n")

    input_box.delete(0, "end")


# Create window
window = ctk.CTk()
window.title("FAQ Chatbot")
window.geometry("700x600")


# Title
title = ctk.CTkLabel(
    window,
    text="\U0001F916 FAQ Chatbot",
    font=("Arial", 24, "bold")
)
title.pack(pady=(20, 10))


# Subtitle
subtitle = ctk.CTkLabel(
    window,
    text="Ask me anything about our services",
    font=("Arial", 13)
)
subtitle.pack(pady=(0, 15))


# Chat box
chat_box = ctk.CTkTextbox(
    window,
    width=620,
    height=400,
    font=("Arial", 14),
    corner_radius=15
)
chat_box.pack(padx=30, pady=10, fill="both", expand=True)

# Make chat box read-only
chat_box.configure(state="disabled")


# Input frame
input_frame = ctk.CTkFrame(
    window,
    fg_color="transparent"
)
input_frame.pack(fill="x", padx=30, pady=(5, 20))


# Input box
input_box = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your question here...",
    height=45,
    font=("Arial", 14),
    corner_radius=12
)
input_box.pack(side="left", fill="x", expand=True, padx=(0, 10))


# Send button
send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    width=100,
    height=45,
    font=("Arial", 14, "bold"),
    corner_radius=12,
    command=send_message
)
send_button.pack(side="right")


# Press Enter to send
input_box.bind("<Return>", lambda event: send_message())


# Start application
window.mainloop()
