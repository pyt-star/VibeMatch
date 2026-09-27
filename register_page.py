import customtkinter as ctk
import mysql.connector

def open_register():

    def logintodb(user, passw , eml):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="vibematch"
        )
        cursor = con.cursor()

        query = "INSERT INTO login (username, password , email) VALUES (%s, %s,%s)"
        cursor.execute(query, (user, passw,eml))
        con.commit()

    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.geometry("940x500")
    app.title("VIBEMATCH/Register")

    centerframe = ctk.CTkFrame(app, width=350, height=300, corner_radius=15)
    centerframe.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(centerframe, text="REGISTER", font=("Arial", 24, "bold"))
    title.pack(pady=20)

    username = ctk.CTkEntry(centerframe, placeholder_text="Username", width=250)
    username.pack(pady=10)

    password = ctk.CTkEntry(centerframe, placeholder_text="Password", show="*", width=250)
    password.pack(pady=10)

    email = ctk.CTkEntry(centerframe, placeholder_text="Email", width=250)
    email.pack(pady=10)


    message_label = ctk.CTkLabel(centerframe, text="")
    message_label.pack(pady=5)

    def sendEmail(receiver_email , user):
        import smtplib

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        sender = "vibematch360@gmail.com"
        password = "ivvxjfkaimbfjbqd" 

        s.login(sender, password)

        message = f"""Subject: Welcome to VibeMatch 

            Hi {user},

            Welcome to VibeMatch! We're excited to have you on board 

            Your account has been successfully created.

            Here are your details:
            -----------------------------------
            Username: {user}
            Email: {receiver_email}
            -----------------------------------

            You can now log in and start exploring features like:
             Finding matches
             Chatting with people
             Personalized recommendations

            If you did not register for this account, please ignore this email.

            Best regards,  
            Team VibeMatch 
            """

        s.sendmail(sender, receiver_email, message)

        print("Email sent Successfully!!!")

        s.quit()


    def register():
        user = username.get()
        pwd = password.get()
        eml = email.get()

        logintodb(user, pwd, eml)
        sendEmail(eml, user)   

        message_label.configure(text="Registration Successful", text_color="green")




    def go_back():
        app.destroy()
        import login_page_main
        login_page_main.open_login()



    register_btn = ctk.CTkButton(centerframe, text="Register", command=register)
    register_btn.pack(pady=10)

    back_btn = ctk.CTkButton(centerframe, text="Back", command=go_back)
    back_btn.pack(pady=5)

    app.mainloop()