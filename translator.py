import tkinter as tk
from tkinter import ttk
import requests
import re
from langdetect import detect_langs
def clear_output_when_input_empty(event):
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.config(state="disabled")
def copy_translation():
    translation = output_text.get("1.0", tk.END).strip()

    if not translation:
        return

    window.clipboard_clear()
    window.clipboard_append(translation)
    window.update()
def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please enter some text.")
        output_text.config(state="disabled")
        return

    languages = {
        "English": "en",
        "Urdu": "ur",
        "Arabic": "ar",
        "French": "fr",
        "Spanish": "es",
        "Hindi": "hi"
    }

    language_names = {
        "en": "English",
        "ur": "Urdu",
        "ar": "Arabic",
        "fr": "French",
        "es": "Spanish",
        "hi": "Hindi"
    }

    source = languages[source_language.get()]
    target = languages[target_language.get()]

    # Detect the language of the entered text
    try:
        detected = detect_langs(text)

        detected_language = detected[0].lang
        confidence = detected[0].prob

        if detected_language != source and confidence >= 0.75:
            output_text.config(state="normal")
            output_text.delete("1.0", tk.END)
            output_text.insert(
                tk.END,
                f"Warning: You selected {language_names[source]}, "
                f"but the text appears to be "
                f"{language_names.get(detected_language, 'another language')}."
            )
            output_text.config(state="disabled")
            return

    except Exception as error:
        print("Language detection error:", error)

    # Split text into sentences
    sentences = re.split(r'(?<=[.!?۔])\s+', text)

    translated_sentences = []

    for sentence in sentences:
        if not sentence.strip():
            continue

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": sentence,
            "langpair": f"{source}|{target}"
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            data = response.json()

            translation = data["responseData"]["translatedText"]

            translated_sentences.append(translation)

        except Exception as error:
            print("Translation error:", error)
            translated_sentences.append(
                "Translation failed. Check your internet connection."
            )

    translation = " ".join(translated_sentences)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translation)
    output_text.config(state="disabled")
# Create main window
window = tk.Tk()
window.title("Language Translation Tool")
window.geometry("600x500")

# Title
title = tk.Label(
    window,
    text="Language Translation Tool",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

# Source language
source_label = tk.Label(window, text="Source Language:")
source_label.pack()

source_language = ttk.Combobox(
    window,
    values=["English", "Urdu", "Arabic", "French", "Spanish","Hindi"],
    state="readonly"
)
source_language.set("English")
source_language.pack(pady=5)

# Target language
target_label = tk.Label(window, text="Target Language:")
target_label.pack()

target_language = ttk.Combobox(
    window,
    values=["English", "Urdu", "Arabic", "French", "Spanish","Hindi"],
    state="readonly"
)
target_language.set("Urdu")
target_language.pack(pady=5)

# Input text
input_label = tk.Label(window, text="Enter text:")
input_label.pack(pady=(15, 5))
input_frame = tk.Frame(window)
input_frame.pack()

input_text = tk.Text(input_frame, height=6, width=55,wrap="word")
input_text.pack(side=tk.LEFT)

input_scrollbar = tk.Scrollbar(
    input_frame,
    command=input_text.yview
)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

input_text.config(yscrollcommand=input_scrollbar.set)
input_text.bind("<KeyRelease>", clear_output_when_input_empty)
# Translate button
translate_button = tk.Button(
    window,
    text="Translate",
    font=("Arial", 12, "bold"),
    command=translate_text
)
translate_button.pack(pady=15)

# Output text
output_label = tk.Label(window, text="Translation:")
output_label.pack()
output_frame = tk.Frame(window)
output_frame.pack()

output_text = tk.Text(output_frame, height=6, width=55,state="disabled",wrap="word")
output_text.pack(side=tk.LEFT)

output_scrollbar = tk.Scrollbar(
    output_frame,
    command=output_text.yview
)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=output_scrollbar.set)

copy_button = tk.Button(
    window,
    text="Copy Translation",
    font=("Arial", 11, "bold"),
    command=copy_translation
)
copy_button.pack(pady=10)
# Keep window open
window.mainloop()
