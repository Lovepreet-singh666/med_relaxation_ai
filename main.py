import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
import pyttsx3
from datetime import datetime
from transformers import pipeline

# Initialize text-to-speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Medication schedule
medications = {
    "Aspirin": {"time": "08:00", "dose": "1 tablet", "purpose": "Pain relief"},
    "Vitamin D": {"time": "12:00", "dose": "1000 IU", "purpose": "Bone health"},
    "Melatonin": {"time": "21:00", "dose": "3 mg", "purpose": "Sleep aid"}
}

# Relaxation techniques
relaxation_guides = {
    "Deep Breathing": "Inhale deeply through your nose for 4 seconds, hold for 4 seconds, exhale slowly through your mouth for 6 seconds. Repeat 5 times.",
    "Progressive Relaxation": "Tense each muscle group for 5 seconds then relax, starting from your toes up to your head.",
    "Mindfulness": "Focus on your breath for 5 minutes. Notice the air moving in and out, let thoughts pass without judgment."
}

# Simple AI-based mood interpreter using Hugging Face transformers
classifier = pipeline("sentiment-analysis")

def ai_recommend_relaxation(user_input):
    sentiment = classifier(user_input)[0]
    label = sentiment['label']
    
    if label == "NEGATIVE":
        return "Deep Breathing"
    elif label == "POSITIVE":
        return "Mindfulness"
    else:
        return "Progressive Relaxation"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Medication & Relaxation Guide")
        self.label = tk.Label(root, text="Welcome to your guide!", font=("Helvetica", 14))
        self.label.pack(pady=20)
        
        tk.Button(root, text="Check Medication Schedule", command=self.schedule).pack(pady=5)
        tk.Button(root, text="Get Relaxation Technique", command=self.relax).pack(pady=5)
        tk.Button(root, text="Exit", command=self.root.quit).pack(pady=5)

        threading.Thread(target=self.background_reminder, daemon=True).start()

    def schedule(self):
        msg = "\n".join([f"{k}: {v['dose']} at {v['time']} ({v['purpose']})" for k, v in medications.items()])
        speak(msg)
        messagebox.showinfo("Schedule", msg)

    def relax(self):
        mood = tk.simpledialog.askstring("Mood", "How are you feeling?")
        if mood:
            technique = ai_recommend_relaxation(mood)
            desc = relaxation_guides[technique]
            speak(desc)
            messagebox.showinfo(technique, desc)

    def background_reminder(self):
        while True:
            current_time = datetime.now().strftime("%H:%M")
            check_medication_reminder(current_time)
            time.sleep(60)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
