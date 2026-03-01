from tkinter import Frame, Tk,Label,Entry,Button,simpledialog,messagebox
from tkinter.ttk import Combobox
import time
import random
import dbHandler,generator,sqlite3,mailer
from PIL import Image,ImageTk
dbHandler.create_table()

def update_time():
    lbl_date.configure(text=time.strftime("%A,%d-%b-%Y ⏰%r"))
    lbl_date.after(1000,update_time)

def forgot_screen():
    def main_click():
        frm.destroy()
        main_screen()
    
    def otp():
        uemail=e_email.get()
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select acn,name,pass from accounts where email=?"
        curobj.execute(query,(uemail,))
        conobj.close()
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot Password","Email does not exists")
        else:
            genotp=random.randint(1000,9999)
            mailer.send_otp_forgot(uemail,tup[1],genotp)
            messagebox.showinfo("Forgot Password","we have sent otp to your email")
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                messagebox.showinfo("Password",tup[2])
            else:
                messagebox.showerror("Forgot Password","Invalid otp")


    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.70)

    back_btn=Button(frm,text="back",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=main_click) # type: ignore
    back_btn.place(relx=0,rely=0)

    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),bg="pink")
    lbl_email.place(relx=.3,rely=.2)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.4,rely=.2)
    e_email.focus()

    otp_btn=Button(frm,text="send otp",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=otp)
    
    otp_btn.place(relx=.5,rely=.3)

def admin_screen():
    def logout_click():
        frm.destroy()
        main_screen()
    
    def close_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.2,relwidth=.8,relheight=.6)
        lbl_title=Label(ifrm,text="This is close account section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack()    

        uacn=simpledialog.askinteger("","Enter ACN")

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select email,name from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        
        if tup==None:
            messagebox.showerror("View Account","ACN does not exist")
        else:
            genotp=random.randint(1111,9999)
            mailer.send_otp_close(tup[0],tup[1],genotp)
            
            messagebox.showinfo("Close Account","we have sent otp to your email")
            uotp=simpledialog.askinteger("","Enter OTP")
            if genotp==uotp:
                conobj=sqlite3.connect(database='bank.sqlite3')
                curobj=conobj.cursor()
                query="delete from accounts where acn=?"
                curobj.execute(query,(uacn,))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Account Closure","Account closed")
            else:
                messagebox.showerror("Account Closure","Invalid otp")


    def view_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.2,relwidth=.8,relheight=.5)
        lbl_title=Label(ifrm,text="This is view account section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack()    

        uacn=simpledialog.askinteger("","Enter ACN")

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select acn,name,adhar,opendate,bal,mob,email from accounts where acn=?"
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("View Account","ACN does not exist")
        else:
            messagebox.showinfo("View Account",tup)
            messagebox.showinfo("View Account",f"ACN={tup[0]}\nName={tup[1]}")

        

    def open_click():
        def create():
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadhar=e_adhar.get()
            ubal=0
            uopen=time.strftime("%A,%d-%b-%Y %r")
            upass=generator.generate_pass()

            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="insert into accounts values(null,?,?,?,?,?,?,?)"
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,ubal,uopen))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite3")
            curobj=conobj.cursor()
            query="select max(acn) from accounts"
            curobj.execute(query)
            uacn=curobj.fetchone()[0]
            conobj.close()

            mailer.send_openacn_email(uemail,uacn,upass,uname)

            messagebox.showinfo("Account","Account opened and credentials are mailed to customer email")

            e_name.delete(0,"end")
            e_email.delete(0,"end")
            e_mob.delete(0,"end")
            e_adhar.delete(0,"end")

            e_name.focus()
            


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.1,rely=.25,relwidth=.8,relheight=.6)
        lbl_title=Label(ifrm,text="This is open account section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack()
        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg="white")
        lbl_name.place(relx=.05,rely=.1)

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.15,rely=.1)
        e_name.focus()

        lbl_email=Label(ifrm,text="Email",font=('arial',20,'bold'),bg="white")
        lbl_email.place(relx=.05,rely=.3)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.15,rely=.3)
        
        lbl_mob=Label(ifrm,text="Mob",font=('arial',20,'bold'),bg="white")
        lbl_mob.place(relx=.5,rely=.1)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.6,rely=.1)
        
        lbl_adhar=Label(ifrm,text="Adhar",font=('arial',20,'bold'),bg="white")
        lbl_adhar.place(relx=.5,rely=.3)

        e_adhar=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_adhar.place(relx=.6,rely=.3)

        create_btn=Button(ifrm,text="create",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=create)
    
        create_btn.place(relx=.4,rely=.5)





    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.70)

    lbl_wel=Label(frm,text="Welcome Admin",font=('arial',20,'bold'),bg="pink")
    lbl_wel.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=logout_click)
    
    logout_btn.place(relx=.9,rely=0)

    open_btn=Button(frm,text="open account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg="green",fg="white",command=open_click)
    
    open_btn.place(relx=.2,rely=.1)

    view_btn=Button(frm,text="view account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg="blue",fg="white",command=view_click)
    
    view_btn.place(relx=.4,rely=.1)

    close_btn=Button(frm,text="close account",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',
                     activeforeground='white',bg="red",fg="white",command=close_click)
    
    close_btn.place(relx=.6,rely=.1)

def customer_screen(cname,acn):
    def logout_click():
        frm.destroy()
        main_screen()

    def details_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.22,rely=.22,relwidth=.7,relheight=.6)
        lbl_title=Label(ifrm,text="This is details section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack() 

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()
        info=f'''Account No = {tup[0]}

Account open date = {tup[7]}

Account Bal = {tup[6]}

Account Adhar = {tup[5]}

Account Email = {tup[3]}
'''
        lbl_info=Label(ifrm,text=info,bg='white',font=('verdana',15,'bold'),)
        lbl_info.place(relx=.2,rely=.1)        

    def edit_click():
        def update():
            uname=e_name.get()
            upass=e_pass.get()
            uemail=e_email.get()
            umob=e_mob.get()

            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="update accounts set name=?,pass=?,email=?,mob=? where acn=?"
            curobj.execute(query,(uname,upass,uemail,umob,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Edit","Record updated")
            

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.22,relwidth=.7,relheight=.6)
        
        lbl_title=Label(ifrm,text="This is edit details section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack() 


        lbl_name=Label(ifrm,text="Name",font=('arial',20,'bold'),bg="white")
        lbl_name.place(relx=.05,rely=.1)

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.15,rely=.1)
        e_name.focus()  

        lbl_email=Label(ifrm,text="Email",font=('arial',20,'bold'),bg="white")
        lbl_email.place(relx=.05,rely=.3)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.15,rely=.3)
        
        lbl_mob=Label(ifrm,text="Mob",font=('arial',20,'bold'),bg="white")
        lbl_mob.place(relx=.5,rely=.1)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.6,rely=.1)
        
        lbl_pass=Label(ifrm,text="Pass",font=('arial',20,'bold'),bg="white")
        lbl_pass.place(relx=.5,rely=.3)

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=.6,rely=.3)
        

        update_btn=Button(ifrm,text="update",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=update)
    
        update_btn.place(relx=.4,rely=.5)

        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select name,pass,email,mob from accounts where acn=?"
        curobj.execute(query,(acn,))
        tup=curobj.fetchone()
        conobj.close()

        e_name.insert(0,tup[0])
        e_pass.insert(0,tup[1])
        e_email.insert(0,tup[2])
        e_mob.insert(0,tup[3])

    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.22,rely=.22,relwidth=.7,relheight=.6)
        
        lbl_title=Label(ifrm,text="This is deposit section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack() 

        amt=simpledialog.askfloat("","Amount")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="update accounts set bal=bal+? where acn=?"
        curobj.execute(query,(amt,acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Deposit",f"{amt} deposited")

    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.22,rely=.22,relwidth=.7,relheight=.6)
        
        lbl_title=Label(ifrm,text="This is withdraw section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack() 

        amt=simpledialog.askfloat("","Amount")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select bal from accounts where acn=?"
        curobj.execute(query,(acn,))
        bal=curobj.fetchone()[0]
        conobj.close()
        if bal>=amt:
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="update accounts set bal=bal-? where acn=?"
            curobj.execute(query,(amt,acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Withdraw",f"{amt} withdrawn")
        else:
             messagebox.showerror("Withdraw",f"Insufficient bal {bal}")

    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.22,rely=.22,relwidth=.7,relheight=.6)
        
        lbl_title=Label(ifrm,text="This is transfer section",font=('arial',20,'bold'),
                        bg="white",fg='purple')
        lbl_title.pack() 

        toacn=simpledialog.askinteger("","To ACN")
        conobj=sqlite3.connect(database='bank.sqlite3')
        curobj=conobj.cursor()
        query="select * from accounts where acn=?"
        curobj.execute(query,(toacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup!=None:
            amt=simpledialog.askfloat("","Amount")
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="select bal from accounts where acn=?"
            curobj.execute(query,(acn,))
            bal=curobj.fetchone()[0]
            conobj.close()
            if bal>=amt:
                conobj=sqlite3.connect(database='bank.sqlite3')
                curobj=conobj.cursor()
                query1="update accounts set bal=bal-? where acn=?"
                query2="update accounts set bal=bal+? where acn=?"
                
                curobj.execute(query1,(amt,acn))
                curobj.execute(query2,(amt,toacn))
                
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt} transfered to {toacn} ACN")
            else:
                messagebox.showerror("Withdraw",f"Insufficient bal {bal}") 
        else:
            messagebox.showerror("Transfer",f"To ACN does not exist")


    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.70)

    lbl_wel=Label(frm,text=f"Welcome,{cname}",font=('arial',20,'bold'),bg="pink")
    lbl_wel.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=logout_click)
    
    logout_btn.place(relx=.9,rely=0)

    details_btn=Button(frm,text="view details",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg="blue",fg="white",command=details_click)
    
    details_btn.place(relx=0,rely=.1)

    edit_btn=Button(frm,text="edit details",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg="powder blue",command=edit_click)
    
    edit_btn.place(relx=0,rely=.25)

    deposit_btn=Button(frm,text="deposit",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg="green",fg="white",command=deposit_click)
    
    deposit_btn.place(relx=0,rely=.4)

    withdraw_btn=Button(frm,text="withdraw",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg="red",fg="white",command=withdraw_click)
    
    withdraw_btn.place(relx=0,rely=.55)

    transfer_btn=Button(frm,text="transfer",font=('arial',20,'bold'),
                     bd=5,activebackground='purple',width=15,
                     activeforeground='white',bg="red",fg="white",command=transfer_click)
    
    transfer_btn.place(relx=0,rely=.7)




def main_screen():
    def forgot_click():
        frm.destroy()
        forgot_screen()

    def login_click():
        user=combo_user.get()
        uacn=e_acn.get()
        upass=e_pass.get()
        if user=="Admin" and uacn=="0" and upass=="Admin":
            frm.destroy()
            admin_screen()
        elif user=="Customer":
            conobj=sqlite3.connect(database='bank.sqlite3')
            curobj=conobj.cursor()
            query="select * from accounts where acn=? and pass=?"
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Login","Invalid Credentials")
            else:
                frm.destroy()
                customer_screen(tup[1],tup[0])
        else:
             messagebox.showerror("Login","Invalid User")


    

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.70)

    lbl_acn=Label(frm,text="ACN",font=('arial',20,'bold'),bg="pink")
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()

    lbl_pass=Label(frm,text="PASS",font=('arial',20,'bold'),bg="pink")
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.4,rely=.2)

    lbl_user=Label(frm,text="User",font=('arial',20,'bold'),bg="pink")
    lbl_user.place(relx=.3,rely=.3)

    combo_user=Combobox(frm,values=['---select---','Admin','Customer'],font=('arial',20,'bold'))
    combo_user.current(0)
    combo_user.place(relx=.4,rely=.3)

    login_btn=Button(frm,text="login",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=login_click)
    
    login_btn.place(relx=.42,rely=.4)

    reset_btn=Button(frm,text="reset",font=('arial',20,'bold'),
                     bd=5,bg='powder blue',activebackground='purple',activeforeground='white')
    reset_btn.place(relx=.52,rely=.4)

    forgot_btn=Button(frm,text="forgot password",font=('arial',20,'bold'),width=18,
                     bd=5,bg='powder blue',activebackground='purple',
                     activeforeground='white',command=forgot_click)
    forgot_btn.place(relx=.4,rely=.57)


root=Tk()               #create root window
root.state("zoomed")    #make window fullscreen
root.config(bg="powder blue") #set bgcolor 0f wundow
root.resizable(width=False,height=False)

lbl_title=Label(root,text="Banking Simulation",font=('arial',50,'bold','underline'),bg="powder blue")
lbl_title.pack()

lbl_date=Label(root,text=time.strftime("%A,%d-%b-%Y ⏰%r"),fg='blue',font=('arial',18,'bold'),bg="powder blue")
lbl_date.pack()

img=Image.open("logo.jpg").resize((250,150))
tkimg=ImageTk.PhotoImage(img,master=root)
lbl_logo=Label(root,image=tkimg)
lbl_logo.place(relx=0,rely=0)

lbl_footer=Label(root,text="Developed by\n Ducat WE 3 PM Batch",fg='blue',font=('arial',18,'bold'),bg="powder blue")
lbl_footer.pack(side='bottom',pady=10)

update_time()
main_screen()
root.mainloop() #make the window visible