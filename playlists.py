import customtkinter as ctk
import mysql.connector

vibematch = mysql.connector.connect(host="localhost",user="root",password="",database="vibematch")
cur = vibematch.cursor()


def build_playlists(parent, user):

    main = ctk.CTkFrame(parent)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    filter_frame = ctk.CTkFrame(main, fg_color="transparent")
    filter_frame.pack(pady=(0, 10))

    content = ctk.CTkScrollableFrame(main)
    content.pack(fill="both", expand=True)


    def delete_item(user, title):
        try:
            cur.execute("DELETE FROM saved_items WHERE username=%s AND title=%s",(user, title))
            vibematch.commit()
            print("Deleted")
            
            load_items()
        except Exception as e:
            print("Error deleting:", e)

    current_filter = None

    def load_items(filter_type=None):

        nonlocal current_filter
        current_filter = filter_type

        for widget in content.winfo_children():
            widget.destroy()

        if filter_type:
            cur.execute("SELECT title, type, category FROM saved_items WHERE username=%s AND type=%s",(user, filter_type))
        else:
            cur.execute("SELECT title, type, category FROM saved_items WHERE username=%s",(user,))

        items = cur.fetchall()

        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=4, pady=4)

        for i in range(3):
            grid.columnconfigure(i, weight=1)

        for i in range(len(items)):
            row_pos = i // 3
            col_pos = i % 3

            grid.rowconfigure(row_pos, weight=1)

            title = str(items[i][0]).strip()
            item_type = str(items[i][1]).strip()
            category = str(items[i][2]).strip()

            card = ctk.CTkFrame(grid, corner_radius=12)
            card.grid(row=row_pos, column=col_pos, padx=8, pady=8, sticky="nsew")

            toprow = ctk.CTkFrame(card, fg_color="transparent")
            toprow.pack(fill="x", padx=10, pady=(10, 2))

            label1 = ctk.CTkLabel(toprow,text=f"Saved :{item_type.capitalize()}",font=("Arial", 11),text_color="gray")
            label1.pack(side="left")

            removebtn = ctk.CTkButton(toprow,text="x",width=25,height=25,command=lambda t=title: delete_item(user, t))
            removebtn.pack(side="right")

            label2 = ctk.CTkLabel(card,text=title if len(title) <= 35 else title[:33] + "..",font=("Arial", 13, "bold"),anchor="w",justify="left")
            label2.pack(anchor="w", padx=10, pady=(2, 0))

            label3 = ctk.CTkLabel(card,text=f"Category: {category}",font=("Arial", 11),text_color="gray",anchor="w")
            label3.pack(anchor="w", padx=10, pady=(4, 12))

            content.update_idletasks()

    ctk.CTkButton(filter_frame, text="All", width=80,
                  command=lambda: load_items(None)).grid(row=0, column=0, padx=5)

    ctk.CTkButton(filter_frame, text="Movies", width=80,
                  command=lambda: load_items("movie")).grid(row=0, column=1, padx=5)

    ctk.CTkButton(filter_frame, text="Songs", width=80,
                  command=lambda: load_items("song")).grid(row=0, column=2, padx=5)

    ctk.CTkButton(filter_frame, text="Books", width=80,
                  command=lambda: load_items("book")).grid(row=0, column=3, padx=5)

    ctk.CTkButton(filter_frame, text="Reload", width=90,
                  command=lambda: load_items(current_filter)).grid(row= 0, column = 4 , padx = 5)

    # Load all initially
    load_items()