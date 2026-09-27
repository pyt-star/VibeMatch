import customtkinter as ctk
import mysql.connector
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def buildinsight(parent, user):

    # ================= DATABASE =================
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vibematch"
    )

    cur = db.cursor()

    cur.execute("""
        SELECT start_time, final_sentiment 
        FROM sessions 
        WHERE username=%s 
        AND final_sentiment IS NOT NULL
        ORDER BY start_time ASC
    """, (user,))

    data = cur.fetchall()

    # ================= NO DATA =================
    if not data:
        ctk.CTkLabel(parent, text="No data available").pack(pady=20)
        return

    # ================= SCORE MAP (MATCH YOUR BUCKETS) =================
    score_map = {

        # positive
        "joyful": 3, "excited": 3, "amused": 3,
        "happy": 3, "optimistic": 3, "loved": 3,
        "admired": 3,

        # calm / mid positive
        "relieved": 2, "caring": 2, "hopeful": 2,
        "curious": 2, "awakened": 2,

        # neutral
        "neutral": 1, "confused": 1,

        # low
        "disappointed": 1, "regretfull": 1,
        "nervous": 1, "embarresed": 1,

        # negative
        "melanchonic": 0, "heartbroken": 0,
        "angry": 0, "irritated": 0,
        "disgusted": 0, "disapproving": 0,
        "anxious": 0
    }

    # ================= PROCESS =================
    moods = []
    weekdays = []
    scores = []

    for row in data:
        dt = row[0]
        mood = row[1].lower().strip()

        moods.append(mood)
        weekdays.append(dt.strftime("%A"))
        scores.append(score_map.get(mood, 1))

    # ---- Most Common Mood ----
    most_common = Counter(moods).most_common(1)[0][0]

    # ---- Total Sessions ----
    total_sessions = len(moods)

    # ---- Happiest Day ----
    day_scores = defaultdict(list)

    for i in range(len(scores)):
        day_scores[weekdays[i]].append(scores[i])

    avg_scores = {}
    for day in day_scores:
        avg_scores[day] = sum(day_scores[day]) / len(day_scores[day])

    happiest_day = max(avg_scores, key=avg_scores.get)

    # ================= UI =================
    main = ctk.CTkFrame(parent)
    main.pack(fill="both", expand=True)

    # ---------- TOP ----------
    top = ctk.CTkFrame(main)
    top.pack(fill="x", pady=10)

    ctk.CTkLabel(top, text=f"Most Common Mood: {most_common}").pack(side="left", padx=20)
    ctk.CTkLabel(top, text=f"Happiest Day: {happiest_day}").pack(side="left", padx=20)
    ctk.CTkLabel(top, text=f"Total Sessions: {total_sessions}").pack(side="left", padx=20)

    # ---------- GRAPH ----------
    graph_frame = ctk.CTkFrame(main)
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    fig, ax = plt.subplots()

    ax.plot(scores)
    ax.set_title("Mood Trend")
    ax.set_xlabel("Sessions")
    ax.set_ylabel("Mood Score")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- INSIGHT ----------
    bottom = ctk.CTkFrame(main)
    bottom.pack(fill="x", pady=10)

    if most_common in ["melanchonic", "heartbroken"]:
        tip = "You've been feeling low lately. Try relaxing activities."

    elif most_common in ["joyful", "happy", "excited"]:
        tip = "You're in a great mood! Keep it going."

    elif most_common in ["anxious", "nervous"]:
        tip = "You seem stressed. Take breaks and relax."

    else:
        tip = "You're balanced. Try exploring new activities."

    ctk.CTkLabel(bottom, text="Insight: " + tip).pack(pady=10)