import customtkinter as ctk
import mysql.connector
import pandas as pd
import random

df = pd.read_csv("IMBD.csv")
df.columns = df.columns.str.strip()
df = df.head(1000)

df2 = pd.read_csv("spotify_tracks.csv")
df2 = df2.sample(frac=1, random_state=42)  # shuffle
df2 = df2.head(1000)

df3 = pd.read_csv("books.csv")
df3 = df3.sample(frac=1, random_state=42)  # shuffle
df3 = df3.head(2000)

#Dictionary of Lists
MOOD_TO_GENRE = {
	"joyful": ["Comedy", "Adventure"],
	"amused": ["Comedy"],
	"excited": ["Action", "Adventure"],
	"loved": ["Romance"],
	"admired": ["Biography"],
	"happy": ["Comedy" , "Family" ,"Biography"],
	"optimistic": ["Adventure"],
	"caring": ["Family"],
	"relieved": ["Comedy"],
	"melanchonic": ["Drama"],
	"heartBroken": ["Drama"],
	"disappointed": ["Drama"],
	"regretfull": ["Drama"],
	"angry": ["Action"],
	"irritated": ["Comedy"],
	"disapproving": ["Drama"],
	"anxious": ["Horror"],
	"nervous": ["Thriller"],
	"surprised": ["Mystery"],
	"awakened": ["Mystery"],
	"confused": ["Mystery"],
	"curious": ["Adventure"],
	"disgusted": ["Crime"],
	"neutral": ["Drama"],
	"hopeful": ["Romance"],
	"embarresed": ["Comedy"],
}
MOOD_TO_MUSIC = {
    "joyful": ["pop", "dance"],
    "amused": ["pop"],
    "excited": ["edm", "dance"],
    "loved": ["r&b", "pop"],
    "admired": ["indie", "acoustic"],
    "happy": ["pop", "dance"],
    "optimistic": ["indie", "pop"],
    "caring": ["acoustic"],
    "relieved": ["ambient"],

    "melanchonic": ["acoustic", "piano"],
    "heartBroken": ["blues", "acoustic"],
    "disappointed": ["indie"],
    "regretfull": ["acoustic"],

    "angry": ["rock", "metal"],
    "irritated": ["punk", "rock"],
    "Disapproving": ["rock"],

    "anxious": ["ambient"],
    "nervous": ["ambient"],

    "surprised": ["electronic"],
    "awakened": ["indie"],
    "confused": ["indie"],
    "curious": ["indie"],

    "disgusted": ["metal"],
    "neutral": ["pop"],
    "hopeful": ["acoustic", "pop"],
    "embarresed": ["pop"]
}
MOOD_TO_BOOKS = {
    "joyful":        ["Humor"],
    "amused":        ["Humor", "Comics & Graphic Novels"],
    "excited":       ["Fiction", "Comics & Graphic Novels"],
    "loved":         ["Fiction", "Poetry"],
    "admired":       ["Biography & Autobiography"],
    "happy":         ["Humor", "Juvenile Fiction"],
    "optimistic":    ["Biography & Autobiography", "Self-Help"],
    "caring":        ["Religion", "Biography & Autobiography"],
    "relieved":      ["Self-Help", "Religion"],

    "melanchonic":   ["Poetry", "Drama"],
    "heartBroken":   ["Poetry", "Drama"],
    "disappointed":  ["Philosophy", "Literary Criticism"],
    "regretfull":    ["Philosophy", "Biography & Autobiography"],

    "angry":         ["History", "Social Science"],
    "irritated":     ["Humor", "Comics & Graphic Novels"],
    "disapproving":  ["Social Science", "Philosophy"],
    "disgusted":     ["Psychology", "Social Science"],

    "anxious":       ["Self-Help", "Psychology"],
    "nervous":       ["Self-Help", "Religion"],
    "confused":      ["Philosophy", "Science"],
    "curious":       ["Science", "History"],
    "surprised":     ["History", "Science"],

    "awakened":      ["Philosophy", "Religion"],
    "hopeful":       ["Biography & Autobiography", "Religion"],

    "neutral":       ["Fiction", "History"],
    "embarresed":    ["Humor", "Psychology"],
}


#database connect
vibematch = mysql.connector.connect(host ="localhost" , user = "root", password="" , database="vibematch")
cur = vibematch.cursor()
    
def save_item(username, title, item_type, category):
    try:
        query = """
        INSERT INTO saved_items (username, title, type, category)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (username, title, item_type, category))
        vibematch.commit()
        print("Saved successfully")
    except Exception as e:
        print("Error saving item:", e)

def build_recc(parent, user):

	def show_recc():

		showbtn.pack_forget()

		db = mysql.connector.connect(host="localhost", user="root", password="", database="vibematch")

		def get_mood():
			cur = db.cursor()
			cur.execute("SELECT final_sentiment FROM sessions WHERE username=%s AND final_sentiment IS NOT NULL ORDER BY session_id DESC LIMIT 1", (user,))
			data = cur.fetchone()
			cur.close()
			if data:
				return data[0].lower()
			return "neutral"

		def clear():
			for w in content.winfo_children():
				w.destroy()

		main = ctk.CTkFrame(parent)
		main.pack(fill="both", expand=True, padx=10, pady=10)

		left = ctk.CTkFrame(main)
		left.pack(side="left", fill="both", expand=True, padx=(0, 8))

		right = ctk.CTkFrame(main, width=200)
		right.pack(side="right", fill="y")
		right.pack_propagate(False)

		mood_label = ctk.CTkLabel(left, text="Click a tab to get recommendations", font=("Arial", 18, "bold"))
		mood_label.pack(pady=(10, 6))

		tab_frame = ctk.CTkFrame(left, fg_color="transparent")
		tab_frame.pack(pady=(0, 10))

		content = ctk.CTkScrollableFrame(left)
		content.pack(fill="both", expand=True)

		ctk.CTkLabel(right, text="Your Session", font=("Arial", 14, "bold")).pack(pady=(16, 6), padx=12, anchor="w")

		mood_detail = ctk.CTkLabel(right, text="No session yet", font=("Arial", 12), text_color="gray", wraplength=180, justify="left")
		mood_detail.pack(padx=12, anchor="w")

		def show_movies():
			clear()
			mood = get_mood()
			mood_label.configure(text="You seem:  " + mood.capitalize())
			mood_detail.configure(text="Mood: " + mood.capitalize())

			genres = MOOD_TO_GENRE.get(mood, ["Drama"])
			filtered = df[df["genre"].str.contains("|".join(genres), case=False, na=False)]

			if len(filtered) == 0:
				ctk.CTkLabel(content, text="No movies found for this mood.", font=("Arial", 13)).pack(pady=40)
				return

			movies = filtered.sample(min(10, len(filtered)))

			grid = ctk.CTkFrame(content, fg_color="transparent")
			grid.pack(fill="both", expand=True, padx=4, pady=4)
			grid.columnconfigure(0, weight=1)
			grid.columnconfigure(1, weight=1)
			grid.columnconfigure(2, weight=1)

			for items in range(len(movies)):
				row_pos = items // 3
				col_pos = items % 3

				title  = str(movies.iloc[items]["title"]).strip()
				genre  = str(movies.iloc[items]["genre"]).strip()
				rating = str(movies.iloc[items]["rating"]).strip()
				desc   = str(movies.iloc[items]["description"]).strip()
				year   = str(movies.iloc[items]["year"]).strip()
				match_pct = random.randint(82, 96)

				card = ctk.CTkFrame(grid, corner_radius=12)
				card.grid(row=row_pos, column=col_pos, padx=8, pady=8, sticky="nsew")

				toprow = ctk.CTkFrame(card , fg_color="transparent")
				toprow.pack(fill="x" , padx = 10 , pady=(10, 2))

				label1 = ctk.CTkLabel(toprow, text=str(match_pct) + "% match    Rating: " + rating, font=("Arial", 11), text_color="gray", anchor="w")
				label1.pack(side ="left")

				addbtn = ctk.CTkButton(toprow , text="+" , width = 25 , height = 25 , command=lambda t=title , g=genre :save_item(user, t, "movie" , g))
				addbtn.pack(side="right")

				label2 = ctk.CTkLabel(card, text=title if len(title) <= 35 else title[:33] + "..", font=("Arial", 13, "bold"), anchor="w", justify="left")
				label2.pack(anchor="w", padx=10, pady=(2, 0))

				label3 = ctk.CTkLabel(card, text="(" + year + ")  " + genre.split(",")[0].strip(), font=("Arial", 11), text_color="gray", anchor="w")
				label3.pack(anchor="w", padx=10)

				label4 = ctk.CTkLabel(card, text=desc[:120] + "..." if len(desc) > 120 else desc, font=("Arial", 11), text_color="gray", wraplength=195, anchor="w", justify="left")
				label4.pack(anchor="w", padx=10, pady=(4, 12))

		def show_songs():
			clear()
			mood_label.configure(text="You seem:  " + get_mood().capitalize())
			

			mood = get_mood()
			genres = MOOD_TO_MUSIC.get(mood , ["pop"])
			filtered = df2[df2["track_genre"].str.contains("|".join(genres) , case = False ,na = False)]

			if len(filtered) == 0:
				ctk.CTkLabel(content, text="No Songs found for this mood.", font=("Arial", 13)).pack(pady=40)
				return
			songs = filtered.sample(min(10, len(filtered)))

			grid = ctk.CTkFrame(content, fg_color="transparent")
			grid.pack(fill="both", expand=True, padx=4, pady=4)
			grid.columnconfigure(0, weight=1)#equal column size and more spacing between columns 
			grid.columnconfigure(1, weight=1)
			grid.columnconfigure(2, weight=1)

			for items in range(len(songs)):
				row_pos = items // 3
				col_pos = items % 3

				title  = str(songs.iloc[items]["track_name"]).strip()
				genre  = str(songs.iloc[items]["track_genre"]).strip()
				popularity = str(songs.iloc[items]["popularity"]).strip()
				artist   = str(songs.iloc[items]["artists"]).strip()
				album_name   = str(songs.iloc[items]["album_name"]).strip()
				match_pct = random.randint(82, 96)

				card = ctk.CTkFrame(grid, corner_radius=12)
				card.grid(row=row_pos, column=col_pos, padx=8, pady=8, sticky="nsew")

				toprow = ctk.CTkFrame(card , fg_color="transparent")
				toprow.pack(fill="x" , padx = 10 , pady=(10, 2))

				label1 = ctk.CTkLabel(toprow, text=str(match_pct) + f"% match    Popularity:{popularity} " , font=("Arial", 11), text_color="gray")
				label1.pack(side ="left")

				addbtn = ctk.CTkButton(toprow , text="+" , width = 25 , height = 25, command=lambda t=title , g=genre :save_item(user, t, "song" , g))
				addbtn.pack(side="right")

				label2 = ctk.CTkLabel(card, text=title if len(title) <= 35 else title[:33] + "..", font=("Arial", 13, "bold"), anchor="w", justify="left")
				label2.pack(anchor="w", padx=10, pady=(2, 0))

				label3 = ctk.CTkLabel(card,text=f"Artist: {artist}",font=("Arial", 11),text_color="gray",anchor="w")
				label3.pack(anchor="w", padx=10)

				label4 = ctk.CTkLabel(card, text=f"Album name: {album_name} Genre:{genre}", font=("Arial", 11), text_color="gray", wraplength=195, anchor="w", justify="left")
				label4.pack(anchor="w", padx=10, pady=(4, 12))



		def show_books():
			clear()
			mood_label.configure(text="You seem:  " + get_mood().capitalize())
			
			mood = get_mood()

			genres = MOOD_TO_BOOKS.get(mood ,["Fiction"])
			import re
			pattern = "|".join([r"(?<![a-zA-Z])" + re.escape(g) + r"(?![a-zA-Z])" for g in genres])
			filtered = df3[df3["categories"].str.contains(pattern, case=False, na=False, regex=True)]

			if len(filtered) == 0:
				ctk.CTkLabel(content, text="No Books found for this mood.", font=("Arial", 13)).pack(pady=40)
				return

			books = filtered.sample(min(10, len(filtered)))

			grid = ctk.CTkFrame(content, fg_color="transparent")
			grid.pack(fill="both", expand=True, padx=4, pady=4)
			grid.columnconfigure(0, weight=1)
			grid.columnconfigure(1, weight=1)
			grid.columnconfigure(2, weight=1)

			for items in range(len(books)):
				row_pos = items // 3
				col_pos = items % 3

				title  = str(books.iloc[items]["title"]).strip()
				genre  = str(books.iloc[items]["categories"]).strip()
				rating = str(books.iloc[items]["average_rating"]).strip()
				authors   = str(books.iloc[items]["authors"]).strip()
				subtitle   = str(books.iloc[items]["subtitle"]).strip()
				match_pct = random.randint(82, 96)

				card = ctk.CTkFrame(grid, corner_radius=12)
				card.grid(row=row_pos, column=col_pos, padx=8, pady=8, sticky="nsew")

				toprow = ctk.CTkFrame(card , fg_color="transparent")
				toprow.pack(fill="x" , padx = 10 , pady=(10, 2))

				label1 = ctk.CTkLabel(toprow, text=str(match_pct) + f"% match    Rating:{rating} " , font=("Arial", 11), text_color="gray", anchor="w")
				label1.pack(side="left")

				addbtn = ctk.CTkButton(toprow , text="+" , width = 25 , height = 25 , command=lambda t=title , g=genre :save_item(user, t, "book" , g))
				addbtn.pack(side="right")

				label2 = ctk.CTkLabel(card, text=title if len(title) <= 35 else title[:33] + "..", font=("Arial", 13, "bold"), anchor="w", justify="left")
				label2.pack(anchor="w", padx=10, pady=(2, 0))

				label3 = ctk.CTkLabel(card,text=f"Author: {authors}",font=("Arial", 11),text_color="gray",anchor="w")
				label3.pack(anchor="w", padx=10)


				label4 = ctk.CTkLabel(card, text=f"Subtitle: {subtitle} Genre:{genre}", font=("Arial", 11), text_color="gray", wraplength=195, anchor="w", justify="left")
				label4.pack(anchor="w", padx=10, pady=(4, 12))


		

		tabs = [("Movies", show_movies), ("Songs", show_songs), ("Books", show_books)]

		for name, fn in tabs:
			ctk.CTkButton(tab_frame, text=name, width=100, command=fn).pack(side="left", padx=5)

		show_movies()

	showbtn = ctk.CTkButton(parent, text="Show Recommendations", command=show_recc)
	showbtn.pack(padx=10, pady=10)