import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from kittentts import KittenTTS
import soundfile as sf

# Available options
MODELS = [
    "KittenML/kitten-tts-mini-0.8",
    "KittenML/kitten-tts-micro-0.8",
    "KittenML/kitten-tts-nano-0.8",
    "KittenML/kitten-tts-nano-0.8-int8"
]

VOICES = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']

def browse_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav")]
    )
    output_path.set(file_path)

def generate_tts():
    try:
        text = text_input.get("1.0", tk.END).strip()
        model_name = model_var.get()
        voice = voice_var.get()
        sample_rate = int(sample_rate_var.get())
        file_path = output_path.get()

        if not text:
            messagebox.showerror("Error", "Text cannot be empty!")
            return

        if not file_path:
            messagebox.showerror("Error", "Please select output file!")
            return

        status_label.config(text="Loading model...")
        root.update()

        m = KittenTTS(model_name)

        status_label.config(text="Generating audio...")
        root.update()

        audio = m.generate(text, voice=voice)

        sf.write(file_path, audio, sample_rate)

        status_label.config(text="Done ✅")
        messagebox.showinfo("Success", "Audio generated successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Kitten TTS GUI")
root.geometry("500x500")

# Model Dropdown
tk.Label(root, text="Select TTS Model:").pack(pady=5)
model_var = tk.StringVar(value=MODELS[2])
model_dropdown = ttk.Combobox(root, textvariable=model_var, values=MODELS, state="readonly")
model_dropdown.pack()

# Voice Dropdown
tk.Label(root, text="Select Voice:").pack(pady=5)
voice_var = tk.StringVar(value=VOICES[0])
voice_dropdown = ttk.Combobox(root, textvariable=voice_var, values=VOICES, state="readonly")
voice_dropdown.pack()

# Sample Rate
tk.Label(root, text="Sample Rate (Hz):").pack(pady=5)
tk.Label(root, text="(8000, 16000, 220500, 24000 (Default), 44100, 48000").pack(pady=5)
sample_rate_var = tk.StringVar(value="24000")
sample_rate_entry = tk.Entry(root, textvariable=sample_rate_var)
sample_rate_entry.pack()

# Text Input
tk.Label(root, text="Enter Text:").pack(pady=5)
text_input = tk.Text(root, height=6)
text_input.pack(padx=10, fill="both")

# Output File
tk.Label(root, text="Output File:").pack(pady=5)
output_path = tk.StringVar()
tk.Entry(root, textvariable=output_path).pack(padx=10, fill="x")
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

# Generate Button
tk.Button(root, text="Generate Speech", command=generate_tts, bg="green", fg="white").pack(pady=15)

# Status Label
status_label = tk.Label(root, text="Idle")
status_label.pack()

root.mainloop()
