#use of moduls to import build function from different pages
import customtkinter as ctk
from playlists import build_playlists
from voice_session import build_voice
from home import build_home
from insights import buildinsight
from reccomendations import build_recc
import mysql.connector 

#database connect
vibematch = mysql.connector.connect(host ="localhost" , user = "root", password="" , database="vibematch")
cur = vibematch.cursor()

def open_dashboard(user):


	app = ctk.CTk()


	app.geometry("940x500")
	app.title("VIBEMATCH/DASHBOARD")

	ctk.set_appearance_mode("dark")

	app.grid_rowconfigure(0, weight=1)
	app.grid_columnconfigure(1, weight=1)

	sidebar = ctk.CTkFrame(app, width=200 , fg_color="#111111")
	sidebar.grid( row= 0 , column = 0 , sticky="ns")
	sidebar.grid_propagate(False)


	


	#all pages load logic
	home_page = ctk.CTkFrame(app)
	voice_page = ctk.CTkFrame(app)
	recc_page = ctk.CTkFrame(app)
	playlist_page = ctk.CTkFrame(app)
	insights_page = ctk.CTkFrame(app)

	all_pages = [home_page , voice_page , recc_page , playlist_page , insights_page]
	for i in all_pages:
		i.grid(row = 0 , column = 1 , sticky = "nsew")

	def show(page):
		for i in all_pages:
			i.grid_remove()
		page.grid()

	build_home(home_page , user)
	build_voice(voice_page , user )
	build_recc(recc_page , user)
	build_playlists(playlist_page , user)
	buildinsight(insights_page , user)


    #sidebar buttons
	title = ctk.CTkLabel(sidebar , text="VIBEMATCH" , font=("Arial" , 20 , "bold"), text_color="#1DB954")
	title.grid(row= 0 , column = 0 , pady = 10 , padx = 10)
	HomeBtn = ctk.CTkButton(sidebar , text="Home" , font =("Arial",20 , "bold"), text_color="white" , command=lambda:show(home_page))
	HomeBtn.grid(row = 4 , column = 0 , pady = 10 , padx = 10)
	voicesession = ctk.CTkButton(sidebar , text="Voice\nSession" , font =("Arial",20 , "bold"), text_color="white" , command=lambda:show(voice_page))
	voicesession.grid(row = 6 , column = 0 , pady = 10 , padx = 10)
	reccomendation = ctk.CTkButton(sidebar , text="Reccomendation" , font =("Arial",20 , "bold"), text_color="white" , command=lambda:show(recc_page))
	reccomendation.grid(row = 8 , column = 0 , pady = 10 , padx = 10)
	playlist_btn = ctk.CTkButton(sidebar , text="Playlists" , font =("Arial",20 , "bold"), text_color="white" ,command=lambda: show(playlist_page))
	playlist_btn.grid(row = 10 , column = 0 , pady = 10 , padx = 10)
	insights = ctk.CTkButton(sidebar , text="Insights" , font =("Arial",20 , "bold"), text_color="white", command = lambda: show(insights_page))
	insights.grid(row = 12 , column = 0 , pady = 10 , padx = 10)
	sidebar.grid_rowconfigure(16, weight=1)#for long space between buttons



    
	def logout():
	    cur.execute("DELETE FROM active_sessions WHERE username=%s", (user,))
	    vibematch.commit()

	    import login_page_main
	    app.destroy()
	    login_page_main.open_login()


	logout = ctk.CTkButton(sidebar , text="logout" , font =("Arial",20 , "bold"), text_color="red", command=logout)
	logout.grid(row = 17 , column = 0 , pady = 10 , padx = 10 )

	show(home_page)

	app.mainloop()