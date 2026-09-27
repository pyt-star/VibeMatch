import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
sender="vibematch360@gmail.com"
receiver="devampithadia13@gmail.com"
password="ivvxjfkaimbfjbqd"
# Authentication
s.login(sender, password)
# message to be sent
message = "Thank you for rejistering in our app!!!"
# sending the mail
s.sendmail(sender, receiver, message)
print("Email sent Successfully!!!")
# terminating the session
s.quit()
