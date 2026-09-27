import customtkinter as ctk
import playlists
import voice_session

def open_dashboard():


	app = ctk.CTk()


	app.geometry("940x500")
	app.title("VIBEMATCH/DASHBOARD")

	ctk.set_appearance_mode("dark")

	app.grid_rowconfigure(0, weight=1)
	app.grid_columnconfigure(1, weight=1)

	sidebar = ctk.CTkFrame(app, width=200 , fg_color="#111111")
	sidebar.grid( row= 0 , column = 0 , sticky="ns")
	sidebar.grid_propagate(False)


	mainframe = ctk.CTkFrame(app)
	mainframe.grid(row=0 , column = 1 , sticky="nsew")

	title = ctk.CTkLabel(sidebar , text="VIBEMATCH" , font=("Arial" , 20 , "bold"), text_color="#1DB954")
	title.grid(row= 0 , column = 0 , pady = 10 , padx = 10)

	HomeBtn = ctk.CTkButton(sidebar , text="Home" , font =("Arial",20 , "bold"), text_color="white")
	HomeBtn.grid(row = 4 , column = 0 , pady = 10 , padx = 10)
	def open_voice_session():

			 voice_session.open_voice()

	voicesession = ctk.CTkButton(sidebar , text="Voice\nSession" , font =("Arial",20 , "bold"), text_color="white" , command=open_voice_session)
	voicesession.grid(row = 6 , column = 0 , pady = 10 , padx = 10)

	reccomendation = ctk.CTkButton(sidebar , text="Reccomendation" , font =("Arial",20 , "bold"), text_color="white")
	reccomendation.grid(row = 8 , column = 0 , pady = 10 , padx = 10)
	def open_playlist():
	            
	            playlists.open_playlists()

	playlist_btn = ctk.CTkButton(sidebar , text="Playlists" , font =("Arial",20 , "bold"), text_color="white" ,command=open_playlist)
	playlist_btn.grid(row = 10 , column = 0 , pady = 10 , padx = 10)

	insights = ctk.CTkButton(sidebar , text="Insights" , font =("Arial",20 , "bold"), text_color="white")
	insights.grid(row = 12 , column = 0 , pady = 10 , padx = 10)

	sidebar.grid_rowconfigure(16, weight=1)
	def logout():
		import login_page_main
		app.destroy()
		login_page_main.open_login()


	logout = ctk.CTkButton(sidebar , text="logout" , font =("Arial",20 , "bold"), text_color="red", command=logout)
	logout.grid(row = 17 , column = 0 , pady = 10 , padx = 10 )

	titlemsg = ctk.CTkLabel(mainframe , text="Good Evening , Devam!" , font=("Arial" , 20 , "bold"),  text_color="white")
	titlemsg.grid(row = 0 , column = 0 , padx = 10 , pady = 10)

	insightframe = ctk.CTkFrame(mainframe)
	insightframe.grid(row = 2 , column = 0 , padx = 14 , pady = 14)

	voicesession_frame = ctk.CTkFrame(mainframe)
	voicesession_frame.grid(row = 2, column = 1 , padx = 14 , pady = 14)

	mood_trendd_frame = ctk.CTkFrame(mainframe)
	mood_trendd_frame.grid(row = 2 , column = 2 , padx = 14 , pady = 14)

	msg2 = ctk.CTkLabel(mainframe , text = "Recent Reccomendations" , font =("Arial",20 , "bold"), text_color="white")
	msg2.grid(row = 3 , column = 0 , padx = 14, pady = 10)


	app.mainloop()