import customtkinter as ctk
from transformers import pipeline#will take roberta model 
import speech_recognition as sr
import threading
import mysql.connector 
from collections import Counter #to count most detected emotions 

#database connect
vibematch = mysql.connector.connect(host ="localhost" , user = "root", password="" , database="vibematch")
cur = vibematch.cursor()
#creating object of roberta model
emotion_pipe = pipeline("text-classification",model ="SamLowe/roberta-base-go_emotions", top_k=1)


def build_voice(parent , user):

    parent.pack_propagate(False)


    info_label = ctk.CTkLabel(parent,text="""Studies show that naming your emotions helps your brain process them better.
    Even just putting feelings into words has been shown to reduce stress and improve mental clarity.

    VibeMatch uses Roberto AI to detect 28 distinct emotions from your responses
    including joy, sadness, anxiety, excitement, relief, anger, gratitude, grief, and more.

    Simply answer 5 short questions by voice or text,
    and VibeMatch will match you with music, movies and books
    that fit exactly how you feel right now.""",
        font=("Arial", 18), wraplength=600,justify="center")

    info_label.pack(padx=20, pady=20)

    def start_session():

        start_button.pack_forget()
        info_label.pack_forget()

        recognizer = sr.Recognizer()
        
        cur.execute("INSERT INTO sessions (username) VALUES (%s)", (user,))
        vibematch.commit()
        session_id = cur.lastrowid

        #progres bar to show how many questions done
        progress = ctk.CTkProgressBar(parent , width = 300)
        progress.pack(pady=20)
        progress.set(0)

        question = ctk.CTkLabel(parent, text="Walk me through your day , what happened and how did it make you feel?", font=("Arial", 20))
        question.pack(pady=30)

        mic_btn = ctk.CTkButton(parent,text="🎤",width=120,height=120,corner_radius=100,font=("Arial", 40),fg_color="#6C63FF")
        mic_btn.pack(pady=20)

        status_label = ctk.CTkLabel(parent, text="Tap to Speak or Type your response", text_color="gray")
        status_label.pack()

        response_box = ctk.CTkEntry(parent, width=400, height=40, placeholder_text="Your response...")
        response_box.pack(pady=20)

        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack()

        start_btn = ctk.CTkButton(btn_frame, text="Start Recording")
        start_btn.grid(row=0, column=1, padx=10)

        questions = [
            "Walk me through your day , what happened and how did it make you feel?",
            "Was there a moment today where you felt really good, proud, or at peace what was it?",
            "Did anything today leave you feeling drained, upset, or unsettled? Tell me about it.",
            "If your mood right now were a weather report, what would it say and why?",
            "Finish this sentence honestly , today I felt most alive when... or today was hard because..."
        ]

        current_qn = 0
        responses = [None] * len(questions)

        def back_button():
            nonlocal current_qn
            if current_qn > 0:
                if responses[current_qn] is None:
                    responses[current_qn] = ("", response_box.get(), "")
                else:
                    q, _, s = responses[current_qn]
                    responses[current_qn] = (q, response_box.get(), s)

                current_qn -= 1
                question.configure(text=questions[current_qn])

                response_box.delete(0, "end")
                if responses[current_qn]:
                    response_box.insert(0, responses[current_qn][1])

                progress.set((current_qn + 1) / len(questions))

        backbtn = ctk.CTkButton(btn_frame, text="<- Back" , command = back_button)
        backbtn.grid(row=0, column=0, padx=10)

        def restart_session():
            for widget in parent.winfo_children():
                widget.destroy()
            build_voice(parent, user)

        def show_summary():
            question.configure(text="Session Complete ")
            response_box.pack_forget()
            mic_btn.pack_forget()

            scroll_frame = ctk.CTkScrollableFrame(parent, width=600, height=300)
            scroll_frame.pack(pady=20)

            restart_btn = ctk.CTkButton(parent , text="Restart" , command=restart_session)
            restart_btn.pack(pady=10)

            
            cur.execute("SELECT sentiment FROM session_responses WHERE session_id=%s", (session_id,))
            sentiments = [row[0] for row in cur.fetchall()]

            counts = Counter(sentiments)

            final = counts.most_common(1)[0][0]

            # UPDATE SESSION TABLE
            cur.execute("UPDATE sessions SET final_sentiment=%s WHERE session_id=%s", (final, session_id))
            vibematch.commit()

            for i, item in enumerate(responses):
                if item:
                    q, r, s , emo , conf = item
                    ctk.CTkLabel(scroll_frame, text=f"Q{i+1}: {q}", font=("Arial", 14, "bold"), wraplength=550).pack(anchor="w", pady=5)
                    ctk.CTkLabel(scroll_frame, text=f"Response: {r}", wraplength=550).pack(anchor="w")
                    ctk.CTkLabel(scroll_frame, text=f"Sentiment: {s}").pack(anchor="w", pady=(0,10))
                    ctk.CTkLabel(scroll_frame, text=f"Emotion: {emo} ({conf:.0%})").pack(anchor="w", pady=(0,10))

            progress.set(1)
            backbtn.grid_remove()
            start_btn.grid_remove()
            next_btn.grid_remove()
            status_label.configure(text=f"Session Finished | Final Mood: {final}")

        def next_button():
            nonlocal current_qn

            text = response_box.get().strip()
            if not text:
                status_label.configure(text="Please speak or type something")
                return
            emotion_result = emotion_pipe(text)[0][0]

            detected_emotion = emotion_result['label']
            confidence = emotion_result['score']
            

            MOOD_BUCKETS = {
                "joy": "joyful", "excitement": "excited", "amusement": "amused",
                "admiration": "admired", "approval": "happy", "pride": "happy",
                "optimism": "optimistic", "love": "loved", "gratitude": "happy",
                "sadness": "melanchonic", "grief": "heartBroken", "disappointment": "disappointed",
                "remorse": "regretfull",
                "anger": "angry", "annoyance": "irritated", "disgust": "disgusted",
                "disapproval": "disapproving",
                "fear": "anxious", "nervousness": "nervous",
                "relief": "relieved", "caring": "caring",
                "surprise": "surprised", "realization": "awakened", "curiosity": "curious",
                "confusion": "confused", "desire": "hopeful", "embarrassment": "embarresed",
                "neutral": "neutral"
            }

            result = MOOD_BUCKETS.get(detected_emotion, "neutral")

            question_text = question.cget("text")

          
            cur.execute(
                "INSERT INTO session_responses (session_id, question, response, sentiment, emotion) VALUES (%s, %s, %s, %s, %s)",
                (session_id, question_text, text, result, detected_emotion))
            vibematch.commit()

            responses[current_qn] = (question_text, text, result , detected_emotion , confidence)

            if current_qn < len(questions) - 1:
                current_qn += 1
                question.configure(text=questions[current_qn])
                response_box.delete(0, "end")
                progress.set((current_qn + 1) / len(questions))
                status_label.configure(text="Next question...")
            else:
                show_summary()

        next_btn = ctk.CTkButton(btn_frame, text="Next →", fg_color="#6C63FF", command=next_button)
        next_btn.grid(row=0, column=2, padx=10)

        def record_and_analyze():
            try:
                parent.after(0, lambda: status_label.configure(text="Calibrating..."))
                parent.after(0, lambda: mic_btn.configure(fg_color="#1DB954"))

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=2)
                    parent.after(0, lambda: status_label.configure(text="Speak now..."))
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                text = recognizer.recognize_google(audio)

                parent.after(0, lambda: response_box.delete(0, "end"))
                parent.after(0, lambda: response_box.insert(0, text))
                parent.after(0, lambda: status_label.configure(text="Voice captured ✔ Click Next"))

            except Exception as e:
                parent.after(0, lambda: status_label.configure(text=f"Error: {str(e)}"))

            finally:
                parent.after(0, lambda: mic_btn.configure(fg_color="#6C63FF"))

        mic_btn.configure(command=lambda: threading.Thread(target=record_and_analyze).start())
        start_btn.configure(command=lambda: threading.Thread(target=record_and_analyze).start())

    start_button = ctk.CTkButton(parent , text="Start Session!" , command = start_session)
    start_button.pack(padx = 10 , pady=10)