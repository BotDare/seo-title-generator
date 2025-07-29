import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to call OpenAI API
def generate_title_and_description():
    content_type = content_type_var.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not notes:
        messagebox.showwarning("Missing Input", "Please enter some notes.")
        return

    prompt = f"""You are a helpful SEO assistant. Generate an attention-grabbing, Google-search-friendly TITLE and a short, keyword-optimised DESCRIPTION for a {content_type}.

Notes:
{notes}

Format your answer like this:
Title: ...
Description: ...
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        result = response.choices[0].message.content.strip()
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("API Error", str(e))

# GUI Setup
window = tk.Tk()
window.title("SEO Title Generator")
window.geometry("600x600")
window.resizable(False, False)

# Content type selection
content_type_var = tk.StringVar(value="blog")

tk.Label(window, text="Choose content type:", font=("Arial", 12)).pack(pady=5)
tk.Radiobutton(window, text="Blog", variable=content_type_var, value="blog").pack()
tk.Radiobutton(window, text="Article", variable=content_type_var, value="article").pack()

# Notes input
tk.Label(window, text="Enter your notes:", font=("Arial", 12)).pack(pady=(10, 0))
notes_text = scrolledtext.ScrolledText(window, height=10, width=70, wrap=tk.WORD)
notes_text.pack(pady=5)

# Generate button
tk.Button(window, text="Generate", font=("Arial", 12), command=generate_title_and_description).pack(pady=10)

# Output display
tk.Label(window, text="Generated title and description:", font=("Arial", 12)).pack(pady=(15, 0))
output_text = scrolledtext.ScrolledText(window, height=8, width=70, wrap=tk.WORD, state="disabled")
output_text.pack(pady=5)

# Run the GUI
window.mainloop()
