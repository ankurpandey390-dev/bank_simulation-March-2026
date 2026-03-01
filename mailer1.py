import gmail

#credentials
email="" #mention your gmail id
app_pass="" #mention your app password



def send_openacn_email(uemail,uacn,upass,uname):
    con=gmail.GMail(email,app_pass)
    text_msg=f'''Welcome {uname},
You have successfully opened your account with our bank ABC
Here is your credentials
ACN = {uacn}
Pass = {upass}

Kindly Change your password on 1st login

Thanks
ABC Bank
Noida,UP,India
'''
    msg=gmail.Message(to=uemail,subject="Account Opened",text=text_msg)
    con.send(msg)

def send_otp_forgot(uemail,uname,otp):
    con=gmail.GMail(email,app_pass)
    text_msg=f'''Hello {uname},
Here is your otp to recover password
OTP = {otp}

Kindly do not share otp to others

Thanks
ABC Bank
Noida,UP,India
'''
    msg=gmail.Message(to=uemail,subject="Password Recovery",text=text_msg)
    con.send(msg)

def send_otp_close(uemail,uname,otp):
    con=gmail.GMail(email,app_pass)
    text_msg=f'''Hello {uname},
Here is your otp to close your account
OTP = {otp}

Kindly do not share otp to others

Thanks
ABC Bank
Noida,UP,India
'''
    msg=gmail.Message(to=uemail,subject="Account closure",text=text_msg)
    con.send(msg)    


