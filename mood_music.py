import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

# Initialize Spotify client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Initialize NLTK sentiment analyzer
sia = SentimentIntensityAnalyzer()

def get_music_recommendations(mood):
    mood_map = {
        "happy": "happy hindi songs",
        "sad": "sad hindi songs",
        "angry": "angry hindi songs",
        "emotional": "emotional hindi songs",
        "crying": "heartbreak hindi songs",
        "relaxed": "relaxing hindi songs"
    }
    
    results = sp.search(q=mood_map.get(mood, "hindi songs"), type="track", limit=20)
    return results["tracks"]["items"]

def detect_mood(user_input):
    mood_map = {
        "happy": ["happy", "joyful", "cheerful"],
        "sad": ["sad", "depressed", "unhappy"],
        "angry": ["angry", "furious", "annoyed"],
        "emotional": ["emotional", "sensitive"],
        "crying": ["crying", "tearful"],
        "relaxed": ["relaxed", "calm"]
    }
    
    user_input = user_input.lower()
    for mood, keywords in mood_map.items():
        if any(keyword in user_input for keyword in keywords):
            return mood
    return "relaxed"  # default mood

def play_song(song):
    webbrowser.open(song["external_urls"]["spotify"])

def recommend_music():
    user_input = entry.get()
    mood = detect_mood(user_input)
    recommendations = get_music_recommendations(mood)
    recommendation_text.delete(1.0, tk.END)
    for i, song in enumerate(recommendations):
        recommendation_text.insert(tk.END, f"{i+1}. {song['name']} by {song['artists'][0]['name']}\n")

    def play_selected_song():
        try:
            song_choice = int(song_entry.get())
            if 1 <= song_choice <= len(recommendations):
                play_song(recommendations[song_choice - 1])
            else:
                messagebox.showerror("Invalid song choice", "Please enter a valid song number.")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a number.")

    song_label = tk.Label(root, text="Enter song number to play:", bg="#f0f0f0")
    song_label.pack()
    song_entry = tk.Entry(root)
    song_entry.pack()
    play_button = tk.Button(root, text="Play Song", command=play_selected_song, bg="#4CAF50", fg="#ffffff")
    play_button.pack()

root = tk.Tk()
root.title("Music Mood Recommendation")
root.config(bg="#C0C0C0")

label = tk.Label(root, text="How are you feeling today?", bg="#f0f0f0", fg="#00698f", font=("Arial", 16))
label.pack(pady=20)

entry = tk.Entry(root, font=("Arial", 16))
entry.pack()

button = tk.Button(root, text="Get Recommendations", command=recommend_music, bg="#4CAF50", fg="#ffffff", font=("Arial", 16))
button.pack(pady=10)

recommendation_text = tk.Text(root, height=10, width=50, font=("Arial", 12))
recommendation_text.pack(pady=10)

nltk.download('vader_lexicon')  # Download NLTK data
root.mainloop()