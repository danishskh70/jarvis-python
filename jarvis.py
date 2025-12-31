import threading
import customtkinter as ctk
import pyttsx3
from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

# ---------------- Voice Function ----------------
engine = pyttsx3.init()
voice_enabled = True

def speak(text):
    if voice_enabled:
        def tts():
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=tts, daemon=True).start()

# ---------------- Context Memory ----------------
context_memory = {"conversation": []}

# ---------------- Gemini SDK Client ----------------
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- Fetch AI Response ----------------
def fetch_and_summarize(query):
    update_gui(f"User: {query}\nJarvis: Thinking...\n")
    context_memory["conversation"].append({"role": "user", "content": query})

    try:
        # Combine conversation
        contents = "\n".join([msg["content"] for msg in context_memory["conversation"]])
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        answer = response.text.strip()
        if not answer:
            answer = "Jarvis: Sorry, I could not generate a response."

        context_memory["conversation"].append({"role": "assistant", "content": answer})
        update_gui(f"Jarvis: {answer}")
        speak(answer)

    except Exception as e:
        msg = f"Jarvis: An error occurred: {e}"
        update_gui(msg)
        speak(msg)

# ---------------- GUI ----------------
def update_gui(text):
    output_text.configure(state='normal')
    output_text.insert(ctk.END, text + "\n\n")
    output_text.see(ctk.END)
    output_text.configure(state='disabled')

def on_submit():
    query = entry.get()
    if not query.strip():
        return
    entry.delete(0, ctk.END)
    threading.Thread(target=fetch_and_summarize, args=(query,)).start()

def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    btn_voice.configure(text="🔊" if voice_enabled else "🔇")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("AI Gemini Jarvis")
root.geometry("900x650")

output_text = ctk.CTkTextbox(root, height=35, width=105)
output_text.pack(padx=10, pady=(10,0), fill='both', expand=True)
output_text.configure(state='disabled')

input_frame = ctk.CTkFrame(root, height=80)
input_frame.pack(side='bottom', fill='x', padx=10, pady=10)

entry = ctk.CTkEntry(input_frame, placeholder_text="Ask Jarvis anything...", width=650, height=45, corner_radius=20)
entry.pack(side='left', padx=(10,5), pady=10)

submit_btn = ctk.CTkButton(input_frame, text="Ask", width=80, height=45, corner_radius=20, command=on_submit)
submit_btn.pack(side='left', padx=5, pady=10)

btn_voice = ctk.CTkButton(input_frame, text="🔊", width=60, height=45, corner_radius=20, command=toggle_voice)
btn_voice.pack(side='left', padx=5, pady=10)

root.mainloop()
