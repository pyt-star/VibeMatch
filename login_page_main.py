import customtkinter as ctk
import mysql.connector 


vibematch = mysql.connector.connect(host ="localhost" , user = "root", password="" , database="vibematch")
cur = vibematch.cursor()


def logintodb(user, passw):
    try:
        query = "SELECT * FROM login WHERE username=%s AND password=%s"
        cur.execute(query, (user, passw))

        result = cur.fetchone()

        return True if result else False
    except Exception as e:
        print("Database error" , e)
        return False
        
def check_session():
    cur.execute("SELECT username FROM active_sessions LIMIT 1")
    result = cur.fetchone()
    return result[0] if result else None
        


def open_login():
    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.geometry("700x500")
    app.title("VIBEMATCH")

    

    centerframe = ctk.CTkFrame(app, width=350, height=300, corner_radius=15)
    centerframe.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(
        centerframe,
        text="LOGIN",
        font=("Arial", 24, "bold"),
        text_color="white"
    )
    title.pack(pady=(20, 10))

    username_entry = ctk.CTkEntry(centerframe, placeholder_text="Username", width=250)
    username_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(centerframe, placeholder_text="Password", show="*", width=250)
    password_entry.pack(pady=10)

    message_label = ctk.CTkLabel(centerframe, text="", text_color="white")
    message_label.pack(pady=5)


    def submitact():
        user = username_entry.get()
        pwd = password_entry.get()

        if logintodb(user, pwd):

            message_label.configure(text="Login Successful", text_color="green")

            cur.execute("DELETE FROM active_sessions WHERE username=%s", (user,))


            cur.execute("INSERT INTO active_sessions (username) VALUES (%s)", (user,))
            vibematch.commit()

            app.destroy()
            import dashboard
            dashboard.open_dashboard(user) 

        else:
            message_label.configure(text="Login Failed", text_color="red")

    def open_register_page():
        app.destroy()
        import register_page
        register_page.open_register()

    def clear_fields():
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")


    login_btn = ctk.CTkButton(centerframe, text="Login", command=submitact)
    login_btn.pack(pady=20)

    register_btn = ctk.CTkButton(centerframe, text="Register", command=open_register_page)
    register_btn.pack(pady=5)

    clear_btn = ctk.CTkButton(centerframe, text="Clear", command=clear_fields)
    clear_btn.pack(pady=5)

    app.mainloop()


if __name__ == "__main__":
    user = check_session()

    if user:
        import dashboard
        dashboard.open_dashboard(user)
        
    else:
        open_login()