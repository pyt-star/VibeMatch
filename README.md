# 🎵 VIBEMATCH – Mood-Based Recommendation System

VIBEMATCH is a desktop application that provides personalized recommendations based on the user's mood and emotions. The application recommends movies, books, songs and activities to help users discover content that matches their current mood.

## ✨ Features

- 🔐 User Registration and Login
- 🎙️ Voice-based mood input
- 😊 Emotion and sentiment analysis
- 🎬 Movie recommendations
- 📚 Book recommendations
- 🎵 Song recommendations
- 🎯 Activity recommendations
- 💾 Save recommended items to personal playlists
- 📊 User insights and session information
- 🗄️ MySQL database integration
- 🖥️ User-friendly desktop interface

## 🛠️ Technologies Used

### Programming Language
- Python

### GUI
- Tkinter
- CustomTkinter

### Machine Learning / NLP
- VADER Sentiment Analysis
- RoBERTa-based emotion classification
- Hugging Face Transformers

### Database
- MySQL

### Other Libraries
- SpeechRecognition
- Pandas
- NumPy

## 🧠 How It Works

1. The user logs into the VIBEMATCH application.
2. The user provides their mood through text or voice input.
3. The application processes the input using sentiment and emotion analysis.
4. The detected emotion is used to determine suitable recommendations.
5. VIBEMATCH displays recommendations for movies, books, songs and activities.
6. Users can save items they like to their personal playlist.
7. User sessions and saved items are stored in the MySQL database.

## 📂 Main Modules

- **Login/Register** – Handles user authentication.
- **Dashboard** – Main interface for accessing different features.
- **Voice Session** – Accepts voice input and analyzes the user's emotions.
- **Recommendations** – Displays personalized content based on the detected mood.
- **Playlists** – Allows users to save and manage recommended items.
- **Insights** – Displays information related to the user's sessions and activity.

## 🗄️ Database

VIBEMATCH uses MySQL for storing application data.

The database contains tables for managing information such as:

- Users
- Saved Items
- Active Sessions
- Playlists
- Content

> Create the required database and tables before running the application.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/pyt-star/VIBEMATCH.git
