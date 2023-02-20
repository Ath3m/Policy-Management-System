
#### GENERAL IMPORTS#####
import datetime
from tkinter import *
from tkinter import messagebox, Label
from tkinter import ttk
from tkcalendar import *
from datetime import date
import mysql.connector
import tkinter as tk

##### IMPORT LIBRARY FOR RANDOM POL GENERATOR#
import random
#### TREEVIEW LIBRARY ####
from sqlalchemy import create_engine

#### payment library###
import requests

## EMAIL notification packages
import smtplib,ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd

#### GENERATE PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages

### REPORT LIBRARY
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt




#### DEF MAIN ROOT ####
def main():
    root=Tk()
    app=Window1(root)
    root.mainloop()


def db_create():## FUNCTION TO CHECK DB_COUNTER DATABASE
    con = mysql.connector.connect(host="localhost", user="root", password="", database='db_counter')
    cur = con.cursor()
    sql = "SELECT counter FROM tbl_db_counter"
    cur.execute(sql)  ### AFTER EXTRACT FROM DB TO BE ASSIGN TO A LIST FOR CONDITION
    db_counter_get = cur.fetchall()
    # print(db_counter_get)
    for x in db_counter_get:
        # print(x[0])
        flag=x[0]
        if flag=="False": ## IF DB COUNTER == FALSE CREATE practicedb
                        ###else: skip db creation
            con = mysql.connector.connect(host="localhost", user="root", password="", database='db_counter')
            cur = con.cursor()
            cur.execute("create database practicedb;")
            con.commit()
            con.close()
           #####
            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
            cur = con.cursor()
            cur.execute("create table tbl_employee(EMP_ID INT AUTO_INCREMENT PRIMARY KEY,EMP_NUM INT,firstname varchar(15),lastname varchar(15))")
            cur.execute("create table tbl_useraccount(ADMIN_ID INT AUTO_INCREMENT PRIMARY KEY,EMP_NUM VARCHAR(10),USER_NAME VARCHAR(10),USER_PASSWORD VARCHAR(10))")
            cur.execute("create table tbl_policy(POLICY_ID int AUTO_INCREMENT PRIMARY KEY,POLICY_NUM INT,POLICY_STATUS VARCHAR(15),REG_DATE DATE,START_DATE DATE,END_DATE DATE,PRODUCT_NAME VARCHAR(45),INS_TYPE VARCHAR(50),PRODUCT_DURATION VARCHAR(20),COVERAGE_AMOUNT INT,MODE VARCHAR(10),FREQUENCY VARCHAR(10),PAYMENT_DURATION VARCHAR (10),PAYMENT_TOTAL VARCHAR(10))")
            cur.execute("create table tbl_po(PO_ID int,firstname varchar(45),middlename varchar(30),lastname varchar (30),age varchar (3),birthday date,gender varchar(10),profession varchar(20),civilstatus varchar(10),FOREIGN KEY (`PO_ID`) REFERENCES `tbl_policy`(`POLICY_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_insured(INS_ID int,firstname varchar(45),middlename varchar(30),lastname varchar (30),age varchar (3),birthday date,gender varchar(10),profession varchar(20),civilstatus varchar(10),FOREIGN KEY (`INS_ID`) REFERENCES `tbl_policy`(`POLICY_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_bene(BENE_ID INT AUTO_INCREMENT PRIMARY KEY,firstname varchar(45),middlename varchar(30),lastname varchar (30),age varchar(3),birthday date,gender varchar(10),relationship varchar(10),benefit_percentage int,BENE_POLICY_ID int,FOREIGN KEY (`BENE_POLICY_ID`) REFERENCES `tbl_policy`(`POLICY_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_rider(RIDER_ID INT AUTO_INCREMENT PRIMARY KEY,RIDER VARCHAR(40),RIDER_STATUS VARCHAR(15),RIDER_REG_DATE VARCHAR(20),RIDER_STARTDATE VARCHAR (20),RIDER_DURATION VARCHAR(10),RIDER_END_DATE VARCHAR(20),RIDER_COVERAGE INT,RIDER_ID_FK INT,FOREIGN KEY (`RIDER_ID_FK`) REFERENCES `tbl_policy`(`POLICY_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create TABLE tbl_payment(PAYMENT_ID INT AUTO_INCREMENT PRIMARY KEY,POLICY_NUM INT,PAY_STARTDATE DATE,DUE_DATE DATE,FULLNAME VARCHAR(40),EMAIL VARCHAR (30),ADDRESS VARCHAR(150),PROVINCECITY VARCHAR(30),ZIPCODE VARCHAR(4),CARDNAME VARCHAR(20),CARDNUM VARCHAR(16),EXPMONTH VARCHAR(10),EXPYEAR VARCHAR(10),CVV VARCHAR(3),amount int,MONTHS_PAID VARCHAR(10),PAYMENT_REMAINING VARCHAR(10),PAYMENT_ID_FK INT,FOREIGN KEY (`PAYMENT_ID_FK`) REFERENCES `tbl_policy`(`POLICY_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_contact_po(CONTACT_ID_PO INT AUTO_INCREMENT PRIMARY KEY,MOBILE VARCHAR(11),LANDLINE VARCHAR(8),EMAIL VARCHAR(35),CONTACT_TYPE VARCHAR(10),CONTACT_FK_PO INT,FOREIGN KEY (`CONTACT_FK_PO`) REFERENCES `tbl_po`(`PO_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_contact_ins(CONTACT_ID_INS INT AUTO_INCREMENT PRIMARY KEY,MOBILE VARCHAR(11),LANDLINE VARCHAR(8),EMAIL VARCHAR(35),CONTACT_TYPE VARCHAR(10),CONTACT_FK_INS INT,FOREIGN KEY (`CONTACT_FK_INS`) REFERENCES `tbl_insured`(`INS_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbl_contact_bene(CONTACT_ID_BENE INT AUTO_INCREMENT PRIMARY KEY,MOBILE VARCHAR(11),LANDLINE VARCHAR(8),EMAIL VARCHAR(35),CONTACT_TYPE VARCHAR(10),FOREIGN KEY (`CONTACT_ID_BENE`) REFERENCES `tbl_bene`(`BENE_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbladdress_po(ADDRESS_ID INT AUTO_INCREMENT PRIMARY KEY,address varchar(45),city varchar(20),province varchar(15),zipcode varchar(4),country varchar(2),type varchar(10),PO_ADDRESS_ID int,FOREIGN KEY (`PO_ADDRESS_ID`) REFERENCES tbl_po(`PO_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbladdress_ins(ADDRESS_ID INT AUTO_INCREMENT PRIMARY KEY,address varchar(45),city varchar(20),province varchar(15),zipcode varchar(4),country varchar(2),type varchar(10),INS_ADDRESS_ID int,FOREIGN KEY (`INS_ADDRESS_ID`) REFERENCES tbl_insured(`INS_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            cur.execute("create table tbladdress_bene(ADDRESS_ID INT AUTO_INCREMENT PRIMARY KEY,address varchar(45),city varchar(20),province varchar(15),zipcode varchar(4),country varchar(2),type varchar(10),FOREIGN KEY (`ADDRESS_ID`) REFERENCES tbl_bene(`BENE_ID`) ON DELETE CASCADE ON UPDATE CASCADE);")
            con.commit()
            con.close()
            #### After DB creation update counter from tbl_db_counter =TRUE
            con = mysql.connector.connect(host="localhost", user="root", password="", database='db_counter')
            cur = con.cursor()
            updatesql="update tbl_db_counter set counter='True'"
            cur.execute(updatesql)
            con.commit()
            con.close()
        else:
            print("database already created!")
db_create()


############## SIGN IN #############
class Window1:
    def __init__(self, master):
        self.master=master
        self.master.title("Sign in")
        self.master.geometry("925x600+300+300")
        self.master.config(bg="#008631")
        self.master.resizable(False, False)
        self.frame=Frame(self.master,width=350,height=350,bg="#008631")
        self.frame.place(x=480,y=70)


        # ##TEMPO###
        # def new_window():
        #     self.master.withdraw()
        #     self.inputpolicy = Toplevel(self.master)
        #     self.app = MainWIndow(self.inputpolicy)


        ######################## LOGIN AUTHENTICATION ######################################
        def register():
            self.master.withdraw()
            self.inputpolicy = Toplevel(self.master)
            self.app = RegistrationTab(self.inputpolicy)


        def new_window():
            # global self.uname,self.pw
            uname = self.user_entry.get()
            pw = self.pw_entry.get()

            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
            cur = con.cursor()

            sql = "SELECT * from tbl_useraccount where USER_NAME= %s and USER_PASSWORD=%s"
            cur.execute(sql,[(uname),(pw)])  ### AFTER EXTRACT FROM DB AND I AUTOMATICALLY ASSIGN IT TO A LIST FOR CONDITION
            records = cur.fetchall()

            if uname == "Username" or pw == "Password":
                messagebox.showerror("Error", "Some fields are missing!!")

            elif records:
                self.master.withdraw()
                self.inputpolicy = Toplevel(self.master)
                self.app = MainWIndow(self.inputpolicy)

            else:
                messagebox.showerror(title="Error", message="Username or Password is incorrect!!")


        def exit():
            if messagebox.askokcancel(" ", message="Confirm Exit?"):
                self.master.destroy()


        #### KEY EVENTS FOR PLACEHOLDER USERNAME####

        def on_enter_uname(e):
            self.user_entry.delete(0, 'end')

        def on_leave_uname(e):
            name = self.user_entry.get()
            if name == "":
                self.user_entry.insert(0, 'Username')


        self.user_entry=Entry(self.frame,width=25,fg='white',border=0,bg='#008631',font=('Microsoft YaHei UI Light',11))
        self.user_entry.place(x=30,y=80)
        self.user_entry.insert(0,'Username')

        self.user_entry.bind('<FocusIn>', on_enter_uname)
        self.user_entry.bind('<FocusOut>', on_leave_uname)

        Frame(self.frame,width=300, height=2, bg='white').place(x=27, y=107)

        #### KEY EVENTS FOR PLACEHOLDER PASSWORD####
        def on_enter_pw(e):
            password = False
            self.pw_entry.delete(0, 'end')
            if password == False:
                self.pw_entry.config(show="*")

        def on_leave_pw(e):
            password = self.pw_entry.get()
            if password == "":
                self.pw_entry.insert(0, 'Password')
                self.pw_entry.config(show="", font=('Microsoft YaHei UI Light', 11))

        ##################################### SIGN IN ENTRY AND PW ENTRY #############################################################################
        self.registration_label = Label(self.frame, text='Sign in', fg='white', bg='#008631',font=('Microsoft YaHei UI Light', 23, 'bold'))
        self.registration_label.place(x=140, y=5)

        self.pw_entry = Entry(self.frame, width=25, fg='white', border=0, bg='#008631',font=('Microsoft YaHei UI Light', 11))
        self.pw_entry.place(x=30, y=150)
        self.pw_entry.insert(0, 'Password')
        self.pw_entry.bind('<FocusIn>', on_enter_pw)
        self.pw_entry.bind('<FocusOut>', on_leave_pw)

        Frame(self.frame, width=300, height=2, bg='white').place(x=27, y=177)
        Button(self.frame, width=15, pady=7, text="Sign in", bg='white', fg='black', border=0,command=new_window).place(x=35, y=204)
        Button(self.frame,width=15, pady=7, text="Exit", bg='white', fg='black', border=0,command=exit).place(x=158, y=204)

        label1 = Label(self.frame, text="New User?", fg='white', bg='#008631',font=('Microsoft YaHei UI Light', 9))
        label1.place(x=135, y=250)

        register_button = Button(self.frame, width=12, text='Register here', border=0, bg='#008631', cursor='hand2',fg='white',command=register)
        register_button.place(x=209, y=250)
        Frame(self.frame, width=70, height=2, bg='white').place(x=220, y=270)

        label2 = Label(self.frame, text="Having trouble Signing in ?", fg='white', bg='#008631',font=('Microsoft YaHei UI Light', 9))
        label2.place(x=53, y=280)

        pwreset = Button(self.frame, width=12, text='Password Reset', border=0, bg='#008631', cursor='hand2', fg='white')
        pwreset.place(x=209, y=280)
        Frame(self.frame, width=80, height=2, bg='white').place(x=214, y=300)


######## REGISTER TAB #########
class RegistrationTab:
    def __init__(self, master):
        self.master=master
        self.master.title("Register")
        self.master.geometry("400x400")
        self.master.config(bg="#008631")
        self.master.resizable(False, False)

        emp_var = StringVar()
        uname_var=StringVar()
        pw_var=StringVar()

        def Register():
            emp_num=emp_var.get()
            uname=uname_var.get()
            pw=pw_var.get()
            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
            cur = con.cursor()
            sql = "SELECT EMP_NUM FROM tbl_employee where EMP_NUM=%s"
            cur.execute(sql,[(emp_num)])  ### AFTER EXTRACT FROM DB TO BE ASSIGN TO A LIST FOR CONDITION
            records = cur.fetchall()
            sql1 = "SELECT EMP_NUM FROM tbl_useraccount where EMP_NUM=%s"
            cur.execute(sql1,[(emp_num)])
            useraccount=cur.fetchall()

            if records:
                if not useraccount or useraccount[0][0] != emp_num:
                    con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                    cur = con.cursor()
                    sql2 = "INSERT INTO tbl_useraccount(`EMP_NUM`,USER_NAME,USER_PASSWORD) VALUES ('" + str(
                        emp_num) + "','" + uname + "','" + pw + "')"
                    cur.execute(sql2)
                    con.commit()
                    con.close()
                    if messagebox.askokcancel("Registration Successful", "Proceed to Login?"):
                        self.master.withdraw()
                        self.inputpolicy = Toplevel(self.master)
                        self.app = Window1(self.inputpolicy)
                    else:
                        clear()
                else:
                    messagebox.showerror("", "Employee already registered!")
                    clear()
            else:
                messagebox.showerror("ERROR", "Employee Number not exist")
                clear()

        def clear():
            self.Empnum_entry.delete(0, END)
            self.Username_entry.delete(0,END)
            self.Password_entry.delete(0,END)

        def Exit():
            if messagebox.askokcancel("","Proceed to Exit?"):
                self.master.withdraw()
                self.inputpolicy = Toplevel(self.master)
                self.app = Window1(self.inputpolicy)
            else:
                pass



        self.mainframe=Frame(master,width=380,height=380,bg="#008631")
        self.mainframe.place(x=10,y=10)

        self.Username_label = Label(self.mainframe, text="Register your account", font=('Microsoft YaHei UI Light', 21, "bold"),bg="#008631", fg="white")
        self.Username_label.place(x=20, y=5)


        self.Empnum_label = Label(self.mainframe, text="Employee #:",font=('Microsoft YaHei UI Light', 11, "bold"), bg="#008631", fg="white")
        self.Empnum_label.place(x=75, y=55)
        self.Empnum_entry=Entry(self.mainframe, width=30, textvariable=emp_var)
        self.Empnum_entry.place(x=77, y=85)

        self.Username_label = Label(self.mainframe, text="UserName:", font=('Microsoft YaHei UI Light', 11, "bold"),bg="#008631", fg="white")
        self.Username_label.place(x=75, y=105)
        self.Username_entry = Entry(self.mainframe, width=30, textvariable=uname_var)
        self.Username_entry.place(x=77, y=135)

        self.Password_label = Label(self.mainframe, text="Password:", font=('Microsoft YaHei UI Light', 11, "bold"),bg="#008631", fg="white")
        self.Password_label.place(x=75,y=155)
        self.Password_entry = Entry(self.mainframe, width=30, textvariable=pw_var)
        self.Password_entry.place(x=77, y=185)
        self.Password_entry.config(show="*")


        self.Register_Button = Button(self.mainframe, text="Register", border=0, bg="#0bb839", fg="white", padx=10,pady=5, compound='left', font=('Microsoft YaHei UI Light', "8", "bold"),activebackground="#10752b", command=Register)
        self.Register_Button.place(x=70, y=230)

        self.Register_Button = Button(self.mainframe, text="Exit", border=0, bg="#d15036", fg="white", padx=23,pady=5, compound='left', font=('Microsoft YaHei UI Light', "8", "bold"),activebackground="#ad2307", command=Exit)
        self.Register_Button.place(x=150, y=230)



######## NEW ACCOUNTS / MANAGE ACCOUNTS ################

class MainWIndow:
    def __init__(self,master1):
        # self.window1=window1
        self.menu=master1
        self.menu.title("Menu")
        self.menu.geometry("1100x650")
        self.menu.config(bg='#008631')
        self.menu.resizable(False, False)


        def signout():
            if messagebox.askyesno("","Confirm Sign-Out?"):
                self.menu.withdraw()
                self.inputpolicy = Toplevel(self.menu)
                self.app = Window1(self.inputpolicy)
            else:
                pass


        def new_account():
            self.menu.withdraw()
            self.inputpolicy = Toplevel(self.menu)
            self.app = Policy_input(self.inputpolicy)

        def manage_account():
            self.menu.withdraw()
            self.inputpolicy = Toplevel(self.menu)
            self.app = Policy_view_main_admin(self.inputpolicy)

        def reports():
            self.menu.withdraw()
            self.inputpolicy = Toplevel(self.menu)
            self.app = Reports(self.inputpolicy)

        #########################QUERIES for Counter########################
        global active,pending,cancelled

        def extractacounter():
            active=0
            pending=0
            cancelled=0

            con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
            cur = con.cursor()
            sql = "SELECT POLICY_STATUS from tbl_policy"
            cur.execute(sql)
            records = cur.fetchall()
            for x in records:
                if x[0] =='ACTIVE'or x[0]=='FULLY-PAID':
                    active=active+1
                    totalactive_label.config(text=str(active))
                elif x[0]=='PENDING':
                    pending=pending+1
                    totalpending_label.config(text=str(pending))
                elif x[0]=='CANCELLED':
                    cancelled=cancelled+1
                    totalcancelled_label.config(text=str(cancelled))

        ############## Frames and Widgets and Treeview##############

        self.frame = LabelFrame(self.menu, width=1070, height=630, bg='#008631')
        self.frame.place(x=10, y=10)
        self.trvframe = LabelFrame(self.frame, width=700, height=300, bg='#04820e',border=0)
        self.trvframe.place(x=350, y=40)
        self.counterframe = LabelFrame(self.frame, width=632, height=300, bg='#04820e', border=1)
        self.counterframe.place(x=350, y=280)

        ############TREEVIEW POLICY Number, STATUS REGDATE, ENDDATE##############
        my_conn = create_engine("mysql+mysqldb://root:""@localhost/practicedb")
        # Using treeview widget
        self.trv = ttk.Treeview(self.trvframe)
        self.trv.grid(row=0, column=0,padx=83,pady=5)

        # number of columns
        self.trv["columns"] = ("1", "2", "3", "4")

        # Defining heading
        self.trv['show'] = 'headings'

        # width of columns and alignment
        self.trv.column("1", width=100, anchor='c')
        self.trv.column("2", width=150, anchor='c')
        self.trv.column("3", width=100, anchor='c')
        self.trv.column("4", width=100, anchor='c')

        # Headings
        # respective columns
        self.trv.heading("1", text="Policy Number")
        self.trv.heading("2", text="Policy Status")
        self.trv.heading("3", text="Registration Date")
        self.trv.heading("4", text="Expiration Date")

        # getting data from tbl_policy table
        r_set = my_conn.execute("SELECT tbl_policy.POLICY_ID, tbl_policy.POLICY_NUM, tbl_policy.POLICY_STATUS, tbl_policy.REG_DATE,tbl_policy.END_DATE FROM tbl_policy")

        self.trv.tag_configure('active', background='lightgreen')
        self.trv.tag_configure('pending', background='#f7e928')
        self.trv.tag_configure('cancelled', background='#e05536')
        self.trv.tag_configure('fullpaid', background='#73c0d1')
        self.trv.tag_configure('deathclaim', background='#c5c6c7')

        my_tag = ""
        for x in r_set:
            if x[2] == "ACTIVE":
                my_tag = 'active'
            elif x[2] == 'PENDING':
                my_tag = 'pending'
            elif x[2] == 'FULLY-PAID':
                my_tag = 'fullpaid'
            else:
                my_tag = 'cancelled'
            self.trv.insert("", 'end', id=x[0], text=x[0],values=(x[1], x[2], x[3], x[4]),tags=my_tag)

        scrollbar=ttk.Scrollbar(self.trvframe,orient='vertical',command=self.trv.yview)
        self.trv.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0,column=1,sticky='ns')

        ####################### COUNTER FRAMES AND WIDGETS#######################
        self.counteractive_frame = LabelFrame(self.frame, width=250, height=250, bg='#04820e', border=0)
        self.counteractive_frame.place(x=360, y=300)
        self.counterpending_frame = LabelFrame(self.frame, width=250, height=250, bg='#04820e', border=0)
        self.counterpending_frame.place(x=585, y=300)
        self.countercancelled_frame = LabelFrame(self.frame, width=250, height=250, bg='#04820e', border=0)
        self.countercancelled_frame.place(x=810, y=300)

        totalactive_label=Label(self.counteractive_frame,text="0" ,font=('Microsoft YaHei UI Light',70,"bold"),bg="#04820e",fg="white")
        totalactive_label.grid(row=0,column=0)
        active_counterlabel = Label(self.counteractive_frame, text="Total\nActive Policies", bg="#04820e", fg='white',font=('Microsoft YaHei UI Light', 12, "bold"))
        active_counterlabel.grid(row=1, column=0)

        totalpending_label = Label(self.counterpending_frame , text="0", font=('Microsoft YaHei UI Light',70,"bold"),bg="#04820e",fg="#f7e928")
        totalpending_label.grid(row=0,column=0)
        pending_counterlabel = Label(self.counterpending_frame , text="Total\nPending Policies", bg="#04820e", fg='#f7e928',font=('Microsoft YaHei UI Light', 12, "bold"))
        pending_counterlabel.grid(row=1, column=0)

        totalcancelled_label = Label(self.countercancelled_frame, text="0", font=('Microsoft YaHei UI Light',70,"bold"),bg="#04820e",fg="#e82525")
        totalcancelled_label.grid(row=0,column=0)
        cancelled_counterlabel = Label(self.countercancelled_frame,text="Total\nCancelled Policies", bg="#04820e", fg='#870303',font=('Microsoft YaHei UI Light', 12, "bold"))
        cancelled_counterlabel.grid(row=1,column=0)

        footer_label = Label(self.counterframe, text="Policy Statistics", font=('Microsoft YaHei UI Light', 20, "bold"),bg="#04820e", fg="white")
        footer_label.place(x=200, y=230)

        ################################# BUTTONS######################################
        newaccount_Button=Button(self.frame,text="New Policy",border=1,bg="#b0a507",fg="white" ,padx=67,pady=15, font=('Microsoft YaHei UI Light',"11","bold"),activebackground="white",command=new_account)
        newaccount_Button.place(x=110,y=50)

        manageaccount_Button = Button(self.frame, text="Manage Accounts", border=1,bg="#b0a507",fg="white",padx=40,pady=15, compound='left', font=('Microsoft YaHei UI Light', "11", "bold"),activebackground="white", command=manage_account)
        manageaccount_Button.place(x=110, y=130)

        reports_Button = Button(self.frame, text="Reports", border=1,bg="#b0a507",fg="white",padx=79,pady=15,compound='left', font=('Microsoft YaHei UI Light', "11", "bold"),activebackground="white", command=reports)
        reports_Button.place(x=110, y=210)

        signout_Button = Button(self.frame, text="Sign Out", border=0, bg="#008631", fg="white", padx=5, pady=5, font=('Microsoft YaHei UI Light', "8", "bold"),activebackground="white", command=signout)
        signout_Button.place(x=30, y=590)
        extractacounter()


#################################################################################################################################################################################################

class Policy_input:
    ###Policy _input class####
    def __init__(self, master6):
        self.master6 = master6
        self.master6.title("C.A.M.S v1.2022 - Policy Input")
        self.master6.geometry("1000x680")
        self.master6.config(bg='#008631')
        self.master6.resizable(False,False)

        ###########Product Name selection via product Type###############
        getpolicy_type = StringVar()
        getproduct_name = StringVar()


        def input_policy_query():
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()
            sql = "INSERT INTO tbl_policy(`POLICY_ID`,POLICY_NUM,POLICY_STATUS,REG_DATE,START_DATE,END_DATE,PRODUCT_NAME,INS_TYPE,PRODUCT_DURATION,COVERAGE_AMOUNT)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (POLICY_ID,POLICY_NUM,POLICY_STATUS,REG_DATE,START_DATE, End_date, Product_Name,INS_TYPE ,duration, Coverage_Amount)
            cur.execute(sql,val)
            con.commit()
            con.close()


        def input_rider_query():
            ##### INITIATE SELECT * to tbl_policy to extract POLICY_ID ####
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()
            sql="Select POLICY_ID FROM tbl_policy"
            cur.execute(sql)
            indexes=cur.fetchall() #### fetch the policy id result is in tuple format
            indexes.reverse()  ### reversed the fetch result to get the last index
            x=indexes[0]   ### variable x is not holding the last tuple index
            items=list(x)  ### convert tuple to list to extract as normal integer
            index=items[0] ## finally assign last value of the list from the converted tuple assign to variable (index) then run INSERT query

            ### tbl_rider has a foreign key RIDER_ID which gives error 1452 foreign key failure. (to avoid this run this:to tbl_rider table "SET GLOBAL FOREIGN_KEY_CHECKS=0")
            ### this disables foreign key checks however we need to perform JOIN to access the parent table index.
            sql1 = "INSERT INTO tbl_rider (RIDER_ID,RIDER,RIDER_STATUS,RIDER_DURATION,RIDER_REG_DATE,RIDER_STARTDATE,RIDER_END_DATE,RIDER_COVERAGE,RIDER_ID_FK) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (Rider_ID,Rider,Rider_status,Rider_duration,Rider_reg_date,Rider_startdate,Rider_end_date,Ridercoverage,index)
            cur.execute(sql1, val)
            con.commit()
            messagebox.showinfo("", "Rider added successfully!")
            con.rollback()
            con.close()

        def clear():
            policy_type_combobox.set("Type")
            getproduct_name.set("Product Name")
            benefitterm_display.config(text="Duration")
            Policy_regdate_date.config(text="")
            Policy_end_date.config(text="")
            ECI_coverage_entry.delete(0, END)
            coverageamount_entry.delete(0,END)
            ADB.set("No")
            TDW.set("No")
            ECI.set("No")
            HIB.set("No")
            TLB.set("No")

        ##### SUBMIT FORM WITH SELECTED POLICY AND RIDERS#####
        def submit_policyinput():
            # # ####TEMPORARY ACCESS### REMOVE AAFFTER####
            # self.master6.withdraw()
            # self.inputpolicyinsured = Toplevel(self.master6)
            # self.app = policyowner_register(self.inputpolicyinsured)
        ####################################

            global POLICY_ID,POLICY_NUM,POLICY_STATUS,REG_DATE,START_DATE,End_date,Product_Name,duration,Coverage_Amount,INS_TYPE,\
                Rider_ID,Rider,Rider_duration,Rider_reg_date,Rider_startdate,Rider_end_date,Rider_status,Ridercoverage,Rider_fk,ADB_value,TDW_value,ECI_value,HIB_value,TLB_value,ECI_VAL
            try:
                POLICY_ID=0
                POLICY_NUM=get_policynumber()
                POLICY_STATUS=get_policystatus()
                INS_TYPE=getpolicy_type.get()
                REG_DATE=REG_DATE
                START_DATE=REG_DATE
                End_date=End_date
                duration=duration
                Product_Name = getproduct_name.get()
                Coverage_Amount = coverageamount_limit_fuction()


                Rider_ID = 0
                Rider = ""
                Rider_reg_date=REG_DATE
                Rider_startdate=REG_DATE
                Rider_end_date=Rider_end_date
                Rider_status=get_policystatus()
                Ridercoverage = 0
                Rider_duration=duration
                ADB_value=ADB.get()
                TDW_value=TDW.get()
                ECI_value = ECI.get()
                HIB_value = HIB.get()
                TLB_value = TLB.get()
                ECI_VAL=ECI_GETVALUE()
                self.getpolicy_type = getpolicy_type.get()


                if Product_Name=="Traditional Plan Products" or Product_Name=="Insurance with Investment Products":
                    messagebox.showerror("","No Product Selected")
                else:
                    if Coverage_Amount >= 300000 and ECI_value=="No":
                        input_policy_query()
                        if ADB_value=="Accidental Death Benefit":
                            Rider=ADB_value
                            Ridercoverage=Coverage_Amount
                            input_rider_query()

                        if TDW_value=="Total Disability Waiver":
                            Rider = TDW_value
                            Ridercoverage = 0
                            input_rider_query()

                        if HIB_value=="Hospital Income Benefit":
                            Rider = HIB_value
                            Ridercoverage = 0
                            input_rider_query()

                        if TLB_value=="Term Life Benefit":
                            Rider = TLB_value
                            Ridercoverage = 0
                            input_rider_query()

                        #### ONCE INSERT RIDER DONE ROUTE TO POLICY OUT AND PAYMENT###
                        self.master6.withdraw()
                        self.inputpolicyinsured = Toplevel(self.master6)
                        self.app =policyowner_register (self.inputpolicyinsured)

                    elif Coverage_Amount >= 300000 and ECI_value=="Enhance Critical Illness":

                        if ECI_VAL==0 :
                            messagebox.showerror("", "ECI Coverage cannot be NULL")
                        elif ECI_VAL > eci_limiter:
                            messagebox.showerror("", "ECI Coverage amount cannot be above limit" + " " + str(eci_limiter))
                        else:
                            ### INSERT RIDER IF Coverage_Amount >= 300000 and ECI_value=="Enhance Critical Illness this includes ECI RIDER INPUT##
                            Rider=ECI_value
                            Ridercoverage=ECI_VAL
                            input_policy_query()
                            input_rider_query()

                            if ADB_value == "Accidental Death Benefit":
                                Rider = ADB_value
                                Ridercoverage = Coverage_Amount
                                input_rider_query()

                            if TDW_value == "Total Disability Waiver":
                                Rider = TDW_value
                                Ridercoverage = 0
                                input_rider_query()

                            if HIB_value == "Hospital Income Benefit":
                                Rider = HIB_value
                                Ridercoverage = 0
                                input_rider_query()

                            if TLB_value == "Term Life Benefit":
                                Rider = TLB_value
                                Ridercoverage = 0
                                input_rider_query()

                            #### ONCE INSERT RIDER DONE ROUTE TO POLICY OUT AND PAYMENT###
                            self.master6.withdraw()
                            self.inputpolicyinsured = Toplevel(self.master6)
                            self.app = policyowner_register(self.inputpolicyinsured)
            except:
                messagebox.showerror("","Some fields are missing")



        #### FUNCTION TO GENERATE POLICY NUMBER######
        def get_policynumber():
            ### select all numbers in policy tables to scan policy numbers to avoid and use if else to avoid duplication.
            number = random.randint(1, 9999999)
            return number
        def get_policystatus():
            status=["ACTIVE","PENDING","LAPSED"]
            ##### access payment db to access payment details ###
            ## for now set this to default##
            finalstatus=status[1]
            return finalstatus



        def update_productname(*args):
            for x in master6.grid_slaves(1):
                x.grid_remove()

            if getpolicy_type.get()=="Traditional Life Plan":
                product_name_combobox = ttk.Combobox(self.policy_info_frame, width=70,values=Traditional_Plan,textvariable=getproduct_name)
                product_name_combobox.place(x=120, y=43)
                product_name_combobox.set("Traditional Plan Products")

            elif getpolicy_type.get()=="Insurance with investment Plan":
                product_name_combobox = ttk.Combobox(self.policy_info_frame, width=70,values=Investment_Plan,textvariable=getproduct_name)
                product_name_combobox.place(x=120, y=43)
                product_name_combobox.set("Insurance with Investment Products")
        getpolicy_type.trace("w", update_productname)



        def update_duration(*args):
            global REG_DATE,duration,date_range,End_date,Rider_reg_date,Rider_end_date


            if getproduct_name.get() == "Manu Edge Classic":
                REG_DATE = date.today()
                duration=36500/365
                benefitterm_display.config(text=duration)
                date_range=datetime.timedelta(days=36524)
                End_date = date_range + REG_DATE

                Rider_reg_date = date.today()
                rider_daterange = datetime.timedelta(days=36524)
                Rider_end_date = rider_daterange + Rider_reg_date

                Policy_regdate_date.config(text=str(REG_DATE))
                Policy_end_date.config(text=str(End_date))
                benefitterm_display.config(text=duration)

            elif getproduct_name.get() == "Manu Protect at 65":
                REG_DATE = date.today()
                duration = 23725/365
                benefitterm_display.config(text=duration)
                date_range = datetime.timedelta(days=23740)
                End_date = date_range + REG_DATE
                Rider_reg_date=date.today()
                Rider_end_date=date_range+Rider_reg_date
                Policy_regdate_date.config(text=str(REG_DATE))
                Policy_end_date.config(text=str(End_date))
                benefitterm_display.config(text=duration)

            else:
                REG_DATE = date.today()
                duration = 36500 / 365
                benefitterm_display.config(text=duration)
                date_range = datetime.timedelta(days=36524)
                End_date = date_range + REG_DATE
                rider_daterange = datetime.timedelta(days=36524)
                Rider_reg_date = date.today()
                Rider_end_date =  rider_daterange+Rider_reg_date
                Policy_regdate_date.config(text=str(REG_DATE))
                Policy_end_date.config(text=str(End_date))
                benefitterm_display.config(text=duration)
            return REG_DATE,End_date
        getproduct_name.trace("w", update_duration)


        def coverageamount_limit_fuction():
            global coveragelimiter
            global coverage_amount
            try:
                coveragelimiter = 300000
                plan_coverageamount = coverageamount_entry.get()
                coverage_amount = int(plan_coverageamount)

                if coverage_amount>=coveragelimiter:
                    return coverage_amount

                elif coverage_amount==" " or coverage_amount==0:
                    messagebox.showerror("", "Coverage cannot be NULL")
                    return coverage_amount

                else:
                    messagebox.showerror("","Coverage amount cannot be below minimum PHP300,000")
                    return coverage_amount

            except ValueError:
                messagebox.showerror("", "Coverage Entry is Null")
                coverage_amount = 0
                return coverage_amount



        def ECI_COVERAGEFUNCTION():
            ECI_value = ECI.get()
            if ECI_value == "Enhance Critical Illness":
                ECI_coverage_entry.config(state=NORMAL)
                ECI_GETVALUE()
            elif ECI_value == "No":
                ECI_coverage_entry.delete(0,END)
                ECI_coverage_entry.insert(0,str(0))
                ECI_coverage_entry.config(state=DISABLED)


        def ECI_GETVALUE():
            global ECI_VAL
            global eci_limiter
            try:

                coverage_get=coverage_amount.get()
                coverageamount_get = int(coverage_get)
                eci_limiter = 0.5 * coverageamount_get
                ECI_VAL = float(ECI_amount.get())

                #ECI_VAL = float(ECI_amount.get())
                if ECI_VAL <= eci_limiter:
                    return ECI_VAL

                else:
                    return ECI_VAL
            except ValueError:
                ECI_VAL=0
                return ECI_VAL


        ####### PLAN Type and PLAN NAME######
        policy_typelist = ["Traditional Life Plan", "Insurance with investment Plan"]
        Traditional_Plan = ["Manu Edge Classic", "Manu Protect at 65"]
        Investment_Plan = ["Horizon", "Affluence Builder", "Manu Affluence Elite"]
        coverage_amount=StringVar()

        self.policy_info_frame = LabelFrame(self.master6, text="Policy Information", bg='#008631', fg='white', width=900,height=380)
        self.policy_info_frame.place(x=45, y=20)

        self.policy_dates_frame = LabelFrame(self.master6, text="Policy Dates", bg='#008631', fg='white', width=400,height=230)
        self.policy_dates_frame.place(x=45, y=420)

        product_type=Label(self.policy_info_frame, text="Product Type", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        product_type.place(x=10, y=10)
        policy_type_combobox = ttk.Combobox(self.policy_info_frame, width=35, values=policy_typelist,textvariable=getpolicy_type)
        policy_type_combobox.place(x=115, y=12)
        policy_type_combobox.set("Type")

        product_name_label = Label(self.policy_info_frame, text="Product Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        product_name_label.place(x=10, y=40)

        coverageamount_label = Label(self.policy_info_frame, text="Coverage Amount", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        coverageamount_label.place(x=10, y=70)
        coverageamount_entry = Entry(self.policy_info_frame, width=30,textvariable=coverage_amount)
        coverageamount_entry.place(x=150, y=72)


        #### Rider Selection Part #####
        ### RIDER VARIABLES ###
        ADB = StringVar(value="No")
        TDW = StringVar(value="No")
        ECI = StringVar(value="No")
        TLB = StringVar(value="No")
        HIB = StringVar(value="No")
        ECI_amount = StringVar(value=str(0))


        Rider_name_label = Label(self.policy_info_frame, text="Supplemental Benefits:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,"bold"))
        Rider_name_label.place(x=10, y=100)

        ADB_Checkbutton = Checkbutton(self.policy_info_frame, variable=ADB, bg='#008631',onvalue="Accidental Death Benefit", offvalue="No")
        ADB_Checkbutton.place(x=30, y=130)
        ADB_LABEL = Label(self.policy_info_frame, text="Accidental Death Benefit", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        ADB_LABEL.place(x=50, y=130)

        TDW_Checkbutton=Checkbutton(self.policy_info_frame, variable=TDW, bg='#008631',onvalue="Total Disability Waiver", offvalue="No")
        TDW_Checkbutton.place(x=30, y=160)
        TDW_LABEL = Label(self.policy_info_frame, text="Total Disability Waiver", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        TDW_LABEL.place(x=50, y=160)

        #### ECI COVERAGE INPUT###
        ECI_Checkbutton = Checkbutton(self.policy_info_frame, variable=ECI, bg='#008631',onvalue="Enhance Critical Illness",offvalue="No",command=ECI_COVERAGEFUNCTION)
        ECI_Checkbutton.place(x=30, y=200)
        ECI_Coverage_label = Label(self.policy_info_frame, text="ECI Coverage:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        ECI_Coverage_label.place(x=240, y=200)
        ECI_coverage_entry = Entry(self.policy_info_frame, width=20,textvariable=ECI_amount)
        ECI_coverage_entry.place(x=340, y=200)
        ECI_coverage_entry.config(state=DISABLED)


        HIB_Checkbutton = Checkbutton(self.policy_info_frame, variable=HIB, bg='#008631',onvalue="Hospital Income Benefit", offvalue="No")
        HIB_Checkbutton.place(x=30, y=230)
        TLB_Checkbutton = Checkbutton(self.policy_info_frame, variable=TLB, bg='#008631', onvalue="Term Life Benefit",offvalue="No")
        TLB_Checkbutton.place(x=30, y=260)


        optionalrider1 = Label(self.policy_info_frame, text="Enhance Critical Illness:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        optionalrider1.place(x=50, y=200)
        optionalrider2 = Label(self.policy_info_frame, text="Hospital Income Benefit:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        optionalrider2.place(x=50, y=230)
        optionalrider3 = Label(self.policy_info_frame, text="Term Life Benefit:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11,))
        optionalrider3.place(x=50, y=260)


        ########Policy dates############
        Policy_regdate_label = Label(self.policy_dates_frame, text="Registration Date:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10,))
        Policy_regdate_label.place(x=10, y=10)
        Policy_regdate_date = Label(self.policy_dates_frame,text="",font=('Microsoft YaHei UI Light',10),width=10)
        Policy_regdate_date.place(x=130, y=10)

        Policy_end_label = Label(self.policy_dates_frame, text="End Date:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10,))
        Policy_end_label.place(x=10, y=50)

        Policy_end_date = Label(self.policy_dates_frame, text="",font=('Microsoft YaHei UI Light', 10,), width=10)
        Policy_end_date.place(x=130, y=50)

        benefitterm_label = Label(self.policy_dates_frame, text="Benefit Term", bg='#008631', fg='white',font=('Microsoft YaHei UI Light',10))
        benefitterm_label.place(x=10, y=90)

        benefitterm_display = Label(self.policy_dates_frame, width=10, text="Duration",font=('Microsoft YaHei UI Light', 10,))
        benefitterm_display.place(x=130, y=90)



        ########### SAVE and CLEAR BUTTON##########
        save_button = Button(self.policy_dates_frame, text="Save", font=('arial', 10 ),bg='white', fg='black', border=0, command=submit_policyinput, padx=15)
        save_button.place(x=60, y=140)
        clear_button = Button(self.policy_dates_frame, text="clear", font=('arial', 10 ),bg='white', fg='black', border=0, command=clear, padx=15)
        clear_button.place(x=140, y=140)


class policyowner_register:
    def __init__(self, master3):
        self.master3=master3
        self.master3.title("C.A.M.S v1.2022/Policy Owner Input")
        self.master3.geometry("700x680")
        self.master3.config(bg='#008631')
        self.master3.resizable(False, False)

        # def inputpolicyowner():
        #     self.master3.withdraw()
        #     self.inputpolicy = Toplevel(self.master3)
        #     self.app = insured_register(self.inputpolicy)

        def cancelregistration():

            messagebox.showwarning("", "Your are about to cancel your registration!")
            if messagebox.askokcancel("", "Confirm Cancel registration?"):

                ############## SELECT QUERY FROM tlb_policy, tlb_po,tlb_poinsured###################
                con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                cur = con.cursor()
                sql = "SELECT POLICY_ID,POLICY_NUM FROM tbl_policy where tbl_policy.POLICY_ID=POLICY_ID order by POLICY_ID DESC"
                cur.execute(sql)
                records = cur.fetchall()
                for x in records:  ####### I loop the datas extracted from my select query and assign each to a variable to manipulate each#########
                    Policynum = x[1]

                    ########## IF CLIENT WISH TO CANCEL REGISTRATION POLICY INPUT WILL BE TAGGED AS CANCELLED############

                    sql1 = "UPDATE tbl_policy SET POLICY_STATUS = 'CANCELLED' WHERE tbl_policy.POLICY_NUM = '" + str(Policynum) + "' "
                    cur.execute(sql1)
                    con.commit()
                    messagebox.showinfo("", "REGISTRATION CANCELLED!")
                    self.master3.withdraw()
                    self.home = Toplevel(self.master3)
                    self.app = MainWIndow(self.home)
                    break



        def clear():
            self.first_name_entry.delete(0,END)
            self.middle_name_entry.delete(0, END)
            self.last_name_entry.delete(0, END)
            self.profession_combobox.set("None")
            self.civil_status_combobox.set("None")
            self.first_name_entry.delete(0, END)
            self.mobile_entry.delete(0, END)
            self.landline_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.address_entry.delete(0, END)
            self.city_entry.delete(0, END)
            self.province_entry.delete(0, END)
            self.zipcode_entry.delete(0, END)
            self.country_combobox.set("None")
            self.address_type_combobox.set("None")

        def inputpolicyowner():
            ID=0
            firstname = self.first_name_entry.get()
            middlename = self.middle_name_entry.get()
            lastname = self.last_name_entry.get()
            age = self.age_spinbox.get()
            birthday = cal.get()
            profession = self.profession_combobox.get()
            civilstatus = self.civil_status_combobox.get()
            genderinput = gender.get()
            mobile=self.mobile_entry.get()
            landline=self.landline_entry.get()
            email=self.email_entry.get()
            ADDRESS_ID = 0
            address = self.address_entry.get(1.0,END)
            city = self.city_entry.get()
            province = self.province_entry.get()
            zipcode = self.zipcode_entry.get()
            countrycode = self.country_combobox.get()
            type = self.address_type_combobox.get()


            if firstname == "" or middlename == "" or lastname == "" or age == "" or birthday == "" or civilstatus == "" or profession == "" or genderinput == "" or mobile == "" or address == "" or city == "" \
                    or province == "" or zipcode == "" or countrycode == "" or type == "":
                messagebox.showerror("", "Some fields are missing in Client info")


            elif messagebox.askokcancel("", message="Proceed to Insured?"):
            # if messagebox.askokcancel("", message="Proceed to Insured?"):
                ## SELECT QUERY TO EXTRACT PO_ID FROM PARENT POLICY TO ASSIGN AS INDEX ID TO FOREIGN KEYS###
                con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                cur = con.cursor()
                ##
                sql = "Select POLICY_ID FROM tbl_policy"
                cur.execute(sql)
                indexes=cur.fetchall() #### fetch the policy id result is in tuple format
                indexes.reverse()  ### reversed the fetch result to get the last index
                x=indexes[0]   ### variable x is not holding the last tuple index
                items=list(x)  ### convert tuple to list to extract as normal integer
                index=items[0] ## finally assign last value of the list from the converted tuple assign to variable (index) then run INSERT query

                try:
                    sql = "INSERT INTO tbl_po(PO_ID,firstname,middlename,lastname,age, birthday,gender,profession,civilstatus)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (index, firstname,middlename,lastname,age,birthday,genderinput,profession,civilstatus)
                    cur.execute(sql, val)
                    con.commit()

                    sql2 = "INSERT INTO `tbladdress_po`(`ADDRESS_ID`, `address`,city,province,zipcode,country,type,PO_ADDRESS_ID)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    val2 = (ADDRESS_ID, address, city, province, zipcode, countrycode,type,index)
                    cur.execute(sql2, val2)
                    con.commit()

                    sql3 = "INSERT INTO tbl_contact_po(CONTACT_ID_PO,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE,CONTACT_FK_PO)  VALUES (%s,%s,%s,%s,%s,%s)"
                    val3 = (ID, mobile, landline, email, type, index)
                    cur.execute(sql3, val3)
                    con.commit()

                    messagebox.showinfo("", "Record inserted successfully!")
                    con.rollback()
                    con.close()
                    ### ROUTE to INSURED REGISTRATION####
                    self.master3.withdraw()
                    self.inputpolicy = Toplevel(self.master3)
                    self.app = insured_register(self.inputpolicy)
                except ValueError as e:
                    messagebox.showerror("", str(e))
                    con.rollback()
                    con.close()



        # ########################## Client info ###################################################
        self.user_info_frame =LabelFrame(self.master3, text="Client Information",bg='#008631',fg='white',width=800,height=300)
        self.user_info_frame.place(x=40,y=40)
        ##########Name############
        self.first_name_label =Label(self.user_info_frame, text="First Name",bg='#008631',fg='white',font=('Microsoft YaHei UI Light', 11))
        self.first_name_label.grid(row=0, column=0)

        self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.middle_name_label.grid(row=0, column=1)

        self.last_name_label =Label(self.user_info_frame, text="Last Name",bg='#008631',fg='white',font=('Microsoft YaHei UI Light', 11))
        self.last_name_label.grid(row=0, column=2)

        self.first_name_entry =  Entry(self.user_info_frame,width=25)
        self.middle_name_entry = Entry(self.user_info_frame,width=25)
        self.last_name_entry = Entry(self.user_info_frame,width=25)

        self.first_name_entry.grid(row=1, column=0 ,padx=10,pady=10,)
        self.middle_name_entry.grid(row=1, column=1 ,padx=10,pady=10)
        self.last_name_entry.grid(row=1, column=2,padx=10,pady=10)


        ##########AGE ############
        self.age_label =Label(self.user_info_frame, text="Age",bg='#008631',fg='white',font=('Microsoft YaHei UI Light', 11))
        self.age_spinbox =Spinbox(self.user_info_frame, from_=18, to=110,width=23,)
        self.age_label.grid(row=2, column=0)
        self.age_spinbox.grid(row=3, column=0,pady=15)
        self.age_label.grid(row=2, column=0)


        ########## BDAY############


        self.birthday_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.birthday_label.grid(row=2, column=1)
        cal = DateEntry(self.user_info_frame, selectmode='day',date_pattern="yyyy-mm-dd")
        cal.grid(row=3, column=1)


        ##########GENDER############

        gender = StringVar()
        self.Gender = Label(self.user_info_frame, text="Gender",bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.Gender.grid(row=2, column=2)
        self.mLabel = Label(self.user_info_frame, text="Male",bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mLabel.place(x=370,y=103)
        self.fLabel = Label(self.user_info_frame, text="Female",bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.fLabel.place(x=455,y=103)

        self.rbtnMale = Radiobutton(self.user_info_frame,variable=gender,value="Male",bg='#008631')
        self.rbtnMale.place(x=340,y=105)
        self.rbtnFemale =Radiobutton(self.user_info_frame,variable=gender,value="female",bg='#008631')
        self.rbtnFemale.place(x=425,y=105)


        ##########Profession############
        profession=["Accountant","Actor/Actress","Aircraft pilot","Software Engineer","Librarian","Architect","Artist","Barber","Bricklayer","Business Person","Butcher","Chef","Cleaner","Construction worker","Corporate Secretary","Dentist","Designer","Driver","Electrician","Engineer",
                    "Farmer","Fire Fighter","Fisherman","Gardener","Hair Dresser","House Pinter and Decorator","Journalist","Judge","Lawyer","Lifeguard","Mail Carrier","Mechanic","Model","Nurse","Personal Assistant","Cashier","Pharmacist","Photographer","Physician",
                    "Plumber","Police officer","Politician","Realstate Broker","Salesperson","Scientist","Sea Farer","Software Developer","Soldier","Tailor","Teacher","Technician","Veterinarian","Waiter","Web Developer","Worker","Others not specified"]


        def search(event):
            self.profession_combobox.set("")
            value=event.widget.get()
            if value == "":
                self.profession_combobox['value']=profession
            else:
                data=[]
                for item in profession:
                    if value.lower() in item.lower():
                        data.append(item)
                self.profession_combobox['values']=data

        self.profession_label = Label(self.user_info_frame, text="Profession",bg='#008631',fg='white',font=('Microsoft YaHei UI Light', 11))
        self.profession_combobox = ttk.Combobox(self.user_info_frame,width=23,values=profession)
        self.profession_combobox.set("Search")
        self.profession_label.grid(row=4, column=0)
        self.profession_combobox.grid(row=5, column=0)
        self.profession_combobox.bind('<Button-1>', search)
        self.profession_combobox.bind('<KeyRelease>', search)

        ##########Civil Status############
        sts=['Single','Married','Widowed','Annulled']
        self.status_label = Label(self.user_info_frame, text="Civil Status", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.civil_status_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts)
        self.civil_status_combobox.set("")
        self.status_label.grid(row=4, column=1)
        self.civil_status_combobox.grid(row=5, column=1)

    ############### ADD CONTACT TAB#######
        self.contact_info_frame=LabelFrame(master3,text='Contact Information',bg='#008631',fg='white',width=515, height=110)
        self.contact_info_frame.place(x=40,y=250)

        self.mobile_Label=Label(self.contact_info_frame, text="Mobile Number", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mobile_Label.place(x=0, y=0)

        self.landline_Label = Label(self.contact_info_frame, text="Landline", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.landline_Label.place(x=15, y=25)

        self.email_Label = Label(self.contact_info_frame, text="Email", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.email_Label.place(x=15, y=50)

        self.mobile_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.mobile_entry.place(x=120, y=0)

        self.landline_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.landline_entry.place(x=120, y=25)

        self.email_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.email_entry.place(x=120, y=50)


        ################### Address##############################
        address_type = ['Primary', 'Alternate']

        country = ["PH"]

        self.addressframe = LabelFrame(master3, text="Address Information", bg='#008631', fg='white', width=550,height=200)
        self.addressframe.place(x=40, y=360)

        address_label = Label(self.addressframe, text="Address:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        address_label.place(x=0, y=0)
        self.address_entry = Text(self.addressframe, width=40,height=2, bg='white')
        self.address_entry.place(x=57, y=0)

        city_label = Label(self.addressframe, text="City:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        city_label.place(x=0, y=40)
        self.city_entry = Entry(self.addressframe, width=45, bg='white')
        self.city_entry.place(x=57, y=43)

        province_label = Label(self.addressframe, text="Province:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        province_label.place(x=0, y=64)
        self.province_entry = Entry(self.addressframe, width=45, bg='white')
        self.province_entry.place(x=57, y=66)

        zipcode_label = Label(self.addressframe, text="Zipcode:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        zipcode_label.place(x=0, y=87)
        self.zipcode_entry = Entry(self.addressframe, width=16, bg='white')
        self.zipcode_entry.place(x=88, y=88)

        countrycode_label = Label(self.addressframe, text="Country code:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        countrycode_label.place(x=0, y=107)
        self.country_combobox = ttk.Combobox(self.addressframe, width=13, values=country)
        self.country_combobox.place(x=88, y=110)

        address_type_label = Label(self.addressframe, text="Type:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        address_type_label.place(x=0, y=127)
        self.address_type_combobox = ttk.Combobox(self.addressframe, width=13, values=address_type)
        self.address_type_combobox.place(x=88, y=133)
        self.address_type_combobox.set("Type")


        self.button1=Button(self.master3,text="Save Details",font=('arial',9,'bold'),padx=10,pady=5,bg="white", fg='black', border=0,command=inputpolicyowner)
        self.button1.place(x=190,y=570)
        self.clear_button = Button(self.master3, text="Clear", font=('arial', 9, 'bold'),bg="white", border=0,padx=20,pady=5 ,command=clear)
        self.clear_button.place(x=300, y=570)
        self.cancel_button = Button(self.master3, text="Cancel", font=('arial', 9, 'bold'), bg="white", border=0, padx=20,pady=5, command=cancelregistration)
        self.cancel_button.place(x=390, y=570)


#############################Insured Register################################################

class insured_register:
    def __init__(self, master4):
        self.master4=master4
        self.master4.title("C.A.M.S v1.2022/Insured Input")
        self.master4.geometry("700x680")
        self.master4.config(bg='#008631')
        self.master4.resizable(False,False)

        def cancelregistration():

            messagebox.showwarning("", "Your are about to cancel your registration!")
            if messagebox.askokcancel("", "Confirm Cancel registration?"):

                ############## SELECT QUERY FROM tlb_policy, tlb_po,tlb_poinsured###################
                con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                cur = con.cursor()
                sql = "SELECT POLICY_ID,POLICY_NUM FROM tbl_policy where tbl_policy.POLICY_ID=POLICY_ID order by POLICY_ID DESC"
                cur.execute(sql)
                records = cur.fetchall()
                for x in records:  ####### I loop the datas extracted from my select query and assign each to a variable to manipulate each#########
                    Policynum = x[1]

                    ########## IF CLIENT WISH TO CANCEL REGISTRATION POLICY INPUT WILL BE TAGGED AS CANCELLED############

                    sql1 = "UPDATE tbl_policy SET POLICY_STATUS = 'CANCELLED' WHERE tbl_policy.POLICY_NUM = '" + str(Policynum) + "' "
                    cur.execute(sql1)
                    con.commit()
                    messagebox.showinfo("", "REGISTRATION CANCELLED!")
                    self.master4.withdraw()
                    self.home = Toplevel(self.master4)
                    self.app = MainWIndow(self.home)
                    break

        def clear():
            self.first_name_entry.delete(0,END)
            self.middle_name_entry.delete(0, END)
            self.last_name_entry.delete(0, END)
            self.profession_combobox.set("None")
            self.civil_status_combobox.set("None")
            self.first_name_entry.delete(0, END)
            self.mobile_entry.delete(0, END)
            self.landline_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.address_entry.delete(0,END)
            self.city_entry.delete(0,END)
            self.province_entry.delete(0,END)
            self.zipcode_entry.delete(0,END)
            self.country_combobox.set("None")
            self.address_type_combobox.set("None")


        def inputpolicyinsured():
            ID = 0
            firstname = self.first_name_entry.get()
            middlename = self.middle_name_entry.get()
            lastname = self.last_name_entry.get()
            age = self.age_spinbox.get()
            birthday = cal.get()
            profession = self.profession_combobox.get()
            civilstatus = self.civil_status_combobox.get()
            genderinput = gender.get()
            mobile = self.mobile_entry.get()
            landline = self.landline_entry.get()
            email = self.email_entry.get()
            ADDRESS_ID = 0
            address = self.address_entry.get(1.0,END)
            city = self.city_entry.get()
            province = self.province_entry.get()
            zipcode = self.zipcode_entry.get()
            countrycode = self.country_combobox.get()
            type = self.address_type_combobox.get()


            if firstname == "" or middlename == "" or lastname == "" or age == "" or birthday == "" or civilstatus == "" or profession== "" or genderinput == "" or mobile == "" or address == "" or city == "" \
                    or province == "" or zipcode == "" or countrycode == "" or type == "":
                messagebox.showerror("", "Some fields are missing in Client info")


            elif messagebox.askokcancel("", message="Proceed to Beneficiary?"):
            # if messagebox.askokcancel("", message="Proceed to Beneficiary?"):
                con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                cur = con.cursor()

                sql = "Select POLICY_ID FROM tbl_policy"
                cur.execute(sql)
                indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                indexes.reverse()  ### reversed the fetch result to get the last index
                x = indexes[0]  ### variable x is not holding the last tuple index
                items = list(x)  ### convert tuple to list to extract as normal integer
                index = items[0]  ## finally assign last value of the list from the converted tuple assign to variable (index) then run INSERT query


                sql = "INSERT INTO tbl_insured(INS_ID,firstname,middlename,lastname,age,birthday,gender,profession,civilstatus)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (index, firstname, middlename, lastname, age, birthday, genderinput, profession, civilstatus)
                cur.execute(sql, val)

                sql2 = "INSERT INTO tbladdress_ins(ADDRESS_ID,address,city,province,zipcode,country,type,INS_ADDRESS_ID)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                val2 = (ADDRESS_ID, address, city, province, zipcode, countrycode, type,index)
                cur.execute(sql2, val2)
                con.commit()

                sql3 = "INSERT INTO tbl_contact_ins(CONTACT_ID_INS,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE,CONTACT_FK_INS)  VALUES (%s,%s,%s,%s,%s,%s)"
                val3 = (ID, mobile, landline, email, type, index)
                cur.execute(sql3, val3)
                con.commit()


                messagebox.showinfo("", "Record inserted successfully!")
                con.rollback()
                con.close()

                self.master4.withdraw()
                self.inputpolicyinsured = Toplevel(self.master4)
                self.app =bene_register(self.inputpolicyinsured)



        self.user_info_frame = LabelFrame(self.master4, text="Insured Information", bg='#008631', fg='white', width=800,height=300)
        self.user_info_frame.place(x=40, y=40)

        ##########Name############
        self.first_name_label = Label(self.user_info_frame, text="First Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.first_name_label.grid(row=0, column=0)

        self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.middle_name_label.grid(row=0, column=1)

        self.last_name_label = Label(self.user_info_frame, text="Last Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.last_name_label.grid(row=0, column=2)

        self.first_name_entry = Entry(self.user_info_frame, width=25)
        self.middle_name_entry = Entry(self.user_info_frame, width=25)
        self.last_name_entry = Entry(self.user_info_frame, width=25)

        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, )
        self.middle_name_entry.grid(row=1, column=1, padx=10, pady=10)
        self.last_name_entry.grid(row=1, column=2, padx=10, pady=10)

        ##########AGE ############
        self.age_label = Label(self.user_info_frame, text="Age", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.age_spinbox = Spinbox(self.user_info_frame, from_=18, to=110, width=23, )
        self.age_label.grid(row=2, column=0)
        self.age_spinbox.grid(row=3, column=0, pady=15)
        self.age_label.grid(row=2, column=0)


        ########## BDAY############
        self.birthday_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.birthday_label.grid(row=2, column=1)
        cal = DateEntry(self.user_info_frame, selectmode='day',date_pattern="yyyy-mm-dd")
        cal.grid(row=3, column=1)


        ##########GENDER############
        gender = StringVar()
        self.Gender = Label(self.user_info_frame, text="Gender", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.Gender.grid(row=2, column=2)
        self.mLabel = Label(self.user_info_frame, text="Male", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mLabel.place(x=370, y=103)
        self.fLabel = Label(self.user_info_frame, text="Female", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.fLabel.place(x=455, y=103)

        self.rbtnMale = Radiobutton(self.user_info_frame, variable=gender,value="Male", bg='#008631')
        self.rbtnMale.place(x=340, y=105)
        self.rbtnFemale = Radiobutton(self.user_info_frame,variable=gender, value="Female", bg='#008631')
        self.rbtnFemale.place(x=425, y=105)

        ##########Profession############
        profession = ["Accountant", "Actor/Actress", "Aircraft pilot", "Application or Software Engineer", "Librarian",
                      "Architect", "Artist", "Barber", "Bricklayer", "Business Person", "Butcher", "Chef", "Cleaner",
                      "Construction worker", "Corporate Secretary", "Dentist", "Designer", "Driver", "Electrician",
                      "Engineer",
                      "Farmer", "Fire Fighter", "Fisherman", "Gardener", "Hair Dresser", "House Pinter and Decorator",
                      "Journalist", "Judge", "Lawyer", "Lifeguard", "Mail Carrier", "Mechanic", "Model", "Nurse",
                      "Others not specified", "Personal Assistant", "Cashier", "Pharmacist", "Photographer",
                      "Physician",
                      "Plumber", "Police officer", "Politician", "Realstate Broker", "Salesperson", "Scientist",
                      "Sea Farer", "Software Developer", "Soldier", "Tailor", "Teacher", "Technician", "Veterinarian",
                      "Waiter", "Web Developer", "Worker"]

        def search(event):
            value = event.widget.get()
            if value == "":
                self.profession_combobox['value'] = profession
            else:
                data = []
                for item in profession:
                    if value.lower() in item.lower():
                        data.append(item)
                self.profession_combobox['values'] = data

        self.profession_label = Label(self.user_info_frame, text="Profession", bg='#008631', fg='white',
                                      font=('Microsoft YaHei UI Light', 11))
        self.profession_combobox = ttk.Combobox(self.user_info_frame, width=23, values=profession)
        self.profession_combobox.set("Search")
        self.profession_label.grid(row=4, column=0)
        self.profession_combobox.grid(row=5, column=0)
        self.profession_combobox.bind('<KeyRelease>', search)

        ##########Civil Status############

        sts = ['Single', 'Married', 'Widowed', 'Annulled']
        self.status_label = Label(self.user_info_frame, text="Civil Status", bg='#008631', fg='white',
                                  font=('Microsoft YaHei UI Light', 11))
        self.civil_status_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts)
        self.civil_status_combobox.set("")
        self.status_label.grid(row=4, column=1)
        self.civil_status_combobox.grid(row=5, column=1)

        ############### Conctact info####################

        self.contact_info_frame=LabelFrame(master4,text='Contact Information',bg='#008631',fg='white',width=515, height=110)
        self.contact_info_frame.place(x=40,y=250)

        self.mobile_Label=Label(self.contact_info_frame, text="Mobile Number", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mobile_Label.place(x=0, y=0)

        self.landline_Label = Label(self.contact_info_frame, text="Landline", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.landline_Label.place(x=15, y=25)

        self.email_Label = Label(self.contact_info_frame, text="Email", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.email_Label.place(x=15, y=50)

        self.mobile_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.mobile_entry.place(x=120, y=0)

        self.landline_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.landline_entry.place(x=120, y=25)

        self.email_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.email_entry.place(x=120, y=50)



        ################### Address##############################
        # address_type = ['Residence', 'Office', 'Mailing/Billing']
        address_type = ['Primary', 'Alternate']

        country = ["PH"]

        self.addressframe = LabelFrame(master4, text="Address Information", bg='#008631', fg='white', width=550, height=200)
        self.addressframe.place(x=40, y=360)

        address_label=Label(self.addressframe,text="Address:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        address_label.place(x=0,y=0)
        self.address_entry = Text(self.addressframe, width=40, height=2, bg='white')
        self.address_entry.place(x=57, y=0)

        city_label = Label(self.addressframe, text="City:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        city_label.place(x=0, y=40)
        self.city_entry = Entry(self.addressframe, width=45, bg='white')
        self.city_entry.place(x=57, y=43)

        province_label = Label(self.addressframe, text="Province:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        province_label.place(x=0, y=64)
        self.province_entry = Entry(self.addressframe, width=45, bg='white')
        self.province_entry.place(x=57, y=66)


        zipcode_label=Label(self.addressframe, text="Zipcode:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        zipcode_label.place(x=0, y=87)
        self.zipcode_entry = Entry(self.addressframe, width=16, bg='white')
        self.zipcode_entry.place(x=88, y=88)

        countrycode_label = Label(self.addressframe, text="Country code:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        countrycode_label.place(x=0, y=107)
        self.country_combobox = ttk.Combobox(self.addressframe, width=13, values=country)
        self.country_combobox.place(x=88, y=110)

        address_type_label = Label(self.addressframe, text="Type:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        address_type_label.place(x=0, y=127)
        self.address_type_combobox = ttk.Combobox(self.addressframe, width=13, values=address_type)
        self.address_type_combobox.place(x=88, y=133)
        self.address_type_combobox.set("Type")


        self.button1 = Button(self.master4, text="Input Insured", font=('arial', 9, 'bold'),bg='white', fg='black', border=0, command=inputpolicyinsured)
        self.button1.place(x=220, y=570)
        self.clear_button = Button(self.master4, text="Clear", font=('arial', 9, 'bold'),bg='white', fg='black', border=0, padx=15, command=clear)
        self.clear_button.place(x=310, y=570)

        self.cancel_button = Button(self.master4, text="Cancel", font=('arial', 9, 'bold'), bg='white', fg='black',border=0, padx=15, command=cancelregistration)
        self.cancel_button.place(x=390, y=570)


############################Beneficiary Register################################################
class bene_register:
    def __init__(self,master5):
        self.master5=master5
        self.master5.title("C.A.M.S v1.2022/Beneficiary Input")
        self.master5.geometry("700x680")
        self.master5.config(bg='#008631')
        self.master5.resizable(False,False)


        value = IntVar() ### this variable holds the percentage of the beneficiaries maximum percentage over all per policy is 100% splits every bene elected
        self.x=0  ## this variable also signifies the percentage per benefiary
        self.husband_counter=0  ## counter husband maximum 1
        self.wife_counter=0  ## counter wife maximum 1
        self.sumbenefit=0   ## variable that adds collected percentage for display to share() function

        ##### Insert Query#######
        def Insert_query():
            global beneindex
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()

            sql = "Select POLICY_ID FROM tbl_policy"
            cur.execute(sql)
            indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
            indexes.reverse()  ### reversed the fetch result to get the last index
            x=indexes[0]
            items=list(x)
            index=items[0] ## finally assign last value of the list from the converted tuple assign to variable (index) then run INSERT query

            sql1 = "INSERT INTO tbl_bene(BENE_ID, firstname,middlename,lastname,age,birthday,gender,relationship,benefit_percentage,BENE_POLICY_ID)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (Bene_ID, firstname, middlename, lastname, age, birthday, genderinput, relationship, percentage,index)
            cur.execute(sql1, val)
            con.commit()



            sql2 = "INSERT INTO tbladdress_bene(ADDRESS_ID,address,city,province,zipcode,country,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val2 = (ADDRESS_ID, address, city, province, zipcode, countrycode,Type)
            cur.execute(sql2, val2)
            con.commit()

            sql3 = "INSERT INTO tbl_contact_bene(CONTACT_ID_BENE,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE)  VALUES (%s,%s,%s,%s,%s)"
            val3 = (Bene_ID, mobile, landline, email, Type)
            cur.execute(sql3, val3)
            con.commit()
            messagebox.showinfo("", "Beneficiary Added successfully!")
            con.rollback()
            con.close()



        def Benecheck():  ##### THIS FUNCTION IDENTIFIES THE NAME OF THE INSURED ELECTED FROM INSURED INPUT TAB,, ONCE SYSTEM DETECTS SAME INPUT AS BENEFICIARY SYSTEM DECLINES THE INPUT####
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()
            sql1 = "Select INS_ID,firstname,middlename,lastname FROM tbl_insured where INS_ID= INS_ID order by INS_ID DESC"
            cur.execute(sql1)
            insuredname = cur.fetchone()#### fetch firstname,middlename,lastname of the insured displays as tupple inside a list this format " [()] "
            # insuredname.reverse() ### reverse to access the last input
            print(insuredname)
            ## this line extract access the tupple inside the list
            fname=insuredname[1]  ###assigning variable to every item inside the tupple
            mname=insuredname[2] ###assigning variable to every item inside the tupple
            lname=insuredname[3]
            fullname=fname+" "+ mname+" "+lname   ### combine extracted data and returning the "fullname"
            return fullname


        ###### Benefit Share Computation #######
        def share():
            self.sumbenefit=self.sumbenefit+percentage



        def update():
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()
            # sql="DELETE FROM tbl_bene WHERE tbl_bene.BENE_ID = '"+ str(beneindex) +"' "
            # sql1="DELETE FROM tbladdress_bene WHERE tbl_bene.BENE_ID = '"+ str(beneindex) +"' "
            sql = "DELETE FROM tbl_bene WHERE tbl_bene.BENE_ID =BENE_POLICY_ID"
            cur.execute(sql)
            sql1 = "DELETE FROM tbladdress_bene WHERE ADDRESS_ID=ADDRESS_ID"
            cur.execute(sql1)
            con.commit()
            con.close()


        ###### Relation ship Husband Fuction#######
        ### EVERY FUNCTION FOR  relalationship_husband(),relalationship_wife() , relalationship_others() checks if the insured is different on the elected bene system will decline if
        ### user input the same person.
        def relalationship_husband():
            fullname=Benecheck() #### extracted full name from the said function
            if self.husband_counter == 1:
                share()
                self.x = self.x + percentage
                if self.sumbenefit < 100:
                    if fullname != client_fullname:
                        Insert_query()
                        if messagebox.askyesno("", "Input another Beneficiary?"):
                            clear()
                        else:
                            messagebox.showwarning("Unable to use Max Percentage","Balance:" + str(self.sumbenefit - 100) + "%")
                            clear()
                    else:
                        messagebox.showerror("","Cannot Accept INSURED AS BENEFICIARY")
                        update()
                        self.x=0
                        self.husband_counter=0
                        self.sumbenefit=0
                        # print(self.x)
                        # print(self.husband_counter)
                        # print(self.sumbenefit)
                        return self.x,self.sumbenefit,self.husband_counter

                elif self.sumbenefit == 100:
                    if fullname != client_fullname:
                        Insert_query()
                        messagebox.showinfo("", "Benefit limit maximum reached 100%")
                        self.master5.withdraw()
                        self.inputpolicyinsured = Toplevel(self.master5)
                        self.app = Policy_register_output(self.inputpolicyinsured)
                    else:
                        messagebox.showerror("","Cannot Accept INSURED AS BENEFICIARY")
                        update()
                        self.x = 0
                        self.husband_counter = 0
                        self.sumbenefit=0
                        # print(self.x)
                        # print(self.husband_counter)
                        # print(self.sumbenefit)
                        return self.x, self.sumbenefit, self.husband_counter
                else:
                    messagebox.showerror("", "Sobra ang iyong input!")
            else:
                messagebox.showerror("", "Unable to accept duplicate Relationship")
                # clear()

        ###### Relation ship WIFE Fuction#######
        def relalationship_wife():
            fullname = Benecheck() #### extracted full name from the said function
            if self.wife_counter == 1:
                share()
                self.x = self.x + percentage
                if self.sumbenefit < 100:
                    if fullname!=client_fullname:
                        Insert_query()
                        if messagebox.askyesno("", "Input another Beneficiary?"):
                            clear()
                        else:
                            messagebox.showwarning("Unable to use Max Percentage", "Balance:" + str(self.sumbenefit - 100) + "%")
                            clear()
                    else:
                        messagebox.showerror("","Cannot Accept INSURED AS BENEFICIARY")
                        update()
                        self.x = 0
                        self.wife_counter = 0
                        self.sumbenefit = 0
                        # print(self.x)
                        # print(self.wife_counter)
                        # print(self.sumbenefit)
                        return self.x, self.sumbenefit, self.husband_counter

                elif self.sumbenefit == 100:
                    if fullname != client_fullname:
                        Insert_query()
                        messagebox.showinfo("", "Benefit limit maximum reached 100%")
                        messagebox.showinfo("", "Proceed to Policy Input?")
                        self.master5.withdraw()
                        self.inputpolicyinsured = Toplevel(self.master5)
                        self.app = Policy_register_output(self.inputpolicyinsured)
                    else:
                        messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                        update()
                        self.x = 0
                        self.wife_counter = 0
                        self.sumbenefit = 0
                        # print(self.x)
                        # print(self.wife_counter)
                        # print(self.sumbenefit)
                        return self.x, self.sumbenefit, self.husband_counter
                else:
                    messagebox.showerror("", "Sobra ang iyong input!")
            else:
                messagebox.showerror("", "Unable to accept duplicate Relationship")

        ###### Relation ship OTHERS Fuction#######
        def others():
            fullname = Benecheck() #### extracted full name from the said function
            share()
            self.x = self.x + percentage
            if self.sumbenefit < 100:
                if fullname != client_fullname:
                    Insert_query()
                    if messagebox.askyesno("", "Input another Beneficiary?"):
                        clear()
                    else:
                        messagebox.showwarning("Unable to use Max Percentage","Balance:" + str(self.sumbenefit - 100) + "%")
                        clear()
                else:
                    messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                    update()
                    self.x = 0
                    self.sumbenefit = 0
                    # print(self.x)
                    # print(self.sumbenefit)
                    return self.x, self.sumbenefit, self.husband_counter

            elif self.sumbenefit == 100:
                if fullname != client_fullname:
                    Insert_query()
                    messagebox.showinfo("", "Benefit limit maximum reached 100%")
                    messagebox.showinfo("", "Proceed to Policy View?")
                    self.master5.withdraw()
                    self.inputpolicyinsured = Toplevel(self.master5)
                    self.app = Policy_register_output(self.inputpolicyinsured)
                else:
                    messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                    update()
                    self.x = 0
                    self.sumbenefit = 0
                    # print(self.x)
                    # print(self.sumbenefit)
                    return self.x, self.sumbenefit, self.husband_counter
            else:
                messagebox.showerror("", "Sobra ang iyong input!")
        ##############################################################################################################

        #### clear function ### just for clearing fields
        def clear():
            self.first_name_entry.delete(0, END)
            self.middle_name_entry.delete(0, END)
            self.last_name_entry.delete(0, END)
            self.relationship_combobox.set("None")
            self.percentage_entry_label.delete(0, END)
            self.first_name_entry.delete(0, END)
            self.mobile_entry.delete(0, END)
            self.address_entry.delete(1.0, END)
            self.city_entry.delete(0, END)
            self.province_entry.delete(0, END)
            self.zipcode_entry.delete(0, END)
            self.country_combobox.set("None")
            self.address_type_combobox.set("None")

    ########FUNCTION TO GET ALL INPUTS AND VALIDATES entry######

        def Input_bene():
            # ###TEMPO###
            # self.master5.withdraw()
            # self.inputpolicyinsured = Toplevel(self.master5)
            # self.app = Policy_register_output(self.inputpolicyinsured)

            global relationship,percentage,Bene_ID,firstname,middlename,lastname,age,birthday,genderinput,mobile,landline,email,ADDRESS_ID,address,city,province,zipcode,countrycode,Type,client_fullname
            Bene_ID=0
            firstname=self.first_name_entry.get()
            middlename=self.middle_name_entry.get()
            lastname=self.last_name_entry.get()
            age=self.age_spinbox.get()
            birthday=self.cal.get()
            genderinput=gender.get()
            relationship=self.relationship_combobox.get()
            percentage = value.get()
            mobile=self.mobile_entry.get()
            landline=self.Landline_entry.get()
            email=self.email_entry.get()
            ADDRESS_ID = 0
            address=self.address_entry.get("1.0",END)
            city=self.city_entry.get()
            province=self.province_entry.get()
            zipcode=self.zipcode_entry.get()
            countrycode=self.country_combobox.get()
            Type=self.address_type_combobox.get()
            client_fullname=firstname+ " "+ middlename+" "+ lastname


            #### DEFINING

            if self.x <=100:
                if firstname == "" or middlename == "" or lastname == "" or age == "" or birthday == "" or relationship == "" or percentage == "" or genderinput == "" or mobile == "" or address == "" or city == "" \
                        or province == "" or zipcode == "" or countrycode == "" or Type == "":
                    messagebox.showerror("", "Some fields are missing in Beneficiary information")
                elif relationship == "Husband":
                    if self.x+percentage<=100:
                        self.husband_counter = self.husband_counter + 1
                        relalationship_husband()

                    else:
                        messagebox.showerror("", "Input is morethan total limit=100%")
                        self.percentage_entry_label.delete(0, END)

                elif relationship == "Wife":
                    if self.x+percentage<=100:
                        self.wife_counter = self.wife_counter + 1
                        relalationship_wife()

                    else:
                        messagebox.showerror("", "Input is morethan total limit=100%")
                        self.percentage_entry_label.delete(0, END)

                else:
                    if self.x+percentage<=100:
                        others()

                    else:
                        messagebox.showerror("", "Input is morethan total limit=100%")
                        self.percentage_entry_label.delete(0, END)
                ############################################################################################

        def cancelregistration():

            messagebox.showwarning("", "Your are about to cancel your registration!")
            if messagebox.askokcancel("", "Confirm Cancel registration?"):

                ############## SELECT QUERY FROM tlb_policy, tlb_po,tlb_poinsured###################
                con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                cur = con.cursor()
                sql = "SELECT POLICY_ID,POLICY_NUM FROM tbl_policy where tbl_policy.POLICY_ID=POLICY_ID order by POLICY_ID DESC"
                cur.execute(sql)
                records = cur.fetchall()
                for x in records:  ####### I loop the datas extracted from my select query and assign each to a variable to manipulate each#########
                    Policynum = x[1]

                    ########## IF CLIENT WISH TO CANCEL REGISTRATION POLICY INPUT WILL BE TAGGED AS CANCELLED############

                    sql1 = "UPDATE tbl_policy SET POLICY_STATUS = 'CANCELLED' WHERE tbl_policy.POLICY_NUM = '" +str(Policynum)+"' "
                    cur.execute(sql1)
                    con.commit()
                    messagebox.showinfo("", "REGISTRATION CANCELLED!")
                    self.master5.withdraw()
                    self.home = Toplevel(self.master5)
                    self.app = MainWIndow(self.home)
                    break



        ####BENE INPUT WIDGETS######
        self.user_info_frame = LabelFrame(self.master5, text="Beneficiary Information", bg='#008631', fg='white',width=550, height=230)
        self.user_info_frame.place(x=40, y=40)
        self.first_name_label = Label(self.user_info_frame, text="First Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.first_name_label.place(x=10, y=10)
        self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.middle_name_label.place(x=170, y=10)

        self.last_name_label = Label(self.user_info_frame, text="Last Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.last_name_label.place(x=330, y=10)

        self.first_name_entry = Entry(self.user_info_frame, width=25)
        self.first_name_entry.place(x=10, y=40)
        self.middle_name_entry = Entry(self.user_info_frame, width=25)
        self.middle_name_entry.place(x=170, y=40)
        self.last_name_entry = Entry(self.user_info_frame, width=25)
        self.last_name_entry.place(x=330, y=40)

        # ##########AGE ############
        self.age_label = Label(self.user_info_frame, text="Age", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.age_spinbox = Spinbox(self.user_info_frame, from_=18, to=110, width=23, )
        self.age_spinbox.place(x=10, y=95)
        self.age_label.place(x=10, y=60)

        # ########## BDAY############
        self.birthday_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.birthday_label.place(x=170, y=60)

        self.cal = DateEntry(self.user_info_frame, selectmode='day', date_pattern="yyyy-mm-dd")
        self.cal.place(x=170, y=95)

          ##########GENDER############
        gender = StringVar()
        self.Gender = Label(self.user_info_frame, text="Gender", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.Gender.place(x=290, y=60)
        self.mLabel = Label(self.user_info_frame, text="Male", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mLabel.place(x=320, y=90)
        self.fLabel = Label(self.user_info_frame, text="Female", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.fLabel.place(x=385, y=90)

        self.rbtnMale = Radiobutton(self.user_info_frame, variable=gender, value="Male", bg='#008631')
        self.rbtnMale.place(x=290, y=90)
        self.rbtnFemale = Radiobutton(self.user_info_frame, variable=gender, value="Female", bg='#008631')
        self.rbtnFemale.place(x=360, y=90)

    # ###########Relationship############
        sts = ['Husband', 'Wife', 'Child', 'Parent', 'Legal Guardian', 'others']
        self.status_label = Label(self.user_info_frame, text="Relationship", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.status_label.place(x=10, y=120)

        self.relationship_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts)
        self.relationship_combobox.set("None")
        self.relationship_combobox.place(x=10, y=145)

    ###########Benefit_Percentage############

        self.percentage_label = Label(self.user_info_frame, text="Benefit Percentage", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.percentage_label.place(x=190, y=120)

        self.percentage_entry_label = Entry(self.user_info_frame, width=25, textvariable=value)
        self.percentage_entry_label.place(x=190, y=145)


        self.NoteLabel = Label(self.user_info_frame,text="NOTE:Percentage shares for all bene will be strictly limited to total of 100%",bg='#008631', fg='white', font=('Microsoft YaHei UI Light', 10))
        self.NoteLabel.place(x=10, y=170)

        ############## ADD CONTACT TAB##############

        self.contact_info_frame = LabelFrame(self.master5, text='Contact Information', bg='#008631', fg='white',width=400, height=110)
        self.contact_info_frame.place(x=40, y=270)

        self.mobile_Label = Label(self.contact_info_frame, text="Mobile Number", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.mobile_Label.place(x=0, y=0)
        self.mobile_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.mobile_entry.place(x=120, y=0)

        self.Landline_Label = Label(self.contact_info_frame, text="Landline", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.Landline_Label.place(x=0, y=30)
        self.Landline_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.Landline_entry.place(x=120, y=30)

        self.email_Label = Label(self.contact_info_frame, text="Email", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        self.email_Label.place(x=0, y=60)
        self.email_entry = Entry(self.contact_info_frame, width=35, bg='white')
        self.email_entry.place(x=120, y=60)



        # # ################### Address##############################
        address_type = ['Residence', 'Office', 'Mailing/Billing']
        address_type = ['Primary', 'Alternate']
        country = ["PH"]

        self.addressframe = LabelFrame(self.master5, text="Address Information", bg='#008631', fg='white', width=550, height=200)
        self.addressframe.place(x=40, y=380)

        self.address_label=Label(self.addressframe,text="Address:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.address_label.place(x=0,y=0)
        self.address_entry = Text(self.addressframe, width=40, height=2, bg='white')
        self.address_entry.place(x=57, y=0)

        self.city_label = Label(self.addressframe, text="City:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.city_label.place(x=0, y=40)
        self.city_entry = Entry(self.addressframe, width=45, bg='white')
        self.city_entry.place(x=57, y=43)

        self.province_label = Label(self.addressframe, text="Province:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.province_label.place(x=0, y=64)
        self.province_entry = Entry(self.addressframe, width=45, bg='white')
        self.province_entry.place(x=57, y=66)


        self.zipcode_label=Label(self.addressframe, text="Zipcode:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.zipcode_label.place(x=0, y=87)
        self.zipcode_entry = Entry(self.addressframe, width=16, bg='white')
        self.zipcode_entry.place(x=88, y=88)

        self.countrycode_label = Label(self.addressframe, text="Country code:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.countrycode_label.place(x=0, y=107)
        self.country_combobox = ttk.Combobox(self.addressframe, width=13, values=country)
        self.country_combobox.place(x=88, y=110)


        self.address_type_label = Label(self.addressframe, text="Type:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
        self.address_type_label.place(x=0, y=127)
        self.address_type_combobox = ttk.Combobox(self.addressframe, width=13, values=address_type)
        self.address_type_combobox.place(x=88, y=133)
        self.address_type_combobox.set("Type")

        self.button1 = Button(self.master5, text="Input Beneficiaries", font=('arial', 9, 'bold'),bg='white', fg='black', border=0, command=Input_bene, padx=10)
        self.button1.place(x=150, y=600)

        self.clear_button = Button(self.master5, text="Clear", font=('arial', 9, 'bold'),bg='white', fg='black', border=0, padx=15, command=clear)
        self.clear_button.place(x=290, y=600)

        self.cancel_button = Button(self.master5, text="Cancel", font=('arial', 9, 'bold'), bg='white', fg='black',border=0, padx=15, command=cancelregistration)
        self.cancel_button.place(x=370, y=600)


class Policy_register_output:
    def __init__(self, master8):
        self.master8=master8
        self.master8.title("C.A.M.S v1.2022 - Policy Information overview")
        self.master8.geometry("930x500")
        self.master8.config(bg='#008631')
        self.master8.resizable(False,False)

        def query():
            ############## SELECT QUERY FROM tlb_policy, tlb_po,tlb_poinsured####################

            con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
            cur = con.cursor()
            sql = "SELECT POLICY_ID,POLICY_NUM,POLICY_STATUS,PRODUCT_NAME,REG_DATE,tbl_po.firstname,tbl_po.middlename,tbl_po.lastname,tbl_contact_po.email,tbl_contact_po.mobile,tbl_insured.age FROM tbl_policy join tbl_po on POLICY_ID=PO_ID JOIN tbl_contact_po on PO_ID=CONTACT_FK_PO JOIN tbl_insured on POLICY_ID=INS_ID WHERE POLICY_ID=POLICY_ID ORDER BY POLICY_ID DESC;"
            cur.execute(sql)
            records = cur.fetchall()
            for x in records:  ####### I loop the datas extracted from my select query and assign each to a variable to manipulate each#########
                Policy_ID=x[0]
                Policynum = x[1]
                Policystatus = x[2]
                ProductName = x[3]
                regDate = x[4]
                firstname=x[5]
                middlename=x[6]
                lastname=x[7]
                email=x[8]
                contact=x[9]
                getage=x[10]
                return Policy_ID,Policynum, Policystatus, ProductName, regDate,firstname,middlename,lastname,email,contact,getage


        ######Variables#####
        getpolicy_type = StringVar()
        global Policy_ID,Policynum, Policystatus, ProductName, regDate, fullname, email, contact, getage, total, frequency,mode
        Policy_ID,Policynum, Policystatus, ProductName, regDate, firstname, middlename, lastname, email, contact, getage= query()
        fullname = firstname + " " + middlename + " " + lastname

        ############### FUNCTIONS ######################
        def Payfunction():
            duration = getpaymentduration.get()
            frequency=getfrequency_type.get()
            mode="Regular"
            age = int(getage)

            total = 0
            ###### PAYMENT FREQUENCY############
            MONTHLY = 31
            QUARTERLY = 90
            SEMIANNUAL = 181
            ANNUAL = 365

            ##### AGE BRACKET PAYMENT PER AGE#####
            bracket1 = 30
            bracket2 = 32
            bracket3 = 35
            bracket4 = 37
            bracket5 = 39
            ####################################


            ################## PAYMENT COMPUTATION########################
            ########### computation of payment based on the extracted age from tbl_insured depending on age is the clients payment multiplied by frequency selected######
            if age <= 18:
                if frequency == "Monthly":
                    total = bracket1 * MONTHLY
                    Total_amount.config(text=total)

                elif frequency == "Quarterly" :
                    total = bracket1 * QUARTERLY
                    Total_amount.config(text=total)
                elif frequency == "SemiAnnual":
                    total = bracket1 * SEMIANNUAL
                    Total_amount.config(text=total)
                elif frequency == "Annual":
                    total = bracket1 * ANNUAL
                    Total_amount.config(text=total)

            elif age <= 30:
                if frequency == "Monthly":
                    total = bracket2 * MONTHLY
                    Total_amount.config(text=total)
                elif frequency == "Quarterly":
                    total = bracket2 * QUARTERLY
                    Total_amount.config(text=total)
                elif frequency == "SemiAnnual":
                    total = bracket2 * SEMIANNUAL
                    Total_amount.config(text=total)
                elif frequency == "Annual":
                    total = bracket2 * ANNUAL
                    Total_amount.config(text=total)

            elif age <= 35:
                if frequency == "Monthly":
                    total = bracket3 * MONTHLY
                    Total_amount.config(text=total)
                elif frequency == "Quarterly" :
                    total = bracket3 * QUARTERLY
                    Total_amount.config(text=total)
                elif frequency == "SemiAnnual":
                    total = bracket3 * SEMIANNUAL
                    Total_amount.config(text=total)
                elif frequency == "Annual":
                    total = bracket3 * ANNUAL
                    Total_amount.config(text=total)

            elif age <= 40:
                if frequency == "Monthly":
                    total = bracket4 * MONTHLY
                    Total_amount.config(text=total)
                elif frequency == "Quarterly":
                    total = bracket4 * QUARTERLY
                    Total_amount.config(text=total)
                elif frequency == "SemiAnnual":
                    total = bracket4 * SEMIANNUAL
                    Total_amount.config(text=total)
                elif frequency == "Annual":
                    total = bracket4 * ANNUAL
                    Total_amount.config(text=total)

            elif age <= 45:

                if frequency == "Monthly":
                    total = bracket5 * MONTHLY
                    Total_amount.config(text=total)
                elif frequency == "Quarterly":
                    total = bracket5 * QUARTERLY
                    Total_amount.config(text=total)
                elif frequency == "SemiAnnual":
                    total = bracket5 * SEMIANNUAL
                    Total_amount.config(text=total)
                elif frequency == "Annual":
                    total = bracket5 * ANNUAL
                    Total_amount.config(text=total)


            ####### UPDATE QUERY TO UPDATE TOTAL AMOUNT TO POLICY TABLE FROM TOTAL GOT FROM FREQUNCY AND AGE OF THE INSURED#####
            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
            cur = con.cursor()
            sql = "UPDATE tbl_policy SET MODE = '"+mode+"', FREQUENCY= '"+frequency+"',PAYMENT_DURATION='"+duration+"', PAYMENT_TOTAL='"+str(total) +"' WHERE POLICY_ID = '"+str(Policy_ID)+"'"
            cur.execute(sql)
            con.commit()
            messagebox.showinfo("", "Initial payment selected Successfully!")
            con.rollback()
            con.close()


            ####################### EMAIL NOTIFICATION FOR PAYMENT TO CLIENT#################
            def email_alert():
                html = """
                    <html>
                        <body>
                        <h3>Greetings! our valued client,</h3>
                        <p>Our records shows that you have a payment due Pending to activate your Policy, kindly process you`re initial payment. <br>
                        If payment has been sent, please disregard this email. <br>
                        <br>
                        """ + "Total amount due for your first"+ " "+ str(frequency)+" "+ "due is"+" "+"₱" + str(total)+ """
                        <br>
                        <br>
                        """ + "To Process your payment kindly click the (One-Time Payment link:)"+"http://localhost/PHP/payment.html"+"""
                        <br>
                        <br>
                        Please let us know if you have questions or need assistance with the payment process.<br>
                        <br>
                        <br>
                        Thank you!,<br>
                        Management
                        </p>
                        </body>
                    </html>
                """

                email_from = 'liezlcute08@gmail.com'
                password = 'hajgngusvfyalrrb'
                email_to = email

                date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

                email_message = MIMEMultipart()
                email_message['From'] = email_from
                email_message['To'] = email_to
                email_message['Subject'] = f'Payment Reminder -{date_str}'
                email_message.attach(MIMEText(html, "html"))

                email_string = email_message.as_string()

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(email_from, password)
                    server.sendmail(email_from, email_to, email_string)


            if messagebox.askokcancel("", "Proceed to payment?"):
                email_alert()
                messagebox.showinfo("Registration Successful","Kindly Check your email for payment Instruction.")
                self.master8.withdraw()
                self.inputpolicyinsured = Toplevel(self.master8)
                self.app = Policy_view_main_admin(self.inputpolicyinsured)


        def cancelregistration():
            messagebox.showwarning("","Your are about to cancel your registration!")
            if messagebox.askokcancel("","Confirm Cancel registration?"):

        ########## IF CLIENT WISH TO CANCEL REGISTRATION POLICY INPUT WILL BE TAGGED AS CANCELLED############
                con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                cur = con.cursor()
                try:
                    sql = "UPDATE tbl_policy SET POLICY_STATUS = 'CANCELLED' WHERE tbl_policy.POLICY_NUM = '" + str(Policynum) + "' "
                    cur.execute(sql)
                    con.commit()

                    messagebox.showinfo("","REGISTRATION CANCELLED!")
                    self.master8.withdraw()
                    self.home = Toplevel(self.master8)
                    self.app = MainWIndow(self.home)
                    cur.close()
                    con.close()

                except Exception as e:
                    messagebox.showerror("", str(e))
                    con.rollback()
                    con.close()


        ######################## WIDGET GUI#############################
        self.Policy_info_frame = LabelFrame(self.master8, text="Policy Information ", bg='#008631', fg='white', width=900, height=470)
        self.Policy_info_frame.place(x=15, y=10)

        PN_label = Label(self.Policy_info_frame, text="Policy Number:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        PN_label.place(x=10, y=10)
        PN = Label(self.Policy_info_frame,font=(11))
        PN.config(text=Policynum)
        PN.place(x=175, y=10)

        STATUS_LABEL= Label(self.Policy_info_frame, text="Status:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        STATUS_LABEL.place(x=560, y=10)
        STATUS = Label(self.Policy_info_frame,font=(11))
        STATUS.config(text=Policystatus)
        STATUS.place(x=630, y=10)

        PO_Name_label = Label(self.Policy_info_frame, text="Policy Owner Name:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        PO_Name_label.place(x=10, y=40)
        PO_Name = Label(self.Policy_info_frame, font=(11))
        PO_Name.config(text=fullname)
        PO_Name.place(x=175, y=40)

        PO_email_label = Label(self.Policy_info_frame, text="Email:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        PO_email_label .place(x=10, y=70)
        PO_email = Label(self.Policy_info_frame, font=(11))
        PO_email.config(text=email)
        PO_email.place(x=175, y=70)

        PO_contact_label = Label(self.Policy_info_frame, text="Contact:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        PO_contact_label.place(x=10, y=100)
        PO_contact = Label(self.Policy_info_frame, font=(11))
        PO_contact.config(text=contact)
        PO_contact.place(x=175, y=100)

        Policy_Name_label = Label(self.Policy_info_frame, text="Product Name:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        Policy_Name_label.place(x=10, y=130)
        Policy_Name = Label(self.Policy_info_frame, font=(11))
        Policy_Name.config(text=ProductName)
        Policy_Name.place(x=175, y=130)

        PO_Regdate_label = Label(self.Policy_info_frame, text="Registered Date:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        PO_Regdate_label.place(x=+560, y=130)
        PO_Regdate = Label(self.Policy_info_frame, font=(11))
        PO_Regdate.config(text=regDate)
        PO_Regdate.place(x=700, y=130)


        ################## PAYMENT WIDGET###################
        payment_frequecy = ["Monthly", "Quarterly", "SemiAnnual", "Annual"]
        payment_duration=["10-YEARS","5-YEARS","REGULAR"]
        getfrequency_type= StringVar()
        getpaymentduration=StringVar()

        Payment_label = Label(self.Policy_info_frame, text="Payment", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        Payment_label.place(x=10, y=185)

        Payment_duration_label = Label(self.Policy_info_frame, text="Payment Duration:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        Payment_duration_label.place(x=10, y=221)
        Payment_duration = ttk.Combobox(self.Policy_info_frame, width=35, values=payment_duration,textvariable=getpaymentduration)
        Payment_duration.place(x=175, y=221)


        Payment_frequency_label = Label(self.Policy_info_frame, text="Payment Frequency:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
        Payment_frequency_label.place(x=10, y=245)
        Payment_frequency =ttk.Combobox(self.Policy_info_frame, width=35, values=payment_frequecy,textvariable=getfrequency_type)
        Payment_frequency.place(x=175, y=245)

        Total_amount_label = Label(self.Policy_info_frame, text="Total", bg='#008631', fg='yellow',font=('Microsoft YaHei UI Light', 11,"bold"))
        Total_amount_label.place(x=10, y=270)

        Total_amount = Label(self.Policy_info_frame, bg='white', fg='Black',font=('Microsoft YaHei UI Light', 11, "bold"),width=10)
        Total_amount.place(x=175, y=270)


        Pay_button = Button(self.Policy_info_frame, text="Pay Now", font=('arial', 10), bg='white', fg='black', border=0, padx=15,command=Payfunction)
        Pay_button.place(x=70, y=320)
        Cancelregistration_button = Button(self.Policy_info_frame, text="Cancel Registration", font=('arial', 10 ),bg='white', fg='black', border=1, padx=15,command=cancelregistration)
        Cancelregistration_button.place(x=175, y=320)



######## Manage Accounts################  Policy_view_main
class Policy_view_main_admin:
    def __init__(self, master9):
        self.master9=master9
        self.master9.title("C.A.M.S v1.2022")
        self.master9.geometry("900x700")
        self.master9.config(bg='#008631')
        self.master9.resizable(False,False)
        ####### PN SEARCH or NAME SEARCH ##############

        searchthru = tk.StringVar(value="1") ### TEXT VARIABLE FOR RADIOBUTTON DEFAULT VALUE
        def disabler():
            if searchthru.get() == "1":
                fName_entry.delete(0, END)
                mName_entry.delete(0, END)
                lName_entry.delete(0, END)
                fName_entry.config(state=tk.DISABLED)
                mName_entry.config(state=tk.DISABLED)
                lName_entry.config(state=tk.DISABLED)
                PN_entry.config(state=tk.NORMAL)
                self.trv.delete(*self.trv.get_children())
                insertrecord()
            elif searchthru.get() == "0":
                PN_entry.delete(0, END)
                PN_entry.config(state=tk.DISABLED)
                fName_entry.config(state=tk.NORMAL)
                mName_entry.config(state=tk.NORMAL)
                lName_entry.config(state=tk.NORMAL)
                self.trv.delete(*self.trv.get_children())
                insertrecord()

        ##################### Treeview Functions##################################
        ######SEARCH IN TREEVIEW########
        def search():
            searchpolicy = Policynumber.get()
            fname = fnamevar.get()
            mname = mnamevar.get()
            lname = lnamevar.get()
        ##### SELECT QUERY####
            con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
            cur = con.cursor()

            ### QUERY FOR FETCH POLICY##
            sql = "SELECT POLICY_NUM,firstname,middlename,lastname from tbl_policy LEFT JOIN tbl_po ON POLICY_ID=PO_ID WHERE POLICY_NUM = '"+ searchpolicy +"' or lastname Like '"+lname+"' or firstname Like'"+fname+"' or middlename Like'" +mname+ "'"
            cur.execute(sql)
            policies = cur.fetchall()
            # print(policies)
            policy_list = []  ### declaration of list to append all policies extracted from tbl_policy
            for i in policies:  ##### Loop then append each item in the list every index from the tuple is in INT format
                policy_list.append(str(i[0]))  #### convert each item to STR before append in policy_list[]
                policy_list.append(str(i[1]))
                policy_list.append(str(i[2]))
                policy_list.append(str(i[3]))
            # print(policy_list)
            if searchpolicy in policy_list or fname in policy_list or mname in policy_list or lname in policy_list:  ########## checking policy input if exisiting in the list return Error if policy not found#####
                ######QUERY FOR TREEVIEW####
                sql1 ="SELECT * from tbl_policy LEFT JOIN tbl_po ON POLICY_ID=PO_ID WHERE POLICY_NUM= '" + searchpolicy + "' or lastname Like '" + lname + "' or firstname Like'" + fname + "' or middlename  Like'" + mname + "'"
                cur.execute(sql1)
                record = cur.fetchall()
                self.trv.delete(*self.trv.get_children())
                for x in record:
                    global my_tag
                    my_tag = ""
                    self.trv.tag_configure('active', background='lightgreen')
                    self.trv.tag_configure('pending', background='#f7e928')
                    self.trv.tag_configure('cancelled', background='#e05536')
                    self.trv.tag_configure('fullypaid', background='#73c0d1')
                    if x[2] == "ACTIVE":
                        my_tag = 'active'
                    elif x[2] == 'PENDING':
                        my_tag = 'pending'
                    elif x[2] == 'FULLY-PAID':
                        my_tag = 'fullypaid'

                    else:
                        my_tag = 'cancelled'

                    self.trv.insert("", 'end', id=x[0], text=x[0],
                                    values=(x[1], x[6], x[2], x[3], x[17], x[15], x[16]), tags=my_tag)
            else:
                self.trv.delete(*self.trv.get_children())
                messagebox.showerror("","Policy not found")


        #### FETCH RECORDS AND INSERT TO TREEVIEW DESIGNATE COLOR UPON INSERT#####
        def insertrecord():
            for x in records:
                global my_tag
                my_tag = ""
                self.trv.tag_configure('active', background='lightgreen')
                self.trv.tag_configure('pending', background='#f7e928')
                self.trv.tag_configure('cancelled', background='#e05536')
                self.trv.tag_configure('fullypaid', background='#73c0d1')

                if x[2] == "ACTIVE":
                    my_tag = 'active'
                elif x[2] == 'PENDING':
                    my_tag = 'pending'
                elif x[2] =='FULLY-PAID':
                    my_tag='fullypaid'
                else:
                    my_tag = 'cancelled'

                self.trv.insert("", 'end', id=x[0], text=x[0], values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6]),
                           tags=my_tag)

                #### SCROLL BAR######
                scrollbar = ttk.Scrollbar(self.trv_frame, orient='vertical', command=self.trv.yview)
                self.trv.configure(yscrollcommand=scrollbar.set)
                scrollbar.grid(row=1, column=2, sticky='ns')


        ### SELECT CLICK EVENT IN TREEVIEW####
        def click(a):
            a=0 ### setting positional argument value for proceed function
            global polnum,fullname,prodname,polstatus,regdate
            polnum = 0
            if self.trv.selection():
                selectrow=self.trv.item(self.trv.selection())
                #### get valus in TRV selected row display as dictionary######
                items=selectrow.get('values')
                polnum = items[0]
                prodname=items[1]
                polstatus=items[2]
                regdate=items[3]
                lname = items[4]
                fname = items[5]
                mname = items[6]
                fullname = fname + " " + mname + " " + lname
        # ##### DISPLAY SELECTED policy in treeview to LABEL below#####
                fullnameoutput_label.config(text=fullname)
                Productnameoutput_label.config(text=prodname)
                PNoutput_label.config(text=polnum)
                Registrationdateoutput_label.config(text=regdate)
            else:
                return polnum

        ###### PROCEED , CLEAR , HOME FUNCTION########
        def proceed():
            polnum=click(0)
            policy=0
            if policy==polnum:
                messagebox.showerror("","No policy input or selected")
            else:
                self.master9.withdraw()
                self.inputpolicyinsured = Toplevel(self.master9)
                self.app = Policy_view_selected(self.inputpolicyinsured)

        def clear():
            self.trv.delete(*self.trv.get_children())
            insertrecord()
            PN_entry.delete(0,END)
            fName_entry.delete(0,END)
            mName_entry.delete(0,END)
            lName_entry.delete(0,END)
            fullnameoutput_label.config(text="")
            Productnameoutput_label.config(text="")
            PNoutput_label.config(text="")
            Registrationdateoutput_label.config(text="")

        def home():
            self.master9.withdraw()
            self.home = Toplevel(self.master9)
            self.app = MainWIndow(self.home)

        ##################### WIDGETS  NAME AND POLICY SEARCH##########################
        self.frame = LabelFrame(self.master9, width=770, height=190, bg='#008631')
        self.frame.place(x=50,y=30)
        self.frame2 = LabelFrame(self.master9, width=765, height=220,bg='#008631')
        self.frame2.place(x=50, y=440)

        self.trv_frame = LabelFrame(self.master9, width=765, height=220, bg='#008631')
        self.trv_frame.place(x=50, y=230)


        ############## NAME SEARCH OR PN SEARCH WIDGET###########
        mainlabel = Label(self.frame, text="Search Thru: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 9, "bold"))
        mainlabel.place(x=0, y=2)
        PNlabel = Label(self.frame, text="PolicyNumber: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 10, "bold"))
        PNlabel.place(x=90, y=2)
        PN_radiobutton = tk.Radiobutton(self.frame, variable=searchthru, bg='#008631',value="1", command=disabler)
        PN_radiobutton.place(x=200, y=2)

        Namelabel = Label(self.frame, text="Name: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 10, "bold"))
        Namelabel.place(x=240, y=2)
        Name_radiobutton = tk.Radiobutton(self.frame, variable=searchthru, bg='#008631',value="0", command=disabler)
        Name_radiobutton.place(x=300,y=2)


        #### TEXT VARIABLE FOR TEXT BOX#####
        Policynumber=StringVar()
        fnamevar=StringVar()
        mnamevar=StringVar()
        lnamevar=StringVar()


        ### SEARCH SECTION and widgets ####
        PNlabel=Label(self.frame,text="Policy Number: ",bg='#008631',border=0,fg='white',font=('Microsoft YaHei UI Light',11,"bold"))
        PNlabel.place(x=0,y=35)
        PN_entry=Entry(self.frame,width=16, fg='black', border=0,font=4 ,textvariable=Policynumber)
        PN_entry.place(x=120,y=35)

        fNamelabel = Label(self.frame, text="FirstName: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light',11,"bold"))
        fNamelabel.place(x=0, y=65)
        fName_entry = Entry(self.frame, width=18, fg='black', border=0,font=4,textvariable=fnamevar)
        fName_entry.place(x=120,y=65)

        mnamelabel = Label(self.frame, text="MiddleName: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        mnamelabel.place(x=0, y=90)
        mName_entry = Entry(self.frame, width=18, fg='black', border=0, font=4, textvariable=mnamevar)
        mName_entry.place(x=120, y=90)

        lNamelabel = Label(self.frame, text="LastName: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        lNamelabel.place(x=0, y=115)
        lName_entry = Entry(self.frame, width=18, fg='black', border=0, font=4, textvariable=lnamevar)
        lName_entry.place(x=120, y=115)

        search_button=Button(self.frame,text="Search",padx=11,pady=2,bg="#4cafed",compound="left",font=("Arial",10,"bold"),fg="white",border=0,activebackground="#7fc4f0",command=search)
        search_button.place(x=120, y=150)

        ###############TREEVIEW###################

        self.trv=ttk.Treeview(self.trv_frame,columns=[1,2,3,4,5,6,7],show="headings",height="9")
        self.trv.bind('<Double-Button-1>',click)
        self.trv.grid(row=1, column=1)

        # width of columns and alignment
        self.trv.column("1", width=100, anchor='c')
        self.trv.column("2", width=150, anchor='c')
        self.trv.column("3", width=100, anchor='c')
        self.trv.column("4", width=100, anchor='c')
        self.trv.column("5", width=100, anchor='c')
        self.trv.column("6", width=100, anchor='c')
        self.trv.column("7", width=100, anchor='c')
        # Headings
        # respective columns
        self.trv.heading("1", text="Policy Number")
        self.trv.heading("2", text="Product Name")
        self.trv.heading("3", text="Policy Status")
        self.trv.heading("4", text="Registration date")
        self.trv.heading("5", text="LastName")
        self.trv.heading("6", text="FirstName")
        self.trv.heading("7", text="MiddleName")

        ###TREE VIEW QUERY###
        con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
        cur = con.cursor()
        treeviewquery = "SELECT POLICY_NUM,PRODUCT_NAME,POLICY_STATUS,REG_DATE,lastname,firstname,middlename FROM tbl_policy LEFT JOIN tbl_po ON POLICY_ID=PO_ID"
        cur.execute(treeviewquery)
        records = cur.fetchall()
        insertrecord()

        ################ SHOW POLICY BASIC INFO#############

        label=Label(self.frame2, text="Policy Number: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        label.place(x=10,y=40)
        PNoutput_label = Label(self.frame2, bg='white', border=0, fg='black',width=15,font=('Microsoft YaHei UI Light', 11, "bold"))
        PNoutput_label.place(x=150, y=40)

        fullname = Label(self.frame2, text="Full Name: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        fullname.place(x=10, y=70)
        fullnameoutput_label = Label(self.frame2, bg='white', border=0, fg='black', width=30,font=('Microsoft YaHei UI Light', 11, "bold"))
        fullnameoutput_label.place(x=150, y=70)

        Productname = Label(self.frame2, text="Product Name: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        Productname.place(x=10, y=100)
        Productnameoutput_label = Label(self.frame2, bg='white', border=0, fg='black', width=30,font=('Microsoft YaHei UI Light', 11, "bold"))
        Productnameoutput_label.place(x=150, y=100)

        Registrationdate = Label(self.frame2, text="Registration Date: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        Registrationdate.place(x=10, y=130)
        Registrationdateoutput_label = Label(self.frame2, bg='white', border=0, fg='black', width=15,font=('Microsoft YaHei UI Light', 11, "bold"))
        Registrationdateoutput_label.place(x=150, y=130)

        proceed_button=Button(self.frame2,text="Proceed",padx=19,pady=5,bg="#02a355",compound="left",font=("Arial",11,"bold"),fg="white",border=0,activebackground="lightgreen",command=proceed)
        proceed_button.place(x=580,y=30)

        clear_button = Button(self.frame2, text="Clear", padx=30, pady=5, bg="#a37002", compound="left",font=("Arial", 11, "bold"), fg="white", border=0, activebackground="#f7e06a",command=clear)
        clear_button.place(x=580, y=70)

        home_button = Button(self.frame2, text="Home", padx=28, pady=5, bg="#4cafed", compound="left",font=("Arial", 11, "bold"), fg="white", border=0, activebackground="#7fc4f0",command=home)
        home_button.place(x=580, y=110)

        disabler()

################################################### END Policy_view_main_admin  ###########################################################################


################################################## START LINE GRAPH / GENERATE REPORT#####################################################################################
class Reports:
    def __init__(self, master11):
        self.master11=master11
        self.master11.title("C.A.M.S v1.2022/REPORTS")
        self.master11.geometry("450x200")
        self.master11.config(bg='#008631')
        self.master11.resizable(False,False)

        def home():  #### RETURN HOME PAGE#####
            self.master11.withdraw()
            self.home = Toplevel(self.master11)
            self.app = MainWIndow(self.home)

        ## DATES AND DEFAULT VALUE
        self.Jan = 0
        self.Feb = 0
        self.Mar = 0
        self.Apr = 0
        self.May = 0
        self.Jun = 0
        self.Jul = 0
        self.Aug = 0
        self.Sep = 0
        self.Oct = 0
        self.Nov = 0
        self.Dec = 0

        ### QUERY TO EXTRACT POLICIES FROM DB
        def policy_counter():
            global policy_list
            con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
            cur = con.cursor()
            treeviewquery = "SELECT REG_DATE FROM tbl_policy "
            cur.execute(treeviewquery)
            policies = cur.fetchall()
            policy_list=[]
            for a in policies:
                policy_list.append(a)
            return policy_list

        ### DICT VARIABLE
        value = {"Jan-2023": 0, "Feb-2023": 0, "Mar-2023": 0, "Apr-2023": 0, "May-2023": 0,
                 "Jun-2023": 0, "Jul-2023": 0, "Aug-2023": 0, "Sep-2023": 0, "Oct-2023": 0,
                 "Nov-2023": 0, "Dec-2023": 0}


        def display_graph(event=None):
            policy_list=policy_counter()
            ## ONCE POLICIES ARE EXTRACTED I LOOP IT TO GET THE VALUE OF THE LIST TO IDENTIFY THE MONTH PER REGISTRATION DATE OF THE POLICIES
            for x in policy_list:
                for i in x:
                    date_string = str(i)
                    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
                    month = date.month

                    if month == 1:
                        value["Jan-2023"] += 1
                    elif month == 2:
                        value["Feb-2023"] += 1
                    elif month == 3:
                        value["Mar-2023"] += 1
                    elif month == 4:
                        value["Apr-2023"] += 1
                    elif month == 5:
                        value["May-2023"] += 1
                    elif month == 6:
                        value["Jun-2023"] += 1
                    elif month == 7:
                        value["Jul-2023"] += 1
                    elif month == 8:
                        value["Aug-2023"] += 1
                    elif month == 9:
                        value["Sep-2023"] += 1
                    elif month == 10:
                        value["Oct-2023"] += 1
                    elif month == 11:
                        value["Nov-2023"] += 1
                    elif month == 12:
                        value["Dec-2023"] += 1

            ### ONCE VALUE PER DATE IS EXTRACTED FROM DB THE FF ARE TO GENERATE THE REPORT AND PLOT THE VALUES
            ## THE REPORT CAN BE GENERATED AS A COMPARISON THIS WILL BE IDENTIFIED BASE ON 2 SELECTED DATES FOR COMPARISON
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 5))
            fig.tight_layout()

            # Get selected dates from comboboxes
            selected_date_1 = date_var_1.get()
            selected_date_2 = date_var_2.get()

            # Plot first bar graph
            ax1.bar(selected_date_1, value[selected_date_1], color='#0eb052')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Value')
            ax1.set_title(f'Policy Registered')
            ax1.set_ylim(0, 20)
            ax1.set_yticks(range(0, 21, 1))

            # Plot second bar graph
            ax2.bar(selected_date_2, value[selected_date_2], color='#078ba6')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Value')
            ax2.set_title(f'Policy Registered')
            ax2.set_ylim(0, 20)
            ax2.set_yticks(range(0, 21, 1))

            report= Toplevel()
            report.title("Reports")
            report.geometry("600x600")
            canvas = FigureCanvasTkAgg(fig, master=report)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            ###### FUNCTION TO SAVE REPORT AS PDF ######
            def save_as_pdf():
                with PdfPages('C:/Users/JoshuaPC/Desktop/mainprojectbackup2/reports/report.pdf') as pdf:

                    pdf.savefig(fig)
                messagebox.showinfo("","Report saved Successfully!")

            button = Button(report, text="Save as PDF",command = save_as_pdf)
            button.pack()


        ########## STRING VARIABLES
        date_var_1 = tk.StringVar()
        date_var_1.set("Jan-2023")  # default value
        date_var_2 = tk.StringVar()
        date_var_2.set("Feb-2023")  # default value
        # Create first combobox

        comparedate_label = Label(self.master11, text="Compare Dates: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 10, "bold"))
        comparedate_label.place(x=160, y=20)

        combobox_1 = tk.ttk.Combobox(self.master11, textvariable=date_var_1, values=list(value.keys()))
        combobox_1.place(x=60,y=60)
        # Create second combobox
        combobox_2 = tk.ttk.Combobox(self.master11, textvariable=date_var_2, values=list(value.keys()))
        combobox_2.place(x=240,y=60)

        # Create button to display graphs
        display_button = tk.Button(self.master11, text="Generate", bg="#1c8c27", compound="left",font=("Arial", 11), fg="white", border=1, activebackground="#076e11",command=display_graph)
        display_button.place(x=130,y=100)
        # Home Button for Exit
        home_button = Button(self.master11, text="Exit",padx=15, bg="#ad322a", compound="left",font=("Arial", 11), fg="white", border=1, activebackground="#940c03", command=home)
        home_button.place(x=220, y=100)

############################################################## END REPORTS ##########################################################################


class Policy_view_selected():
    def __init__(self, master):
        self.master10=master
        self.master10.title("C.A.M.S /Policy Selected Main")
        self.master10.geometry("1100x650")
        self.master10.config(bg='#008631')
        self.master10.resizable(False,False)

        def home():  #### RETURN HOME PAGE#####
            self.master10.withdraw()
            self.home = Toplevel(self.master10)
            self.app = MainWIndow(self.home)
        def Back():
            self.master10.withdraw()
            self.home = Toplevel(self.master10)
            self.app = Policy_view_main_admin(self.home)

        #################START OF POLICY INFO BUTTON ###################
        def Policyinfo():
            self.Policyinfo_window = Toplevel()
            self.Policyinfo_window.title("C.A.M.S /Policy Information")
            self.Policyinfo_window.geometry("300x230")
            self.Policyinfo_window.config(bg='#008631')
            self.Policyinfo_window.resizable(False, False)

            def view_policy():
                self.policy=Policynumber.get()
                if self.policy==""or self.policy=="0" or self.policy==None:
                    messagebox.showerror("", "No Policy Found")
                else:
                    self.checkpolicy_window = Toplevel()
                    self.checkpolicy_window.title("C.A.M.S /Check Policy view")
                    self.checkpolicy_window.geometry("700x500")
                    self.checkpolicy_window.config(bg='#008631')
                    self.checkpolicy_window.resizable(False, False)

                    #### START CHECK POLICY ############
                    policy_status=['ACTIVE','PENDING','CANCELLED']
                    policy_type=['Traditional Life Plan','Insurance with investment Plan']
                    product_name=['Manu Edge Classic','Manu Protect at 65','ManuHorizon','Affluence Builder','Manu Affluence Elite']

                    POLSTATUSVAR=StringVar()
                    POLINSTYPE=StringVar()
                    PRODNAME=StringVar()
                    PLANDURATION=StringVar()
                    PLANCOVERAGE=StringVar()

                    def policy_show():
                        con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                        cur = con.cursor()
                        query = "SELECT POLICY_NUM,POLICY_STATUS,PRODUCT_NAME,INS_TYPE,PRODUCT_DURATION,COVERAGE_AMOUNT from tbl_policy  where POLICY_NUM='" + self.policy + "'"
                        cur.execute(query)
                        get= cur.fetchall()
                        get_polnum=get[0][0] ## extract policy from the select query
                        con.close()
                        self.POLNUM_OUTPUT.config(text=get_polnum)
                        global pol_status,pol_product,pol_type,pol_dur,pol_cov
                        for i in get:
                            pol_status=i[1]
                            pol_product=i[2]
                            pol_type=i[3]
                            pol_dur=i[4]
                            pol_cov=i[5]
                        delete_data()
                        insert_data()


                    def insert_data():
                        self.POLSTATUS_ENTRY.insert(0, pol_status)
                        self.POLINSTYPE_ENTRY.insert(0, pol_type)
                        self.PRODNAME_ENTRY.insert(0, pol_product)
                        self.PLANDUR_ENTRY.insert(0, pol_dur)
                        self.PLANCOV_ENTRY.insert(0, pol_cov)

                    def delete_data():
                        deleterider()
                        self.POLSTATUS_ENTRY.delete(0,END)
                        self.POLINSTYPE_ENTRY.delete(0,END)
                        self.PRODNAME_ENTRY.delete(0, END)
                        self.PLANDUR_ENTRY.delete(0, END)
                        self.PLANCOV_ENTRY.delete(0, END)

                    def updatepolicyquery():
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql1 = "UPDATE tbl_policy join tbl_rider on POLICY_ID = RIDER_ID_FK  SET POLICY_STATUS =%s, PRODUCT_NAME =%s,INS_TYPE =%s,PRODUCT_DURATION =%s ,COVERAGE_AMOUNT=%s,RIDER_COVERAGE=%s WHERE POLICY_NUM= %s"
                        val1 = (update_status, update_prodname, update_instype, update_plan_duration, update_plan_coverage,update_plan_coverage,self.policy)
                        cur.execute(sql1, val1)
                        messagebox.showinfo("", "Policy Information Updated!")
                        con.commit()

                    def insert_update_info():
                        global update_status,update_instype,update_prodname,update_plan_duration,update_plan_coverage,policycoverage,ecicov
                        update_status=POLSTATUSVAR.get()
                        update_instype=POLINSTYPE.get()
                        update_prodname=PRODNAME.get()
                        update_plan_duration=PLANDURATION.get()
                        update_plan_coverage=PLANCOVERAGE.get()
                        policycoverage=int(update_plan_coverage)
                        ecicov=policycoverage/2

                        messagebox.showwarning("", "You are about to update Policy?")
                        if messagebox.askyesno("", "Proceed with the update?"):
                            if policycoverage < 300000:
                                messagebox.showerror("", "Benefit limit to PHP 300,000")
                            else:
                                if update_prodname=="Manu Protect at 65":
                                    if update_plan_duration != "65.0":
                                        messagebox.showerror("", "Duration should be 65 years")
                                    else:
                                        updatepolicyquery()
                                else:
                                    updatepolicyquery()
                        else:
                            policy_show()

                    self.checkpolicy_result_frame=LabelFrame(self.checkpolicy_window,width=680,height=480,bg='#008631')
                    self.checkpolicy_result_frame.place(x=5,y=5)

                    self.POLNUM_LABEL = Label(self.checkpolicy_result_frame, text="POLICY NUMBER: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.POLNUM_LABEL.place(x=15, y=15)
                    self.POLNUM_OUTPUT = Label(self.checkpolicy_result_frame,width=15, bg='white', border=0, fg='black', font=('ARIAL', 10, "bold"))
                    self.POLNUM_OUTPUT.place(x=155, y=18)

                    self.POLSTATUS_LABEL = Label(self.checkpolicy_result_frame, text="POLICY STATUS: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.POLSTATUS_LABEL.place(x=290, y=15)
                    self.POLSTATUS_ENTRY =Entry(self.checkpolicy_result_frame,width=15, bg='white', border=0, fg='black',font=('ARIAL', 10, "bold"),textvariable=POLSTATUSVAR)
                    self.POLSTATUS_ENTRY.place(x=420, y=18)
                    self.addresstype_combobox = ttk.Combobox(self.checkpolicy_result_frame, width=13,values=policy_status, textvariable=POLSTATUSVAR)
                    self.addresstype_combobox.place(x=540, y=16)

                    self.POLINSTYPE_LABEL = Label(self.checkpolicy_result_frame, text="INSURANCE TYPE: ", bg='white',border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.POLINSTYPE_LABEL.place(x=15, y=60)
                    self.POLINSTYPE_ENTRY = Entry(self.checkpolicy_result_frame, width=40, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=POLINSTYPE)
                    self.POLINSTYPE_ENTRY.place(x=160, y=63)
                    self.polinstype_combobox = ttk.Combobox(self.checkpolicy_result_frame, width=18,values=policy_type, textvariable=POLINSTYPE)
                    self.polinstype_combobox.place(x=450, y=61)

                    self.PRODNAME_LABEL = Label(self.checkpolicy_result_frame, text="PRODUCT: ", bg='white',border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.PRODNAME_LABEL.place(x=60, y=90)
                    self.PRODNAME_ENTRY = Entry(self.checkpolicy_result_frame, width=40, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=PRODNAME)
                    self.PRODNAME_ENTRY.place(x=160, y=93)
                    self.prodname_combobox = ttk.Combobox(self.checkpolicy_result_frame, width=18, values=product_name,textvariable=PRODNAME)
                    self.prodname_combobox.place(x=450, y=91)

                    self.PLANDUR_LABEL= Label(self.checkpolicy_result_frame, text="DURATION: ", bg='white',border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.PLANDUR_LABEL.place(x=60, y=120)
                    self.PLANDUR_ENTRY = Entry(self.checkpolicy_result_frame, width=15, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=PLANDURATION)
                    self.PLANDUR_ENTRY.place(x=160, y=123)

                    self.PLANCOV_LABEL = Label(self.checkpolicy_result_frame, text="PLAN COVERAGE: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.PLANCOV_LABEL.place(x=15, y=150)
                    self.PLANCOV_ENTRY = Entry(self.checkpolicy_result_frame, width=20, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=PLANCOVERAGE)
                    self.PLANCOV_ENTRY.place(x=160, y=153)

                    self.suplemental_LABEL = Label(self.checkpolicy_result_frame, text="SUPPLEMENTAL BENEFIT: ", bg='#008631',border=0, fg='white', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.suplemental_LABEL.place(x=15, y=180)



                    #### RIDER SELECTION VARIABLES###
                    RIDER_ROW_VAR = StringVar()
                    RIDER_NAME = StringVar()
                    RIDER_COVERAGE = StringVar()
                    rider_list = ["Accidental Death Benefit", "Enhance Critical Illness", "Total Disability Waiver",
                                  "Term Life Benefit", "Hospital Income Benefit"]
                    ### RIDER TREEVIEW FRAME#####
                    self.riderframe = Frame(self.checkpolicy_result_frame, width=500, height=150)
                    self.riderframe.place(x=15, y=210)


                    ### RIDER TREEVIEW###
                    def rider_show():  ### FUCNTION to EXTRACT RIDER FROM DB TO INSERT VALUES NEEDED IN THE TREEVIEW BELOW
                        con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                        cur = con.cursor()
                        query = "select * from tbl_rider RIGHT join tbl_policy on POLICY_ID=RIDER_ID_FK where POLICY_NUM='" + self.policy + "'"
                        cur.execute(query)
                        getrider = cur.fetchall()
                        con.commit()
                        con.close()
                        global ID
                        ID = 1 ## DECLARATION OF TEMPORARY ID
                        for x in getrider: ### LOOP AFTER THE EXTRACTION TO INSERT VALUES TO TREEVIEW
                            self.trvrider.insert("", 'end', id=x[1], text=x[0],values=(x[0], ID , x[1], x[7]))
                            ID = ID + 1 ### INCREMENT OF ID

                    ### TREEVIEW###
                    self.trvrider = ttk.Treeview(self.riderframe, columns=[1, 2, 3, 4], show="headings", height="7")
                    self.trvrider.grid(row=0, column=0, sticky='n')
                    # width of columns and alignment
                    self.trvrider.column("1", width=80, anchor='c')
                    self.trvrider.column("2", width=80, anchor='c')
                    self.trvrider.column("3", width=200, anchor='c')
                    self.trvrider.column("4", width=120, anchor='c')
                    # Headings
                    # respective columns
                    self.trvrider.heading("1", text="ROW NO.")
                    self.trvrider.heading("2", text="ID")
                    self.trvrider.heading("3", text="RIDER NAME")
                    self.trvrider.heading("4", text="COVERAGE")

                    def update_rider_query():
                        global ridernameget,ridercov
                        ridernameget = RIDER_NAME.get()
                        ridercov = RIDER_COVERAGE.get()
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbl_rider join tbl_policy on POLICY_NUM =%s SET RIDER=%s,RIDER_COVERAGE=%s  WHERE RIDER_ID=%s"
                        val2 = (self.policy,ridernameget,ridercov,riderrow)
                        cur.execute(sql2,val2)

                        messagebox.showinfo("", "Rider Updated!")
                        con.commit()

                    def insert_update_query():
                        try:
                            benefit_amount=PLANCOVERAGE.get()
                            ridercov = RIDER_COVERAGE.get()
                            ecilimit=int(benefit_amount)/2
                            if ridernameget=="Accidental Death Benefit":
                                if ridercov != benefit_amount:
                                    messagebox.showerror("","ADB coverage cannot be different from POLICY COVERAGE")
                                else:
                                    update_rider_query()
                            elif ridernameget == "Enhance Critical illness":
                                if ecilimit<int(ridercov):
                                    messagebox.showerror("", "ECI coverage cannot be more than limit"+" "+ str(ecilimit))
                                else:
                                    update_rider_query()
                            else:
                                update_rider_query()
                        except:
                            messagebox.showerror("","No Rider Selected")


                    def select_rider(): #### PURPOSE OF THIS QUERY IS TO POPULATE ENTRY BOXES BELOW ONCE CLIENT ENTER A ROW NUMBER IN THE TEXT BOX###
                        try:
                            global rownumget, idget, ridernameget, ridercoverageget, riderrow
                            riderrow=RIDER_ROW_VAR.get()
                            con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                            cur = con.cursor()
                            sql = "select * from tbl_rider left join tbl_policy on policy_id=RIDER_ID_FK where POLICY_NUM='"+self.policy+"' and RIDER_ID='"+riderrow+"'"
                            cur.execute(sql)
                            rideritems = cur.fetchall()
                            for i in rideritems:
                                rownumget=i[0]
                                ridernameget=i[1]
                                ridercoverageget=i[7]

                            deleterider()
                            insertrider()
                        except:
                            messagebox.showerror("","Invalid Row!")

                    def insertrider():
                        self.RIDER_ROWNO_LABEL_OUTPUT.config(text=rownumget)
                        self.RIDER_ENTRY.insert(0,ridernameget)
                        self.COVERAGE_ENTRY.insert(0,ridercoverageget)

                    def deleterider():
                        self.RIDER_ROWNO_LABEL_OUTPUT.config(text="")
                        self.RIDER_ENTRY.delete(0, END)
                        self.COVERAGE_ENTRY.delete(0, END)


                    self.RIDER_ROWNO_LABEL = Label(self.checkpolicy_result_frame, text="Row No:", bg='#008631',border=0, fg="white", font=('ARIAL', 10, "bold"))
                    self.RIDER_ROWNO_LABEL.place(x=30, y=380)
                    self.RIDER_ROWNO_LABEL_OUTPUT = Label(self.checkpolicy_result_frame,width=8, bg='white',border=0, fg="black", font=('ARIAL', 10, "bold"))
                    self.RIDER_ROWNO_LABEL_OUTPUT.place(x=90, y=380)

                    self.RIDER_LABEL = Label(self.checkpolicy_result_frame, text="Rider: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.RIDER_LABEL.place(x=30, y=410)
                    self.RIDER_ENTRY = Entry(self.checkpolicy_result_frame, width=30, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=RIDER_NAME)
                    self.RIDER_ENTRY.place(x=80, y=411)
                    self.prodname_combobox = ttk.Combobox(self.checkpolicy_result_frame, width=30, values=rider_list,textvariable=RIDER_NAME)
                    self.prodname_combobox.place(x=300, y=409)

                    self.COVERAGE_LABEL = Label(self.checkpolicy_result_frame, text="Coverage Amount: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 10, "bold"))
                    self.COVERAGE_LABEL.place(x=30, y=440)
                    self.COVERAGE_ENTRY = Entry(self.checkpolicy_result_frame, width=15, bg='white', border=0, fg='black',font=('ARIAL', 10, "bold"), textvariable=RIDER_COVERAGE)
                    self.COVERAGE_ENTRY.place(x=170, y=440)
                    policy_show()  #### COMMAND TO SHOW POLICY DETAILS AND POPULATE ITEMS ABOVE
                    rider_show() #### COMMAND TO SHOW RIDER DETAILS AND POPULATE ITEMS IN TREEVIEW and widgets below


                    ### LOWER WIDGET FOR UDPATE RIDER####
                    self.RIDER_ROW_LABEL = Label(self.checkpolicy_result_frame, text="Rider Row:", bg='#008631', border=0, fg="white", font=('ARIAL', 10, "bold"))
                    self.RIDER_ROW_LABEL.place(x=530, y=200)
                    self.RIDER_ROW_ENTRY = Entry(self.checkpolicy_result_frame, width=15, bg='white', border=0,fg='black', font=('ARIAL', 10, "bold"), textvariable=RIDER_ROW_VAR)
                    self.RIDER_ROW_ENTRY.place(x=530, y=220)

                    update_button = Button(self.checkpolicy_result_frame, text="Update Policy ", font=('arial', 10), bg='#eb9e34',fg='white', border=0, padx=15, command=insert_update_info)
                    update_button.place(x=360, y=150)

                    select_button = Button(self.checkpolicy_result_frame, text="Select", font=('arial', 8), bg='white',fg='black', border=0, padx=5, command=select_rider)
                    select_button.place(x=530, y=240)
                    update_button_rider = Button(self.checkpolicy_result_frame, text="UPDATE ", font=('arial', 10),bg='white', fg='black', border=0, padx=15, command=insert_update_query)
                    update_button_rider.place(x=530, y=270)
                    clear_button = Button(self.checkpolicy_result_frame, text="CLEAR", font=('arial', 10), bg='white',fg='black', padx=22, border=0, command=policy_show)
                    clear_button.place(x=530, y=300)
                    delete_button = Button(self.checkpolicy_result_frame, text="DELETE", font=('arial', 10), bg='white',fg='black', padx=18, border=0, command=policy_show)
                    delete_button.place(x=530, y=330)
        ######################### END IF CHECK POLICY  ###############################################

        ######## START OF CHECK POLICY OWNER #######
            def view_po():
                self.policy = Policynumber.get()
                if self.policy == "" or self.policy == "0" or self.policy == None:
                    messagebox.showerror("", "No Policy Found")
                else:
                    self.checkpolicyowner_window = Toplevel()
                    self.checkpolicyowner_window.title("C.A.M.S /Check Policy Owner details view")
                    self.checkpolicyowner_window.geometry("600x320")
                    self.checkpolicyowner_window.config(bg='#008631')
                    self.checkpolicyowner_window.resizable(False, False)

                    def show_podetails():
                        con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                        cur = con.cursor()
                        querypo = "SELECT * FROM `tbl_po` join tbl_policy on PO_ID=POLICY_ID where POLICY_NUM ='" + self.policy + "'"
                        cur.execute(querypo)
                        getpo = cur.fetchall()
                        # print(getpo)

                        f_name=getpo[0][1]
                        m_name=getpo[0][2]
                        l_name=getpo[0][3]
                        age=getpo[0][4]
                        b_day=getpo[0][5]
                        po_gender=getpo[0][6]
                        po_profession=getpo[0][7]
                        po_cstatus=getpo[0][8]

                        self.first_namepo_entry.delete(0,END)
                        self.middle_namepo_entry.delete(0,END)
                        self.last_namepo_entry.delete(0,END)
                        self.agepo_entry.delete(0,END)
                        self.genderpo_entry.delete(0,END)
                        self.professionpo_combobox.set(value="")
                        self.civilpo_status_combobox.set(value="")
                        cal.delete(0,END)
                        self.first_namepo_entry.insert(0,f_name)
                        self.middle_namepo_entry.insert(0,m_name)
                        self.last_namepo_entry.insert(0,l_name)
                        self.agepo_entry.insert(0,age)
                        cal.insert(0,b_day)
                        self.genderpo_entry.insert(0,po_gender)
                        self.professionpo_combobox.insert(0,po_profession)
                        self.civilpo_status_combobox.insert(0,po_cstatus)


                    def update_po_query():
                        pofname=POFNAMEVAR.get()
                        pomname=POMNAMEVAR.get()
                        polname=POLNAMEVAR.get()
                        poage=POAGEVAR.get()
                        pobday=POBDAY.get()
                        pogender=POGENDER.get()
                        poprofession=POPROFESSION.get()
                        pocstatus=POCSTATUS.get()
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbl_policy join tbl_po  on POLICY_ID=PO_ID  SET firstname=%s,middlename=%s,lastname=%s,age=%s,birthday=%s,gender=%s,profession=%s,civilstatus=%s  WHERE POLICY_NUM=%s"
                        val2 = (pofname, pomname, polname, poage,pobday,pogender,poprofession,pocstatus,self.policy)
                        cur.execute(sql2, val2)
                        con.commit()
                        messagebox.showinfo("", "Policy Owners Info Updated!")

                    def insert_po_update():
                        pofname = POFNAMEVAR.get()
                        pomname = POMNAMEVAR.get()
                        polname = POLNAMEVAR.get()
                        poage = POAGEVAR.get()
                        pobday = POBDAY.get()
                        pogender = POGENDER.get()
                        poprofession = POPROFESSION.get()
                        pocstatus = POCSTATUS.get()
                        messagebox.showwarning("","You are about to update Policy Owners Info?")
                        if messagebox.askyesno("","Proceed on update?"):
                            if pofname == "" or pomname == "" or polname == "" or poage =="" or pobday == "" or pocstatus == "" or poprofession == "" or pogender=="":
                                messagebox.showerror("", "Some fields are missing in Client info")
                            else:
                                update_po_query()
                        else:
                            show_podetails()


                    ############## TEXT VARIABLE ##################
                    POFNAMEVAR=StringVar()
                    POMNAMEVAR=StringVar()
                    POLNAMEVAR=StringVar()
                    POAGEVAR=StringVar()
                    POBDAY=StringVar()
                    POGENDER=StringVar()
                    POPROFESSION=StringVar()
                    POCSTATUS=StringVar()

                    # ########################## Client info ###################################################
                    self.user_info_frame = LabelFrame(self.checkpolicyowner_window, text="Policy Owner Information", bg='#008631', fg='white',width=560, height=300)
                    self.user_info_frame.place(x=10, y=10)
                    ##########Name############
                    self.first_name_label = Label(self.user_info_frame, text="First Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.first_name_label.place(x=40,y=30)
                    self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.middle_name_label.place(x=220, y=30)
                    self.last_name_label = Label(self.user_info_frame, text="Last Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.last_name_label.place(x=400,y=30)

                    self.first_namepo_entry = Entry(self.user_info_frame, width=20,textvariable=POFNAMEVAR)
                    self.middle_namepo_entry = Entry(self.user_info_frame, width=20,textvariable=POMNAMEVAR)
                    self.last_namepo_entry = Entry(self.user_info_frame, width=20,textvariable=POLNAMEVAR)
                    self.first_namepo_entry.place(x=20,y=60)
                    self.middle_namepo_entry.place(x=200,y=60)
                    self.last_namepo_entry.place(x=380,y=60)

                    # ##########AGE ############
                    self.agepo_label = Label(self.user_info_frame, text="Age", bg='#008631', fg='white', font=('Microsoft YaHei UI Light', 11))
                    self.agepo_label.place(x=60,y=90)
                    self.agepo_entry = Entry(self.user_info_frame,width=10,textvariable=POAGEVAR )
                    self.agepo_entry.place(x=45,y=120)

                    # ########## BDAY############
                    self.birthdaypo_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.birthdaypo_label.place(x=220,y=90)
                    cal = DateEntry(self.user_info_frame, date_pattern="yyyy-mm-dd",textvariable=POBDAY)
                    cal.place(x=210,y=120)

                    # ##########GENDER############
                    self.Genderpo = Label(self.user_info_frame, text="Gender", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.Genderpo.place(x=410,y=90)
                    self.genderpo_entry = Entry(self.user_info_frame, width=15,textvariable=POGENDER)
                    self.genderpo_entry.place(x=390,y=120)

                    # ##########Profession############
                    profession = ["Accountant", "Actor/Actress", "Aircraft pilot", "Software Engineer", "Librarian",
                                  "Architect", "Artist", "Barber", "Bricklayer", "Business Person", "Butcher", "Chef",
                                  "Cleaner", "Construction worker", "Corporate Secretary", "Dentist", "Designer", "Driver",
                                  "Electrician", "Engineer",
                                  "Farmer", "Fire Fighter", "Fisherman", "Gardener", "Hair Dresser",
                                  "House Pinter and Decorator", "Journalist", "Judge", "Lawyer", "Lifeguard",
                                  "Mail Carrier", "Mechanic", "Model", "Nurse", "Personal Assistant", "Cashier",
                                  "Pharmacist", "Photographer", "Physician",
                                  "Plumber", "Police officer", "Politician", "Realstate Broker", "Salesperson", "Scientist",
                                  "Sea Farer", "Software Developer", "Soldier", "Tailor", "Teacher", "Technician",
                                  "Veterinarian", "Waiter", "Web Developer", "Worker", "Others not specified"]

                    def search(event):
                        self.professionpo_combobox.set("")
                        value = event.widget.get()
                        if value == "":
                            self.professionpo_combobox['value'] = profession
                        else:
                            data = []
                            for item in profession:
                                if value.lower() in item.lower():
                                    data.append(item)
                            self.professionpo_combobox['values'] = data

                    self.profession_label = Label(self.user_info_frame, text="Profession", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.professionpo_combobox = ttk.Combobox(self.user_info_frame, width=23, values=profession,textvariable=POPROFESSION)
                    self.profession_label.place(x=40,y=150)
                    self.professionpo_combobox.place(x=10,y=180)
                    self.professionpo_combobox.bind('<Button-1>', search)
                    self.professionpo_combobox.bind('<KeyRelease>', search)

                    # ##########Civil Status############
                    sts = ['Single', 'Married', 'Widowed', 'Annulled']
                    self.statuspo_label = Label(self.user_info_frame, text="Civil Status", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.civilpo_status_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts,textvariable=POCSTATUS)
                    self.civilpo_status_combobox.set("")
                    self.statuspo_label.place(x=220,y=150)
                    self.civilpo_status_combobox.place(x=190,y=180)
                    show_podetails()

                    update_button_po = Button(self.user_info_frame, text="UPDATE ", font=('arial', 10),bg='white', fg='black', border=0, padx=15, command=insert_po_update)
                    update_button_po.place(x=160, y=240)
                    clear_button_po = Button(self.user_info_frame, text="CLEAR", font=('arial', 10), bg='white',fg='black', padx=22, border=0, command=show_podetails)
                    clear_button_po.place(x=270, y=240)
                ####################################### END OF POLICY OWNER VIEW #######################################################

            ############################### START OF POLICY INSURED VIEW ##########
            def view_ins():
                self.policy = Policynumber.get()
                if self.policy == "" or self.policy == "0" or self.policy == None:
                    messagebox.showerror("", "No Policy Found")
                else:
                    self.checkpolicyinsured_window = Toplevel()
                    self.checkpolicyinsured_window.title("C.A.M.S /Check Policy Insured details view")
                    self.checkpolicyinsured_window.geometry("600x320")
                    self.checkpolicyinsured_window.config(bg='#008631')
                    self.checkpolicyinsured_window.resizable(False, False)

                    def show_insdetails():
                        con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                        cur = con.cursor()
                        queryins = "SELECT * FROM `tbl_insured` join tbl_policy on INS_ID=POLICY_ID where POLICY_NUM ='" + self.policy + "'"
                        cur.execute(queryins)
                        getins = cur.fetchall()
                        # print(getins)
                        insf_name = getins[0][1]
                        insm_name = getins[0][2]
                        insl_name = getins[0][3]
                        insage = getins[0][4]
                        insb_day = getins[0][5]
                        ins_gender = getins[0][6]
                        ins_profession = getins[0][7]
                        ins_cstatus = getins[0][8]

                        self.first_nameins_entry.delete(0, END)
                        self.middle_nameins_entry.delete(0, END)
                        self.last_nameins_entry.delete(0, END)
                        self.ageins_entry.delete(0, END)
                        self.genderins_entry.delete(0, END)
                        self.professionins_combobox.set(value="")
                        self.civilins_status_combobox.set(value="")
                        cal.delete(0, END)
                        self.first_nameins_entry.insert(0, insf_name)
                        self.middle_nameins_entry.insert(0, insm_name)
                        self.last_nameins_entry.insert(0, insl_name)
                        self.ageins_entry.insert(0, insage)
                        cal.insert(0, insb_day)
                        self.genderins_entry.insert(0, ins_gender)
                        self.professionins_combobox.insert(0, ins_profession)
                        self.civilins_status_combobox.insert(0, ins_cstatus)

                    def update_ins_query():
                        insfname = INSFNAMEVAR.get()
                        insmname = INSMNAMEVAR.get()
                        inslname = INSLNAMEVAR.get()
                        insage = INSAGEVAR.get()
                        insbday = INSBDAY.get()
                        insgender = INSGENDER.get()
                        insprofession = INSPROFESSION.get()
                        inscstatus = INSCSTATUS.get()
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbl_policy join tbl_insured  on POLICY_ID=INS_ID  SET firstname=%s,middlename=%s,lastname=%s,age=%s,birthday=%s,gender=%s,profession=%s,civilstatus=%s  WHERE POLICY_NUM=%s"
                        val2 = (insfname, insmname, inslname, insage, insbday, insgender, insprofession, inscstatus, self.policy)
                        cur.execute(sql2, val2)
                        con.commit()
                        messagebox.showinfo("", "Policy Insured Info Updated!")

                    def insert_ins_update():
                        insfname = INSFNAMEVAR.get()
                        insmname = INSMNAMEVAR.get()
                        inslname = INSLNAMEVAR.get()
                        insage = INSAGEVAR.get()
                        insbday = INSBDAY.get()
                        insgender = INSGENDER.get()
                        insprofession = INSPROFESSION.get()
                        inscstatus = INSCSTATUS.get()
                        messagebox.showwarning("", "You are about to update Policy Insured Info?")
                        if messagebox.askyesno("", "Proceed on update?"):
                            if insfname == "" or insmname == "" or inslname == "" or insage == "" or insbday == "" or insgender == "" or insprofession == "" or inscstatus == "":
                                messagebox.showerror("", "Some fields are missing in Client info")
                            else:
                                update_ins_query()
                        else:
                            show_insdetails()

                    ############## TEXT VARIABLE ##################
                    INSFNAMEVAR = StringVar()
                    INSMNAMEVAR = StringVar()
                    INSLNAMEVAR = StringVar()
                    INSAGEVAR = StringVar()
                    INSBDAY = StringVar()
                    INSGENDER = StringVar()
                    INSPROFESSION = StringVar()
                    INSCSTATUS = StringVar()

                    # ########################## Client info ###################################################
                    self.user_info_frame = LabelFrame(self.checkpolicyinsured_window, text="Policy Owner Information",bg='#008631', fg='white', width=560, height=300)
                    self.user_info_frame.place(x=10, y=10)
                    ##########Name############
                    self.first_name_label = Label(self.user_info_frame, text="First Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.first_name_label.place(x=40, y=30)
                    self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.middle_name_label.place(x=220, y=30)
                    self.last_name_label = Label(self.user_info_frame, text="Last Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.last_name_label.place(x=400, y=30)

                    self.first_nameins_entry = Entry(self.user_info_frame, width=20, textvariable=INSFNAMEVAR)
                    self.middle_nameins_entry = Entry(self.user_info_frame, width=20, textvariable=INSMNAMEVAR)
                    self.last_nameins_entry = Entry(self.user_info_frame, width=20, textvariable=INSLNAMEVAR)
                    self.first_nameins_entry.place(x=20, y=60)
                    self.middle_nameins_entry.place(x=200, y=60)
                    self.last_nameins_entry.place(x=380, y=60)

                    # ##########AGE ############
                    self.ageins_label = Label(self.user_info_frame, text="Age", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.ageins_label.place(x=60, y=90)
                    self.ageins_entry = Entry(self.user_info_frame, width=10, textvariable=INSAGEVAR)
                    self.ageins_entry.place(x=45, y=120)

                    # ########## BDAY############
                    self.birthdayins_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.birthdayins_label.place(x=220, y=90)
                    cal = DateEntry(self.user_info_frame, date_pattern="yyyy-mm-dd", textvariable=INSBDAY)
                    cal.place(x=210, y=120)

                    # ##########GENDER############
                    self.Genderins = Label(self.user_info_frame, text="Gender", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.Genderins.place(x=410, y=90)
                    self.genderins_entry = Entry(self.user_info_frame, width=15, textvariable=INSGENDER)
                    self.genderins_entry.place(x=390, y=120)

                    # ##########Profession############
                    profession = ["Accountant", "Actor/Actress", "Aircraft pilot", "Software Engineer", "Librarian",
                                  "Architect", "Artist", "Barber", "Bricklayer", "Business Person", "Butcher", "Chef",
                                  "Cleaner", "Construction worker", "Corporate Secretary", "Dentist", "Designer",
                                  "Driver",
                                  "Electrician", "Engineer",
                                  "Farmer", "Fire Fighter", "Fisherman", "Gardener", "Hair Dresser",
                                  "House Pinter and Decorator", "Journalist", "Judge", "Lawyer", "Lifeguard",
                                  "Mail Carrier", "Mechanic", "Model", "Nurse", "Personal Assistant", "Cashier",
                                  "Pharmacist", "Photographer", "Physician",
                                  "Plumber", "Police officer", "Politician", "Realstate Broker", "Salesperson",
                                  "Scientist",
                                  "Sea Farer", "Software Developer", "Soldier", "Tailor", "Teacher", "Technician",
                                  "Veterinarian", "Waiter", "Web Developer", "Worker", "Others not specified"]

                    def search(event):
                        self.professionins_combobox.set("")
                        value = event.widget.get()
                        if value == "":
                            self.professionins_combobox['value'] = profession
                        else:
                            data = []
                            for item in profession:
                                if value.lower() in item.lower():
                                    data.append(item)
                            self.professionins_combobox['values'] = data

                    self.professionins_label = Label(self.user_info_frame, text="Profession", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.professionins_combobox = ttk.Combobox(self.user_info_frame, width=23, values=profession,textvariable=INSPROFESSION)
                    self.professionins_label.place(x=40, y=150)
                    self.professionins_combobox.place(x=10, y=180)
                    self.professionins_combobox.bind('<Button-1>', search)
                    self.professionins_combobox.bind('<KeyRelease>', search)

                    # ##########Civil Status############
                    sts = ['Single', 'Married', 'Widowed', 'Annulled']
                    self.statusins_label = Label(self.user_info_frame, text="Civil Status", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                    self.civilins_status_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts,textvariable=INSCSTATUS)
                    self.civilins_status_combobox.set("")
                    self.statusins_label.place(x=220, y=150)
                    self.civilins_status_combobox.place(x=190, y=180)
                    show_insdetails()

                    update_button_ins = Button(self.user_info_frame, text="UPDATE ", font=('arial', 10), bg='white',fg='black', border=0, padx=15, command=insert_ins_update)
                    update_button_ins.place(x=160, y=240)
                    clear_button_ins = Button(self.user_info_frame, text="CLEAR", font=('arial', 10), bg='white',fg='black', padx=22, border=0, command=show_insdetails)
                    clear_button_ins.place(x=270, y=240)
            ###################################################### END OF POLICY INSURED VIEW #######################################################################

            def view_bene():
                self.policy = Policynumber.get()
                if self.policy == "" or self.policy == "0" or self.policy == None:
                    messagebox.showerror("", "No Policy Found")
                else:
                    def bene_addition():
                        #### CREATE DELETE FUNCTION FIRST DELETE ALL BENE BEFORE RIDER ADDITION
                        global index
                        con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                        cur = con.cursor()
                        sql = "Select POLICY_ID from tbl_policy WHERE POLICY_NUM='" + self.policy + "'"
                        cur.execute(sql)
                        indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        indexes.reverse()  ### reversed the fetch result to get the last index
                        x = indexes[0]
                        items = list(x)
                        index = items[0]  ## finally assign last value of the list from the converted tuple assign to variable (index) then run INSERT query
                        # print(index)

                        ###### QUERY TO EXECUTE BENE DELETION IN THE ASSIGNED POLICY #####
                        cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
                        delete1="DELETE FROM tbl_bene WHERE BENE_POLICY_ID IN (SELECT POLICY_ID FROM tbl_policy WHERE POLICY_NUM='"+self.policy+"')"
                        cur.execute(delete1)
                        con.commit()
                        messagebox.showinfo("Beneficiaries cleared","Kindly input your new Beneficiaries!")
                        con.close()

                    messagebox.showwarning("BENEFICIARY ADDITION","To ensure accuracy of BENEFICIARIES BENEFIT PERCENTAGE,\n We will remove your existing Beneficiaries before you enter.\nResulting to this,we require to re-enter your elected BENEFICIARIES")
                    if messagebox.askyesno("","Do you want to proceed on BENEFICIARY ADDITION?"):
                        self.checkpolicybene_window = Toplevel()
                        self.checkpolicybene_window.title("C.A.M.S /Check Policy Insured details view")
                        self.checkpolicybene_window.geometry("750x700")
                        self.checkpolicybene_window.config(bg='#008631')
                        self.checkpolicybene_window.resizable(False, False)
                        ############### START OF BENE ADDITION #################
                        bene_addition() ####### THIS FUNCTION DELETES ALL EXISTING BENEFICIARY OF THE CLIENT BEFORE SHE ENTER NEW SET OF BENEFICIARIES THIS WILL ALSO RESETS HER BENEFIT PERCENTAGE TO 0
                        value = IntVar()  ### this variable holds the percentage of the beneficiaries maximum percentage over all per policy is 100% splits every bene elected
                        self.x = 0  ## this variable also signifies the percentage per benefiary
                        self.husband_counter = 0  ## counter husband maximum 1
                        self.wife_counter = 0  ## counter wife maximum 1
                        self.sumbenefit = 0  ## variable that adds collected percentage for display to share() function

                        ##### Insert Query#######
                        def Insert_query():
                            if True:
                                con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                                cur = con.cursor()
                                cur.execute("SET FOREIGN_KEY_CHECKS = 0")

                                sql1 = "INSERT INTO tbl_bene(BENE_ID, firstname,middlename,lastname,age,birthday,gender,relationship,benefit_percentage,BENE_POLICY_ID)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                val1 = (Bene_ID, firstname, middlename, lastname, age, birthday, genderinput, relationship, percentage,index)
                                cur.execute(sql1, val1)
                                con.commit()
                                con.close()
                                #################### EXECUTE SELECT QUERY TO EXTRACT BENE_ID THAT WILL USE AS FK to ADDRESS AND CONTACT OF BENE ##########
                                con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                                cur = con.cursor()
                                # select="select BENE_ID from tbl_bene join tbl_policy where POLICY_NUM='"+self.policy+"'"
                                # cur.execute(select)
                                # get_beneid=cur.fetchall()
                                # beneid=get_beneid[0][0]
                                sql2 = "INSERT INTO tbladdress_bene(ADDRESS_ID,address,city,province,zipcode,country,type) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                val2 = (ADDRESS_ID, address, city, province, zipcode, countrycode, Type,)
                                cur.execute(sql2,val2)
                                con.commit()

                                sql3 = "INSERT INTO tbl_contact_bene(CONTACT_ID_BENE,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE)  VALUES (%s,%s,%s,%s,%s)"
                                val3 = (Bene_ID, mobile, landline, email, Type)
                                cur.execute(sql3, val3)
                                con.commit()
                                messagebox.showinfo("", "Beneficiary Added successfully!")
                                con.rollback()
                                con.close()


                        def Benecheck():  ##### THIS FUNCTION IDENTIFIES THE NAME OF THE INSURED ELECTED FROM INSURED INPUT TAB,, ONCE SYSTEM DETECTS SAME INPUT AS BENEFICIARY SYSTEM DECLINES THE INPUT####
                            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                            cur = con.cursor()
                            sql1 = "Select firstname,middlename,lastname FROM tbl_insured join tbl_policy on INS_ID=POLICY_ID where POLICY_NUM='"+self.policy+"'"
                            cur.execute(sql1)
                            insuredname = cur.fetchall()  #### fetch firstname,middlename,lastname of the insured displays as tupple inside a list this format " [()] "
                            insuredname.reverse()  ### reverse to access the last input
                            i = insuredname[0]  ### this line extract access the tupple inside the list
                            # ins_index = i[0]  ###assigning variable to every item inside the tupple
                            fname = i[0]  ###assigning variable to every item inside the tupple
                            mname = i[1]  ###assigning variable to every item inside the tupple
                            lname = i[2]
                            fullname = fname + " " + mname + " " + lname  ### combine extracted data and returning the "fullname"
                            return fullname

                        ###### Benefit Share Computation #######
                        def share():
                            self.sumbenefit = self.sumbenefit + percentage


                        ###################### THIS FUNCTION TRIGGERS IF CLIENT USER ASSIGN BENEFICIARY THE SAME PERSON AS INSURED ###############
                        #### THIS WILL DELETE ALL THE BENEFICIARIES OF THE POLICY, for RE ENTER #########
                        def update():
                            con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                            cur = con.cursor()
                            sql = "DELETE FROM tbl_bene WHERE tbl_bene.BENE_ID =BENE_POLICY_ID"
                            cur.execute(sql)
                            sql1 = "DELETE FROM tbladdress_bene WHERE ADDRESS_ID=ADDRESS_ID"
                            cur.execute(sql1)
                            con.commit()
                            con.close()

                        ###### Relation ship Husband Fuction#######
                        ### EVERY FUNCTION FOR  relalationship_husband(),relalationship_wife() , relalationship_others() checks if the insured is different on the elected bene system will decline if
                        ### user input the same person.
                        def relalationship_husband():
                            fullname = Benecheck()  #### extracted full name from the said function
                            if self.husband_counter == 1:
                                share()
                                self.x = self.x + percentage
                                if self.sumbenefit < 100:
                                    if fullname != client_fullname:
                                        Insert_query()
                                        if messagebox.askyesno("", "Input another Beneficiary?"):
                                            clear()
                                        else:
                                            messagebox.showwarning("Unable to use Max Percentage","Balance:" + str(self.sumbenefit - 100) + "%")
                                            clear()
                                    else:
                                        messagebox.showerror("", "Cannot Accept INSURED AS BENEFICIARY")
                                        update()
                                        self.x = 0
                                        self.husband_counter = 0
                                        self.sumbenefit = 0
                                        return self.x, self.sumbenefit, self.husband_counter

                                elif self.sumbenefit == 100:
                                    if fullname != client_fullname:
                                        Insert_query()
                                        messagebox.showinfo("", "Benefit limit maximum reached 100%")
                                        self.checkpolicybene_window.withdraw()
                                    else:
                                        messagebox.showerror("", "Cannot Accept INSURED AS BENEFICIARY")
                                        update()
                                        self.x = 0
                                        self.husband_counter = 0
                                        self.sumbenefit = 0
                                        return self.x, self.sumbenefit, self.husband_counter
                                else:
                                    messagebox.showerror("", "Sobra ang iyong input!")
                            else:
                                messagebox.showerror("", "Unable to accept duplicate Relationship")
                                # clear()

                        ###### Relation ship WIFE Fuction#######
                        def relalationship_wife():
                            fullname = Benecheck()  #### extracted full name from the said function
                            if self.wife_counter == 1:
                                share()
                                self.x = self.x + percentage
                                if self.sumbenefit < 100:
                                    if fullname != client_fullname:
                                        Insert_query()
                                        if messagebox.askyesno("", "Input another Beneficiary?"):
                                            clear()
                                        else:
                                            messagebox.showwarning("Unable to use Max Percentage", "Balance:" + str(self.sumbenefit - 100) + "%")
                                            clear()
                                    else:
                                        messagebox.showerror("", "Cannot Accept INSURED AS BENEFICIARY")
                                        update()
                                        self.x = 0
                                        self.wife_counter = 0
                                        self.sumbenefit = 0
                                        return self.x, self.sumbenefit, self.husband_counter

                                elif self.sumbenefit == 100:
                                    if fullname != client_fullname:
                                        Insert_query()
                                        messagebox.showinfo("", "Benefit limit maximum reached 100%")
                                        self.checkpolicybene_window.withdraw()

                                    else:
                                        messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                                        update()
                                        self.x = 0
                                        self.wife_counter = 0
                                        self.sumbenefit = 0
                                        return self.x, self.sumbenefit, self.husband_counter
                                else:
                                    messagebox.showerror("", "Sobra ang iyong input!")
                            else:
                                messagebox.showerror("", "Unable to accept duplicate Relationship")
                                # clear()

                        ###### Relation ship OTHERS Fuction#######
                        def others():
                            fullname = Benecheck()  #### extracted full name from the said function
                            share()
                            self.x = self.x + percentage
                            if self.sumbenefit < 100:
                                if fullname != client_fullname:
                                    Insert_query()
                                    if messagebox.askyesno("", "Input another Beneficiary?"):
                                        clear()
                                    else:
                                        messagebox.showwarning("Unable to use Max Percentage","Balance:" + str(self.sumbenefit - 100) + "%")
                                        clear()
                                else:
                                    messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                                    update()
                                    self.x = 0
                                    self.sumbenefit = 0

                                    return self.x, self.sumbenefit, self.husband_counter
                            elif self.sumbenefit == 100:
                                if fullname != client_fullname:
                                    Insert_query()
                                    messagebox.showinfo("", "Benefit limit maximum reached 100%")
                                    self.checkpolicybene_window.withdraw()
                                else:
                                    messagebox.showwarning("", "Cannot Accept INSURED AS BENEFICIARY")
                                    update()
                                    self.x = 0
                                    self.sumbenefit = 0
                                    return self.x, self.sumbenefit, self.husband_counter
                            else:
                                messagebox.showerror("", "Sobra ang iyong input!")

                        #### clear function ### just for clearing fields##
                        def clear():
                            self.first_name_entry.delete(0, END)
                            self.middle_name_entry.delete(0, END)
                            self.last_name_entry.delete(0, END)
                            self.relationship_combobox.set("None")
                            self.percentage_entry_label.delete(0, END)
                            self.first_name_entry.delete(0, END)
                            self.mobile_entry.delete(0, END)
                            self.address_entry.delete(1.0, END)
                            self.city_entry.delete(0, END)
                            self.province_entry.delete(0, END)
                            self.zipcode_entry.delete(0, END)
                            self.country_combobox.delete(0,END)
                            self.address_type_combobox.set("None")

                        #########FUNCTION TO GET ALL INPUTS AND VALIDATES entry######
                        def Input_bene():
                            global relationship, percentage, Bene_ID, firstname, middlename, lastname, age, birthday, genderinput, mobile, landline, email, ADDRESS_ID, address, city, province, zipcode, countrycode, Type, client_fullname
                            Bene_ID = 0
                            firstname = self.first_name_entry.get()
                            middlename = self.middle_name_entry.get()
                            lastname = self.last_name_entry.get()
                            age = self.age_spinbox.get()
                            birthday = self.cal.get()
                            genderinput = gender.get()
                            relationship = self.relationship_combobox.get()
                            percentage = value.get()
                            mobile = self.mobile_entry.get()
                            landline = self.Landline_entry.get()
                            email = self.email_entry.get()
                            ADDRESS_ID = 0
                            address = self.address_entry.get("1.0", END)
                            city = self.city_entry.get()
                            province = self.province_entry.get()
                            zipcode = self.zipcode_entry.get()
                            countrycode = self.country_combobox.get()
                            Type = self.address_type_combobox.get()
                            client_fullname = firstname + " " + middlename + " " + lastname

                            #### VALIDATION OF COVERAGE BEFORE PASSING TO RELATIONSHIP VALIDATION ###
                            if self.x <= 100:
                                if firstname == "" or middlename == "" or lastname == "" or age == "" or birthday == "" or relationship == "" or percentage == "" or genderinput == "" or mobile == "" or address == "" or city == "" \
                                        or province == "" or zipcode == "" or countrycode == "" or Type == "":
                                    messagebox.showerror("", "Some fields are missing in Beneficiary information")
                                elif relationship == "Husband":
                                    if self.x + percentage <= 100:
                                        self.husband_counter = self.husband_counter + 1
                                        relalationship_husband()
                                    else:
                                        messagebox.showerror("", "Input is morethan total limit=100%")
                                        self.percentage_entry_label.delete(0, END)

                                elif relationship == "Wife":
                                    if self.x + percentage <= 100:
                                        self.wife_counter = self.wife_counter + 1
                                        relalationship_wife()
                                    else:
                                        messagebox.showerror("", "Input is morethan total limit=100%")
                                        self.percentage_entry_label.delete(0, END)
                                else:
                                    if self.x + percentage <= 100:
                                        others()
                                    else:
                                        messagebox.showerror("", "Input is morethan total limit=100%")
                                        self.percentage_entry_label.delete(0, END)
                                ############################################################################################


                        ####BENE INPUT WIDGETS######
                        self.user_info_frame = LabelFrame(self.checkpolicybene_window, text="Beneficiary Information", bg='#008631',fg='white', width=550, height=230)
                        self.user_info_frame.place(x=40, y=40)
                        self.first_name_label = Label(self.user_info_frame, text="First Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.first_name_label.place(x=10, y=10)
                        self.middle_name_label = Label(self.user_info_frame, text="Middle Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.middle_name_label.place(x=170, y=10)

                        self.last_name_label = Label(self.user_info_frame, text="Last Name", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.last_name_label.place(x=330, y=10)

                        self.first_name_entry = Entry(self.user_info_frame, width=25)
                        self.first_name_entry.place(x=10, y=40)
                        self.middle_name_entry = Entry(self.user_info_frame, width=25)
                        self.middle_name_entry.place(x=170, y=40)
                        self.last_name_entry = Entry(self.user_info_frame, width=25)
                        self.last_name_entry.place(x=330, y=40)

                        # ##########AGE ############
                        self.age_label = Label(self.user_info_frame, text="Age", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.age_spinbox = Spinbox(self.user_info_frame, from_=18, to=110, width=23, )
                        self.age_spinbox.place(x=10, y=95)
                        self.age_label.place(x=10, y=60)

                        # ########## BDAY############
                        self.birthday_label = Label(self.user_info_frame, text="Birthday", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.birthday_label.place(x=170, y=60)

                        self.cal = DateEntry(self.user_info_frame, selectmode='day', date_pattern="yyyy-mm-dd")
                        self.cal.place(x=170, y=95)

                        ##########GENDER############
                        gender = StringVar()
                        self.Gender = Label(self.user_info_frame, text="Gender", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.Gender.place(x=290, y=60)
                        self.mLabel = Label(self.user_info_frame, text="Male", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.mLabel.place(x=320, y=90)
                        self.fLabel = Label(self.user_info_frame, text="Female", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.fLabel.place(x=385, y=90)

                        self.rbtnMale = Radiobutton(self.user_info_frame, variable=gender, value="Male", bg='#008631')
                        self.rbtnMale.place(x=290, y=90)
                        self.rbtnFemale = Radiobutton(self.user_info_frame, variable=gender, value="Female", bg='#008631')
                        self.rbtnFemale.place(x=360, y=90)

                        # ###########Relationship############
                        sts = ['Husband', 'Wife', 'Child', 'Parent', 'Legal Guardian', 'others']
                        self.status_label = Label(self.user_info_frame, text="Relationship", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.status_label.place(x=10, y=120)

                        self.relationship_combobox = ttk.Combobox(self.user_info_frame, width=23, values=sts)
                        self.relationship_combobox.set("None")
                        self.relationship_combobox.place(x=10, y=145)

                        ###########Benefit_Percentage############

                        self.percentage_label = Label(self.user_info_frame, text="Benefit Percentage", bg='#008631',fg='white', font=('Microsoft YaHei UI Light', 11))
                        self.percentage_label.place(x=190, y=120)

                        self.percentage_entry_label = Entry(self.user_info_frame, width=25, textvariable=value)
                        self.percentage_entry_label.place(x=190, y=145)

                        self.NoteLabel = Label(self.user_info_frame,text="NOTE:Percentage shares for all bene will be strictly limited to total of 100%", bg='#008631', fg='white', font=('Microsoft YaHei UI Light', 10))
                        self.NoteLabel.place(x=10, y=170)

                        ############## ADD CONTACT TAB##############

                        self.contact_info_frame = LabelFrame(self.checkpolicybene_window, text='Contact Information', bg='#008631',fg='white', width=400, height=110)
                        self.contact_info_frame.place(x=40, y=270)

                        self.mobile_Label = Label(self.contact_info_frame, text="Mobile Number", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.mobile_Label.place(x=0, y=0)
                        self.mobile_entry = Entry(self.contact_info_frame, width=35, bg='white')
                        self.mobile_entry.place(x=120, y=0)

                        self.Landline_Label = Label(self.contact_info_frame, text="Landline", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.Landline_Label.place(x=0, y=30)
                        self.Landline_entry = Entry(self.contact_info_frame, width=35, bg='white')
                        self.Landline_entry.place(x=120, y=30)

                        self.email_Label = Label(self.contact_info_frame, text="Email", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                        self.email_Label.place(x=0, y=60)
                        self.email_entry = Entry(self.contact_info_frame, width=35, bg='white')
                        self.email_entry.place(x=120, y=60)

                        # # ################### Address##############################
                        address_type = ['Residence', 'Office', 'Mailing/Billing']
                        address_type = ['Primary', 'Alternate']

                        self.addressframe = LabelFrame(self.checkpolicybene_window, text="Address Information", bg='#008631', fg='white',width=550, height=200)
                        self.addressframe.place(x=40, y=380)

                        self.address_label = Label(self.addressframe, text="Address:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                        self.address_label.place(x=0, y=0)
                        self.address_entry = Text(self.addressframe, width=40, height=2, bg='white')
                        self.address_entry.place(x=57, y=0)

                        self.city_label = Label(self.addressframe, text="City:", bg='#008631', fg='white', font=('Microsoft YaHei UI Light', 10))
                        self.city_label.place(x=0, y=40)
                        self.city_entry = Entry(self.addressframe, width=45, bg='white')
                        self.city_entry.place(x=57, y=43)

                        self.province_label = Label(self.addressframe, text="Province:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                        self.province_label.place(x=0, y=64)
                        self.province_entry = Entry(self.addressframe, width=45, bg='white')
                        self.province_entry.place(x=57, y=66)

                        self.zipcode_label = Label(self.addressframe, text="Zipcode:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                        self.zipcode_label.place(x=0, y=87)
                        self.zipcode_entry = Entry(self.addressframe, width=16, bg='white')
                        self.zipcode_entry.place(x=88, y=88)

                        self.countrycode_label = Label(self.addressframe, text="Country code:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                        self.countrycode_label.place(x=0, y=107)
                        self.country_combobox = Entry(self.addressframe, width=13)
                        self.country_combobox.place(x=88, y=110)

                        self.address_type_label = Label(self.addressframe, text="Type:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                        self.address_type_label.place(x=0, y=127)
                        self.address_type_combobox = ttk.Combobox(self.addressframe, width=13, values=address_type)
                        self.address_type_combobox.place(x=88, y=133)
                        self.address_type_combobox.set("Type")

                        self.button1 = Button(self.checkpolicybene_window, text="Input Beneficiaries", font=('arial', 9, 'bold'),bg='white', fg='black', border=0, command=Input_bene, padx=10)
                        self.button1.place(x=150, y=600)
                        self.clear_button = Button(self.checkpolicybene_window, text="Clear", font=('arial', 9, 'bold'), bg='white',fg='black', border=0, padx=15, command=clear)
                        self.clear_button.place(x=290, y=600)
                    else:
                        pass

            ##################################### END OF VIEW BENEFICIARY ##################################

            CHECKPOLICY_BUTTON = Button(self.Policyinfo_window, text="Policy Information", padx=19, pady=5, bg = "#c99024", compound="left",font=("Arial", 10, "bold"), fg="white", border=1, activebackground = "#a87616",command=view_policy)
            CHECKPOLICY_BUTTON.place(x=50, y=20)
            CHECKPOLICYOWNER_BUTTON = Button(self.Policyinfo_window, text="Policy Owner", padx=34, pady=5, bg = "#c99024", compound="left",font=("Arial", 10, "bold"), fg="white", border=1, activebackground = "#a87616",command=view_po)
            CHECKPOLICYOWNER_BUTTON.place(x=50, y=70)
            CHECKINSURED_BUTTON = Button(self.Policyinfo_window, text="Policy Insured", padx=31, pady=5, bg = "#c99024", compound="left",font=("Arial", 10, "bold"), fg="white", border=1, activebackground = "#a87616",command=view_ins)
            CHECKINSURED_BUTTON.place(x=50, y=120)
            CHECKBENEFICIARY_BUTTON = Button(self.Policyinfo_window, text="Add Beneficiary", padx=26, pady=5, bg="#c99024",compound="left", font=("Arial", 10, "bold"), fg="white", border=1,activebackground="#a87616", command=view_bene)
            CHECKBENEFICIARY_BUTTON.place(x=50, y=170)

##################################################### END OF POLICY INFO #######################################################################################################

#################################################### START PAYMENT INFO ###########################################################################################
        def payment():
            self.policy = Policynumber.get()
            if self.policy == "" or self.policy == "0" or self.policy == None:
                messagebox.showerror("", "No Policy Found")
            else:
                self.checkpaymnetinfowindow = Toplevel()
                self.checkpaymnetinfowindow.title("C.A.M.S /Payment details view")
                self.checkpaymnetinfowindow.geometry("600x380")
                self.checkpaymnetinfowindow.config(bg='#008631')
                self.checkpaymnetinfowindow.resizable(False, False)

                ### LIST VALUES & TEXT VARIABLES###
                MODEPAYMENT = StringVar()
                FREQUENCYPAYMENT = StringVar()
                DURATIONPAYMENT = StringVar()
                mode_list = ['Regular']
                frequency_list = ['Monthly', 'Quarterly', 'SemiAnnual', 'Annual']
                paymentdur_list = ['10-YEARS', '5-YEARS', 'REGULAR']

                ### SHOW PAYMENT DETAILS FROM RECORD##
                def show_paymentinfo():
                    global age_get,monthspaid_get
                    con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                    cur = con.cursor()
                    sql = "select MODE,FREQUENCY,PAYMENT_DURATION,PAYMENT_TOTAL,age from tbl_policy INNER JOIN tbl_insured ON POLICY_ID=INS_ID join tbl_payment on POLICY_ID=PAYMENT_ID_FK where tbl_policy.POLICY_NUM='"+self.policy+"'"
                    cur.execute(sql)
                    payment_details=cur.fetchall()
                    con.close()
                    # print(payment_details)
                    ##### ASSIGNING FETCH DATA TO VARIABLE FOR MANIPULATION
                    mode_get=payment_details[0][0]
                    frequency_get=payment_details[0][1]
                    duration_get = payment_details[0][2]
                    amount_get = payment_details[0][3]
                    age_get=payment_details[0][4]

                    #### CLEARS ALL ENTRY BOX AND COMBO-BOX BEFORE INSERT
                    self.Mode_entry.delete(0, END)
                    self.frequency_entry.delete(0, END)
                    self.paymentdur_entry.delete(0, END)
                    self.paymentamount_label_output.config(text="")
                    self.Mode_entry.insert(0,mode_get)
                    ###### INSERT DATA TO ENTRY BOXES

                    self.frequency_entry.insert(0, frequency_get)
                    self.paymentdur_entry.insert(0, duration_get)
                    self.paymentamount_label_output.config(text=amount_get)
                    #### AFTER INSERT THIS WILL DIS ABLE ENTRY BOX
                    self.Mode_entry.config(state=DISABLED)
                    self.Mode_combobox.config(state=DISABLED)
                    self.frequency_entry.config(state=DISABLED)
                    self.frequency_combobox.config(state=DISABLED)
                    self.paymentdur_entry.config(state=DISABLED)
                    self.paymentdur_combobox.config(state=DISABLED)


                #### COMPUTATION FUNCTION IF USER WILL CHANGE THEIR FREQUENCY###
                def payment_computation():
                    global total,frequency
                    age=int(age_get)
                    frequency = FREQUENCYPAYMENT.get()
                    total = 0
                    ###### PAYMENT FREQUENCY############
                    MONTHLY = 31
                    QUARTERLY = 90
                    SEMIANNUAL = 181
                    ANNUAL = 365

                    ##### AGE BRACKET PAYMENT PER AGE#####
                    bracket1 = 30
                    bracket2 = 32
                    bracket3 = 35
                    bracket4 = 37
                    bracket5 = 39
                    ####################################

                    ################## PAYMENT COMPUTATION########################
                    ########### computation of payment based on the extracted age from tbl_insured depending on age is the clients payment multiplied by frequency selected######
                    if age <= 18:
                        if frequency == "Monthly":
                            total = bracket1 * MONTHLY
                            self.paymentamount_label_output.config(text=total)

                        elif frequency == "Quarterly":
                            total = bracket1 * QUARTERLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "SemiAnnual":
                            total = bracket1 * SEMIANNUAL
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Annual":
                            total = bracket1 * ANNUAL
                            self.paymentamount_label_output.config(text=total)

                    elif age <= 30:
                        if frequency == "Monthly":
                            total = bracket2 * MONTHLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Quarterly":
                            total = bracket2 * QUARTERLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "SemiAnnual":
                            total = bracket2 * SEMIANNUAL
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Annual":
                            total = bracket2 * ANNUAL
                            self.paymentamount_label_output.config(text=total)

                    elif age <= 35:
                        if frequency == "Monthly":
                            total = bracket3 * MONTHLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Quarterly":
                            total = bracket3 * QUARTERLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "SemiAnnual":
                            total = bracket3 * SEMIANNUAL
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Annual":
                            total = bracket3 * ANNUAL
                            self.paymentamount_label_output.config(text=total)

                    elif age <= 40:
                        if frequency == "Monthly":
                            total = bracket4 * MONTHLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Quarterly":
                            total = bracket4 * QUARTERLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "SemiAnnual":
                            total = bracket4 * SEMIANNUAL
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Annual":
                            total = bracket4 * ANNUAL
                            self.paymentamount_label_output.config(text=total)

                    elif age <= 45:
                        if frequency == "Monthly":
                            total = bracket5 * MONTHLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Quarterly":
                            total = bracket5 * QUARTERLY
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "SemiAnnual":
                            total = bracket5 * SEMIANNUAL
                            self.paymentamount_label_output.config(text=total)
                        elif frequency == "Annual":
                            total = bracket5 * ANNUAL
                            self.paymentamount_label_output.config(text=total)
                    return total

                ### INSERT FUNCTION WITH QUERY ###
                def insert_paymentupdate():
                    mode = MODEPAYMENT.get()
                    paymentduration = DURATIONPAYMENT.get()
                    frequency=FREQUENCYPAYMENT.get()
                    total=payment_computation()
                    messagebox.showwarning("","You are going to update client`s Payment Information?")
                    if messagebox.askyesno("Payment Info Update","Do you want to proceed?"):
                        if mode=="" or paymentduration=="" or frequency=="":
                            messagebox.showerror("","Some details are missing")
                        else:
                            con = mysql.connector.connect(host='localhost', database='practicedb', user='root',password='')
                            cur = con.cursor()
                            sql = "UPDATE tbl_policy SET MODE=%s,FREQUENCY=%s,PAYMENT_DURATION=%s,PAYMENT_TOTAL=%s where POLICY_NUM=%s"
                            val=(mode,frequency,paymentduration,total,self.policy)
                            cur.execute(sql,val)
                            con.commit()
                            messagebox.showinfo("","Payment Information Updated!")
                            con.close()
                            show_paymentinfo()
                    else:
                        pass


                #### SET ENTRY BOXES TO ACTIVE IF USET PRESS EDIT
                def edit_payment():
                    self.Mode_entry.config(state=NORMAL)
                    self.Mode_combobox.config(state=NORMAL)
                    self.frequency_entry.config(state=NORMAL)
                    self.frequency_combobox.config(state=NORMAL)
                    self.paymentdur_entry.config(state=NORMAL)
                    self.paymentdur_combobox.config(state=NORMAL)

                #### FRAME CREATION##3
                self.paymentinfoframe=LabelFrame(self.checkpaymnetinfowindow,text="Payment Information",width=560,height=340,bg="#008631",fg="white")
                self.paymentinfoframe.place(x=10,y=10)

                self.current_label = Label(self.paymentinfoframe, text="Current:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 11))
                self.current_label.place(x=10, y=10)
                self.Mode_label = Label(self.paymentinfoframe, text="Mode:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.Mode_label.place(x=10, y=40)
                self.Mode_entry = Entry(self.paymentinfoframe, width=16, bg='white',textvariable=MODEPAYMENT)
                self.Mode_entry.place(x=90, y=40)
                self.Mode_combobox = ttk.Combobox(self.paymentinfoframe, width=13, values=mode_list,textvariable=MODEPAYMENT)
                self.Mode_combobox.place(x=200, y=38)

                self.frequency_label = Label(self.paymentinfoframe, text="Frequency:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.frequency_label.place(x=10, y=65)
                self.frequency_entry = Entry(self.paymentinfoframe, width=16, bg='white', textvariable=FREQUENCYPAYMENT)
                self.frequency_entry.place(x=90, y=65)
                self.frequency_combobox = ttk.Combobox(self.paymentinfoframe, width=13, values=frequency_list,textvariable=FREQUENCYPAYMENT)
                self.frequency_combobox.place(x=200, y=63)

                self.paymentdur_label = Label(self.paymentinfoframe, text="Payment Duration:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.paymentdur_label.place(x=10, y=90)
                self.paymentdur_entry = Entry(self.paymentinfoframe, width=16, bg='white', textvariable=DURATIONPAYMENT)
                self.paymentdur_entry.place(x=130, y=90)
                self.paymentdur_combobox = ttk.Combobox(self.paymentinfoframe, width=13, values=paymentdur_list, textvariable=DURATIONPAYMENT)
                self.paymentdur_combobox.place(x=240, y=88)

                self.paymentamount_label = Label(self.paymentinfoframe, text="Amount:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.paymentamount_label.place(x=10, y=115)
                self.paymentamount_label_output = Label(self.paymentinfoframe,width=15, bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.paymentamount_label_output.place(x=90, y=115)

                show_paymentinfo()

                self.edit_paymnet_button = Button(self.paymentinfoframe, text="Edit",font=('arial', 9, 'bold'),bg="#f5b32f", fg='white', border=0,padx=25, command=edit_payment)
                self.edit_paymnet_button.place(x=30, y=205)
                self.update_paymnet_button = Button(self.paymentinfoframe, text="Update",font=('arial', 9, 'bold'), bg="#3ab55f", fg='white', border=0,padx=15,command=insert_paymentupdate)
                self.update_paymnet_button.place(x=30, y=230)
                self.clear_button = Button(self.paymentinfoframe, text="Clear", font=('arial', 9, 'bold'), bg="#e66763", fg='white', border=0, padx=20, command=show_paymentinfo)
                self.clear_button.place(x=30, y=255)

        #################################################### END PAYMENT INFO ##############################################################################################
        ###################################################### START PAYMENT HISTORY ######################################################################################
        def history():
            self.policy = Policynumber.get()
            if self.policy == "" or self.policy == "0" or self.policy == None:
                messagebox.showerror("", "No Policy Found")
            else:
                self.historywindow = Toplevel()
                self.historywindow.title("C.A.M.S /Payment History")
                self.historywindow.geometry("525x430")
                self.historywindow.config(bg='#008631')
                self.historywindow.resizable(False, False)

                def show_payment_history():
                    con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                    cur = con.cursor()
                    sql2 = "SELECT PAYMENT_ID,PAY_STARTDATE,amount,MODE from tbl_payment INNER JOIN tbl_policy on POLICY_ID = PAYMENT_ID_FK where tbl_policy.POLICY_NUM='" +self.policy+"'"
                    cur.execute(sql2)
                    paymentrecord = cur.fetchall()
                    con.rollback()
                    con.close()
                    for x in paymentrecord:
                        self.payment_hist_trv.insert("", 'end', id=x[0], text=x[0],values=(x[0], x[1], x[3], x[2]))

                self.Payment_history_frame = LabelFrame(self.historywindow, width=1080, height=600, bg='#008631')
                self.Payment_history_frame.place(x=0, y=0)

                self.payment_hist_trv = ttk.Treeview(self.Payment_history_frame, columns=[1, 2, 3, 4], show="headings", height="20")
                self.payment_hist_trv.grid(row=0, column=0)

                # width of columns and alignment
                self.payment_hist_trv.column("1", width=80, anchor='c')
                self.payment_hist_trv.column("2", width=200, anchor='c')
                self.payment_hist_trv.column("3", width=120, anchor='c')
                self.payment_hist_trv.column("4", width=120, anchor='c')
                # Headings
                # respective columns
                self.payment_hist_trv.heading("1", text="PAYMENT ID")
                self.payment_hist_trv.heading("2", text="RECEIVE DATE")
                self.payment_hist_trv.heading("3", text="PAYMENT MODE")
                self.payment_hist_trv.heading("4", text="AMOUNT")
                show_payment_history()
        ####################################### END OF PAYMENT HISTORY #############################################################

        def documentreq():
            self.policy = Policynumber.get()
            if self.policy == "" or self.policy == "0" or self.policy == None:
                messagebox.showerror("", "No Policy Found")
            else:
                self.docreqwindow = Toplevel()
                self.docreqwindow.title("C.A.M.S /Document Request")
                self.docreqwindow.geometry("580x260")
                self.docreqwindow.config(bg='#008631')
                self.docreqwindow.resizable(False, False)

                def show_details():
                    global getfullname,getemail,getamount,getpaydate,getpn,getproduct,getproductcoverage
                    con = mysql.connector.connect(host='localhost', username='root', password='', db='practicedb')
                    cur = con.cursor()
                    querypo = "SELECT tbl_policy.POLICY_NUM,tbl_contact_po.email,firstname,middlename,lastname,amount,PAY_STARTDATE FROM tbl_policy join tbl_contact_po on POLICY_ID=CONTACT_FK_PO INNER join tbl_po on POLICY_ID=PO_ID JOIN tbl_payment on POLICY_ID = PAYMENT_ID_FK where tbl_policy.POLICY_NUM ='" + self.policy + "'"
                    cur.execute(querypo)
                    getpo = cur.fetchall()
                    print(getpo)
                    getpn=getpo[0][0]
                    getemail=getpo[0][1]
                    getfname=getpo[0][2]
                    getmname=getpo[0][3]
                    getlname=getpo[0][4]
                    getfullname=getfname+" "+getlname
                    getamount=getpo[0][5]
                    getpaydate=getpo[0][6]


                    self.policynum_label_output.config(text=getpn)
                    self.email_labeloutput.config(text=getemail)

                    querypolicy = " SELECT PRODUCT_NAME,COVERAGE_AMOUNT,RIDER,RIDER_COVERAGE from tbl_policy join tbl_rider on POLICY_ID=RIDER_ID_FK where POLICY_NUM ='" + self.policy + "'"
                    cur.execute(querypolicy)
                    getpolicy = cur.fetchall()
                    getproduct=getpolicy[0][0]
                    getproductcoverage=getpolicy[0][1]



                def generate_document():
                    global docrequest
                    docrequest=DOCREQVAR.get()
                    if docrequest=='DCMT-OR':
                        def generate_pdf(client_name,PN , date, amount, pdffiles):
                            # create the PDF object, using the buffer as its "file."
                            p = canvas.Canvas(r"C:\Users\JoshuaPC\Desktop\mainprojectbackup2\pdffiles\{}".format(pdffiles), pagesize=letter)

                            # Draw the title
                            p.setFont("Helvetica", 20)
                            p.drawCentredString(letter[0] / 2, 650, "Official Receipt")

                            # Draw the current date
                            p.setFont("Helvetica", 13)
                            today = date.today().strftime("%m/%d/%Y")
                            p.drawString(420, 600, "Date: " + today)

                            # Draw things on the PDF. Here's where the PDF generation happens.
                            # Draw the rest of the receipt

                            p.setFont("Helvetica", 13)
                            p.drawString(72, 550, "Dear Mr/Ms:" + " " + client_name)
                            p.drawString(72, 500, "Greetings!")
                            p.drawString(72, 450,"This email is to acknowledge the receipt of your premium payment  amounting ")
                            p.drawString(72, 430,"to PHP" +" "+ str(getamount) + ". " + "Under Policy Number:" +" " + str(getpn) + ".")
                            p.drawString(72, 390,"Rest assured that you`re payment will be posted in you`re account within 24hrs")
                            p.drawString(72, 370, "upon received of you`re payment.")
                            p.drawString(72, 300, "Thank you, and have a great day!")

                            # Draw the footer
                            p.setFont("Helvetica", 9)
                            p.drawString(72, 50, "For any concern email us: Sample_email@gmail.com ")

                            p.setFont("Helvetica", 13)
                            p.line(72, 40, letter[0] - 72, 40)
                            p.drawString(430, 150, "Management,")

                            # Close the PDF object cleanly, and we're done.
                            p.showPage()
                            p.save()
                            messagebox.showinfo("", "O.R Successfully Generated")
                        generate_pdf(getfullname,getpn ,getpaydate,getamount, "receipt.pdf")


                    else:
                        def generate_pdf(client_name,getproduct,getpn, getproductcoverage, pdffiles):
                            # create the PDF object, using the buffer as its "file."
                            p = canvas.Canvas(r"C:\Users\JoshuaPC\Desktop\mainprojectbackup2\pdffiles\{}".format(pdffiles),pagesize=letter)

                            # Draw the title
                            p.setFont("Helvetica", 20)
                            p.drawCentredString(letter[0] / 2, 650, "Policy Confimation Receipt")

                            # Draw the current date
                            p.setFont("Helvetica", 13)
                            today = date.today().strftime("%m/%d/%Y")
                            p.drawString(420, 600, "Date: " + today)

                            # Draw things on the PDF. Here's where the PDF generation happens.
                            # Draw the rest of the receipt

                            p.setFont("Helvetica", 13)
                            p.drawString(72, 550, "Dear Mr/Ms:" + " " + client_name)
                            p.drawString(72, 500, "Congratulations!")
                            p.drawString(72, 450, "We would like to inform you that you`re policy," +" "+ str(getproduct))
                            p.drawString(72, 430,"Under Policy Number:" +" "+ str(getpn) + " " + "is now Activated." + " " + "The coverage of you`re policy")
                            p.drawString(72, 410, "are the following:")
                            p.drawString(72, 380, "Insurance Coverage amount:" + " "+"PHP"+" " + str(getproductcoverage) )

                            p.drawString(72, 340, "This document will serves as proof of your Policy Activation.")
                            p.drawString(72, 310, "Thank you, and have a great day!")

                            # Draw the footer
                            p.setFont("Helvetica", 9)
                            p.drawString(72, 50, "For any concern email us: Sample_email@gmail.com ")

                            p.setFont("Helvetica", 13)
                            p.line(72, 40, letter[0] - 72, 40)
                            p.drawString(430, 150, "Management,")

                            # Close the PDF object cleanly, and we're done.
                            p.showPage()
                            p.save()
                            messagebox.showinfo("", "P.C.R Successfully Generated")

                        generate_pdf(getfullname,getproduct,getpn,getproductcoverage, "PCR.pdf")


                ##### SEND DOCUMENT ######
                def send_document():
                    if docrequest == 'DCMT-OR':
                        def send_email(to, subject, pdffiles):
                            # create a message object
                            msg = MIMEMultipart()
                            msg['From'] = 'liezlcute08@gmail.com'
                            msg['To'] = getemail
                            msg['Subject'] = subject

                            # attach the PDF to the message
                            with open(pdffiles, 'rb') as f:
                                pdf = MIMEApplication(f.read(), _subtype='pdf')
                                pdf.add_header('content-disposition', 'attachment', filename='receipt.pdf')
                                msg.attach(pdf)

                            # send the email
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login('liezlcute08@gmail.com', 'hajgngusvfyalrrb')
                            server.sendmail('liezlcute08@gmail.com', to, msg.as_string())
                            server.quit()
                            messagebox.showinfo("","Document sent successfully!")
                        send_email(getemail, "Official Receipt", "C:/Users/JoshuaPC/Desktop/mainprojectbackup2/pdffiles/receipt.pdf")
                    else:
                        def send_email(to, subject, pdffiles):
                            # create a message object
                            msg = MIMEMultipart()
                            msg['From'] = 'liezlcute08@gmail.com'
                            msg['To'] = getemail
                            msg['Subject'] = subject

                            # attach the PDF to the message
                            with open(pdffiles, 'rb') as f:
                                pdf = MIMEApplication(f.read(), _subtype='pdf')
                                pdf.add_header('content-disposition', 'attachment', filename='PCR.pdf')
                                msg.attach(pdf)

                            # send the email
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login('liezlcute08@gmail.com', 'hajgngusvfyalrrb')
                            server.sendmail('liezlcute08@gmail.com', to, msg.as_string())
                            server.quit()
                            messagebox.showinfo("", "Document sent successfully!")
                        send_email(getemail, "Policy Confirmation Receipt","C:/Users/JoshuaPC/Desktop/mainprojectbackup2/pdffiles/PCR.pdf")



                ### LIST VALUES & TEXT VARIABLES###
                DOCREQVAR = StringVar()
                document_list = ['DCMT-PCR','DCMT-OR']

                self.docreqframe = LabelFrame(self.docreqwindow, width=560, height=240, bg="#008631", fg="white")
                self.docreqframe.place(x=10, y=10)

                self.policynum_label = Label(self.docreqframe,text="Policy#:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.policynum_label.place(x=20, y=20)
                self.policynum_label_output = Label(self.docreqframe, width=15,bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.policynum_label_output.place(x=80, y=20)

                self.email_label = Label(self.docreqframe,text="Email:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.email_label.place(x=200, y=20)
                self.email_labeloutput = Label(self.docreqframe, width=30, bg='white', fg='black', font=('Microsoft YaHei UI Light', 8))
                self.email_labeloutput.place(x=250, y=20)

                self.doccode_label = Label(self.docreqframe, text="DOCUMENT CODE:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.doccode_label.place(x=50, y=80)
                self.docreq_combobox = ttk.Combobox(self.docreqframe, width=30, values=document_list,textvariable=DOCREQVAR)
                self.docreq_combobox.place(x=180, y=80)
                show_details()

                self.generate_button = Button(self.docreqframe, text="Generate", font=('arial', 9, 'bold'),bg="#f5b32f", fg='white', border=0, padx=8, command=generate_document)
                self.generate_button.place(x=390, y=78)
                self.send_button = Button(self.docreqframe, text="Send Request", font=('arial', 9, 'bold'),bg="#5faae3", fg='white', border=0, padx=8, command=send_document)
                self.send_button.place(x=180, y=150)

        ############################################## END DOC-REQUEST ##########################################################



        ######################### START PAY_NOW ###########################################################
        def Pay_now():
            self.policy = Policynumber.get()
            if self.policy == "" or self.policy == "0" or self.policy == None:
                messagebox.showerror("", "No Policy Found")
            else:
                self.Pay_now_window = Toplevel()
                self.Pay_now_window.title("C.A.M.S /Pay-Now")
                self.Pay_now_window.geometry("380x260")
                self.Pay_now_window.config(bg='#008631')
                self.Pay_now_window.resizable(False, False)

                def show_payment():
                    global get_duedt,get_monthpaid,get_paymentbal,get_dur,get_payamount,get_fre,frequency
                    con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                    cur = con.cursor()
                    ### QUERY FOR FETCH POLICY##
                    sql3 = "SELECT DUE_DATE,MONTHS_PAID,PAYMENT_REMAINING,PAYMENT_DURATION,FREQUENCY,PAYMENT_TOTAL FROM tbl_payment JOIN tbl_policy ON POLICY_ID=PAYMENT_ID_FK WHERE tbl_policy.POLICY_NUM='"+str(pol_num)+"'"
                    cur.execute(sql3)
                    get_paymet_details=cur.fetchall()
                    for i in get_paymet_details:
                        get_duedt=i[0]
                        get_monthpaid=i[1]
                        get_paymentbal=i[2]
                        get_dur=i[3]
                        get_fre=i[4]
                        get_payamount=i[5]
                    self.payment_made_label_output.config(text=get_monthpaid)
                    self.payment_due_label_output.config(text=get_duedt)
                    self.amount_due_label_output.config(text=get_payamount)
                    paymentduration = get_dur
                    frequency = get_fre


                    ### Calculate the number of payments remaining FOR 10-YEARS
                    if paymentduration == "10-YEARS":
                        ### Calculate the number of payments remaining
                        payments_remaining = int(get_paymentbal)

                        #### Calculate the remaining payments for each period
                        if frequency == "Monthly":
                            monthly_remaining = payments_remaining
                            self.paymentleft_label.config(text='Total Monthly payments remaining:')
                            self.paymentleft_label_output.config(text=monthly_remaining)
                        elif frequency == "Quarterly":
                            quarter_remaining = payments_remaining / 3
                            self.paymentleft_label.config(text="Total Quarterly payments remaining:")
                            self.paymentleft_label_output.config(text=quarter_remaining)
                        elif frequency == "SemiAnnual":
                            semi_annual_remaining = payments_remaining / 6
                            self.paymentleft_label.config(text="Total Semi-Annual payments remaining:")
                            self.paymentleft_label_output.config(text=semi_annual_remaining)
                        elif frequency == "Annual":
                            annual_remaining = payments_remaining / 12
                            self.paymentleft_label.config(text="Total Annual payments remaining:")
                            self.paymentleft_label_output.config(text=annual_remaining)

                    ### Calculate the number of payments remaining FOR 5-YEARS
                    elif paymentduration == "5-YEARS":
                        payments_remaining = int(get_paymentbal)
                        #### Calculate the remaining payments for each period
                        if frequency == "Monthly":
                            monthly_remaining = payments_remaining
                            self.paymentleft_label.config(text="Total Monthly payments remaining:")
                            self.paymentleft_label_output.config(text=monthly_remaining)
                        elif frequency == "Quarterly":
                            quarter_remaining = payments_remaining / 3
                            self.paymentleft_label.config(text="Total Quarterly payments remaining:")
                            self.paymentleft_label_output.config(text=quarter_remaining)
                        elif frequency == "SemiAnnual":
                            semi_annual_remaining = payments_remaining / 6
                            self.paymentleft_label.config(text="Total Semi-Annual payments remaining:")
                            self.paymentleft_label_output.config(text=semi_annual_remaining)
                        elif frequency == "Annual":
                            annual_remaining = payments_remaining / 12
                            self.paymentleft_label.config(text="Total Annual payments remaining:")
                            self.paymentleft_label_output.config(text=annual_remaining)
                    else:
                        payments_remaining = int(get_paymentbal)
                        #### Calculate the remaining payments for each period
                        if frequency == "Monthly":
                            monthly_remaining = payments_remaining
                            self.paymentleft_label.config(text="Total Monthly payments remaining:")
                            self.paymentleft_label_output.config(text=monthly_remaining)
                        elif frequency == "Quarterly":
                            quarter_remaining = payments_remaining / 3
                            self.paymentleft_label.config(text="Total Quarterly payments remaining:")
                            self.paymentleft_label_output.config(text=quarter_remaining)
                        elif frequency == "SemiAnnual":
                            semi_annual_remaining = payments_remaining / 6
                            self.paymentleft_label.config(text="Total Semi-Annual payments remaining:")
                            self.paymentleft_label_output.config(text=semi_annual_remaining)
                        elif frequency == "Annual":
                            annual_remaining = payments_remaining / 12
                            self.paymentleft_label.config(text="Total Annual payments remaining:")
                            self.paymentleft_label_output.config(text=annual_remaining)


                ### QUERY TO INSERT PAYMENT TO DB
                def input_payment():
                    due_dt=get_duedt
                    monthspaid=int(get_monthpaid)
                    payment_bal=int(get_paymentbal)

                    if frequency=="Monthly":
                        date_range = datetime.timedelta(days=31)
                        due_date = date_range + due_dt
                        monthspaid=monthspaid+1
                        payment_bal=payment_bal-1
                    elif frequency=="Quarterly":
                        date_range = datetime.timedelta(days=92)
                        due_date=date_range+due_dt
                        monthspaid = monthspaid + 3
                        payment_bal = payment_bal - 3
                    elif frequency=="SemiAnnual":
                        date_range = datetime.timedelta(days=181)
                        due_date = date_range + due_dt
                        monthspaid = monthspaid + 6
                        payment_bal = payment_bal - 6
                    elif frequency=="Annual":
                        date_range = datetime.timedelta(days=365)
                        due_date = date_range + due_dt
                        monthspaid = monthspaid + 12
                        payment_bal = payment_bal - 12

                    ############ INSERT PAYMENT TO DB ##################
                    con = mysql.connector.connect(host='localhost', database='practicedb', user='root', password='')
                    cur = con.cursor()
                    sql1 = "select PAYMENT_ID_FK from tbl_payment join tbl_policy on POLICY_ID=PAYMENT_ID_FK where tbl_policy.POLICY_NUM='" + self.policy + "'"
                    cur.execute(sql1)
                    extract_payment = cur.fetchall()
                    for x in extract_payment:
                        pay_index = x[0]

                    pay_receivedt = datetime.date.today()
                    if messagebox.askyesno("", "Confirm Payment?"):
                        if payment_bal>=0:
                            sql1 = "INSERT INTO tbl_payment(POLICY_NUM,PAY_STARTDATE,DUE_DATE,amount,MONTHS_PAID,PAYMENT_REMAINING,PAYMENT_ID_FK)  VALUES (%s,%s,%s,%s,%s,%s,%s)"
                            val1 = (self.policy, pay_receivedt, due_date, get_payamount, monthspaid, payment_bal, pay_index)
                            cur.execute(sql1, val1)
                            con.commit()
                            messagebox.showinfo("", "Payment Process Complete!")
                            con.close()
                            if payment_bal == 0:
                                con = mysql.connector.connect(host='localhost', database='practicedb', user='root',password='')
                                cur = con.cursor()
                                sql4 = "update tbl_policy SET POLICY_STATUS='FULLY-PAID' WHERE POLICY_NUM='"+self.policy+"'"
                                cur.execute(sql4)
                                con.commit()
                                messagebox.showinfo("","Policy is Fully Paid!")
                                con.close()
                            else:
                                messagebox.showinfo("","Payment remaining"+" "+"Months:"+str(payment_bal))
                        else:
                            messagebox.showerror("Unable to accept payment","Policy is Full Paid")
                    else:
                        pass



                self.Pay_now_frame=LabelFrame(self.Pay_now_window, width=340, height=230, bg='#008631')
                self.Pay_now_frame.place(x=18,y=10)

                self.paymentleft_label=Label(self.Pay_now_frame, width=30, bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.paymentleft_label.place(x=10, y=10)
                self.paymentleft_label_output=Label(self.Pay_now_frame, width=10, bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.paymentleft_label_output.place(x=250, y=10)

                self.payment_made_label = Label(self.Pay_now_frame,text="Total Made Payments:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.payment_made_label.place(x=10, y=40)
                self.payment_made_label_output = Label(self.Pay_now_frame, width=10, bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.payment_made_label_output.place(x=160, y=40)

                self.payment_due_label = Label(self.Pay_now_frame,text="Current Due Date:", bg='#008631', fg='white', font=('Microsoft YaHei UI Light', 10))
                self.payment_due_label.place(x=10, y=70)
                self.payment_due_label_output = Label(self.Pay_now_frame, width=15, bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.payment_due_label_output.place(x=130, y=70)

                self.amount_due_label = Label(self.Pay_now_frame, text="Amount:", bg='#008631', fg='white',font=('Microsoft YaHei UI Light', 10))
                self.amount_due_label.place(x=10, y=100)
                self.amount_due_label_output = Label(self.Pay_now_frame, width=15, bg='white', fg='black',font=('Microsoft YaHei UI Light', 8))
                self.amount_due_label_output.place(x=130, y=100)
                show_payment()

                self.Paynow_button = Button(self.Pay_now_frame, text="Pay Now", padx=17, bg="#c9a324", font=("Arial", 10,"bold"), fg="white", border=0,activebackground="#ad8709", command=input_payment)
                self.Paynow_button.place(x=120, y=160)


        ########################################### END PAYNOW ##############################################


    ############################################### POLICY SELECTED MAIN WIDGETS (TAB 1) ###############################################################################
    ################################################# CENTER TREEVIEW FOR POLICY/ RIDER COVERAGE#################################################
        ####TREE VIEW QUERY###

        def show(event): ### KEY BINDED FUNCTION FOR F8 (SHOW POLICY DETAILS INCLUDING INSERT DATA TO TREEVIEW)#####
            global pol_num
            pol_num = Policynumber.get()
            self.trv.delete(*self.trv.get_children())### clear the treeview before insert
            #### ESTABLISHED CONNECTION###
            con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
            cur = con.cursor()
            ### QUERY FOR FETCH POLICY##
            sql="SELECT POLICY_NUM from tbl_policy where 1"
            cur.execute(sql)
            policies=cur.fetchall()
            policy_list=[] ### declaration of list to append all policies extracted from tbl_policy
            for i in policies: ##### Loop then append each item in the list every index from the tuple is in INT format
                policy_list.append(str(i[0])) #### convert each item to STR before append in policy_list[]
            if pol_num in policy_list: ########## checking policy input if exisiting in the list return Error if policy not found#####
                # if pol_num==index:##### Once POLICY is valid proceed#####
                # try:
                ### Query to extract data for Tab1####
                sql1 = "SELECT POLICY_ID,PRODUCT_NAME,PRODUCT_DURATION,REG_DATE,START_DATE,POLICY_STATUS,COVERAGE_AMOUNT,END_DATE,PAYMENT_TOTAL,lastname,middlename,firstname,INS_TYPE,MODE,FREQUENCY FROM tbl_policy A LEFT JOIN tbl_po B ON A.POLICY_ID=B.PO_ID WHERE a.POLICY_NUM='"+str(pol_num)+"'"
                cur.execute(sql1)
                records = cur.fetchall()
                for x in records: ## TREE VIEW INSERT VALUES###
                    self.trv.insert("", 'end', id=x[0], text=x[0],values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
                    ## treeview to assign to each variable
                    lastname = x[9]
                    middlename=x[10]
                    firstname=x[11]
                    status=x[5]
                    coverage=x[6]
                    reg_dt=x[3]
                    premium=x[8]
                    type=x[12]
                    mode=x[13]
                    frequency=x[14]
                    MODE=mode +"|"+frequency
                    if lastname==None and firstname==None and middlename==None:
                        fullname=""
                    else:
                        fullname = lastname + " " + firstname + " " + middlename

                    self.Policyowner_entry.config(state=NORMAL)
                    self.Policyowner_entry.insert(0, fullname)
                    self.Policyowner_entry.config(state=DISABLED)
                    self.Status_Label_output.config(text=status)
                    self.regdate_Label_output.config(text=reg_dt)

                    self.Modal_currency_output.config(text="PHP")
                    self.Modal_amount_output.config(text=premium)
                    self.Company_Label_output.config(text="MY COMPANY")
                    self.Instype_Label_output.config(text=type)
                    self.Mode_Label_output.config(text=MODE)
                    self.TDB_COV_ENTRY.config(text=coverage)


                ### QUERY FOR FETCH RIDER##
                sql2 = "SELECT RIDER_ID,RIDER,RIDER_DURATION,RIDER_REG_DATE,RIDER_STARTDATE,RIDER_STATUS,RIDER_COVERAGE,RIDER_END_DATE FROM tbl_rider INNER JOIN tbl_policy ON POLICY_ID=RIDER_ID_FK WHERE POLICY_NUM='"+str(pol_num)+"'"
                cur.execute(sql2)
                records2 = cur.fetchall()
                con.rollback()
                con.close()
                for x in records2:

                    self.trv.insert("", 'end', id=x[1], text=x[0], values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
                    rider_name=x[1]
                    rider_coverage=x[6]
                    if rider_name=="Enhance Critical Illness":
                        self.ECI_COV_ENTRY.config(text=rider_coverage)
                    elif rider_name=="Accidental Death Benefit":
                        self.ADB_COV_ENTRY.config(text=coverage)

                show_po_ins_details()  #### THIS IS TO CALL THE FUNCTION CREATED BELOW TO TRIGGER CLIENT INFORMATION IN THE NOTEBOOK AREA######
                show_bene()
                show_duedate()
                # except:
                #     messagebox.showinfo("All details displayed successfully!","No Riders found.")
            else:
                messagebox.showerror("","No Policy Found")  ### This returns error if policy not existing###
                clear("")

        def show_duedate():
            try:
                con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                cur = con.cursor()
                ### QUERY FOR FETCH POLICY##
                sql3 = "SELECT DUE_DATE FROM tbl_payment JOIN tbl_policy ON POLICY_ID=PAYMENT_ID_FK WHERE tbl_policy.POLICY_NUM='"+str(pol_num)+"' ORDER BY DUE_DATE DESC"
                cur.execute(sql3)
                getdue=cur.fetchone()
                print(getdue)
                due_date=getdue[0]
                print(due_date)
                self.PTD_output.config(text=due_date)
            except:
                messagebox.showerror("Failed to display DUE DATE","Please process the Initial payment!")


        def clear(event): ### KEY BINDED FUNCTION FOR F6 (CLEAR POLICY DETAILS INCLUDING INSERT DATA TO TREEVIEW)#####
            self.PN_entry.insert(0,"")
            self.trv.delete(*self.trv.get_children())
            self.trvbene.delete(*self.trvbene.get_children())
            self.Policyowner_entry.config(state=NORMAL)
            self.PN_entry.delete(0,END)
            self.Policyowner_entry.delete(0, END)
            self.Policyowner_entry.config(state=DISABLED)
            self.Policyowner_entry.delete(0, END)
            self.Status_Label_output.config(text="")
            self.regdate_Label_output.config(text="")
            self.PTD_output.config(text="")
            self.Modal_currency_output.config(text="")
            self.Modal_amount_output.config(text="")
            self.Company_Label_output.config(text="")
            self.Instype_Label_output.config(text="")
            self.Mode_Label_output.config(text="")
            self.TDB_COV_ENTRY.config(text="")
            self.ADB_COV_ENTRY.config(text="")
            self.ECI_COV_ENTRY.config(text="")
            self.FNAME_ENTRY_PO.config(text="")
            self.MNAME_ENTRY_PO.config(text="")
            self.LNAME_ENTRY_PO.config(text="")
            self.AGE_ENTRY_PO.config(text="")
            self.DOB_ENTRY_PO.config(text="")
            self.CSTATUS_ENTRY_PO.config(text="")
            self.PROFESSION_ENTRY_PO.config(text="")
            self.GENDER_ENTRY_PO.config(text="")
            self.FNAME_ENTRY_INS.config(text="")
            self.MNAME_ENTRY_INS.config(text="")
            self.LNAME_ENTRY_INS.config(text="")
            self.AGE_ENTRY_INS.config(text="")
            self.DOB_ENTRY_INS.config(text="")
            self.CSTATUS_ENTRY_INS.config(text="")
            self.PROFESSION_ENTRY_INS.config(text="")
            self.GENDER_ENTRY_INS.config(text="")
        #####KEY BINDINGS####
        self.master10.bind("<F8>",show)
        self.master10.bind("<F6 >",clear)



        ##### FRAMES AND WIDGETS###

        self.Policy_frame = LabelFrame(self.master10, width=1080, height=600, bg='#008631')
        self.Policy_frame.place(x=10,y=40)

        ###### NAVIGATION BUTTONS#####
        self.Policyinfo_button = Button(self.Policy_frame, text="Policy Info", padx=17, bg="white", compound="left",font=("Arial", 10), fg="black", border=0, activebackground="lightgreen",command=Policyinfo)
        self.Policyinfo_button.place(x=10, y=10)

        self.Paymentinfo_button = Button(self.Policy_frame, text="Payment Info", padx=17, bg="white", compound="left",font=("Arial", 10), fg="black", border=0, activebackground="lightgreen",command=payment)
        self.Paymentinfo_button.place(x=111, y=10)

        self.History_button = Button(self.Policy_frame, text="Payment History", padx=17, bg="white", compound="left",font=("Arial", 10), fg="black", border=0, activebackground="lightgreen",command=history)
        self.History_button.place(x=228, y=10)

        self.Docreq_button = Button(self.Policy_frame, text="Docs.Req", padx=17, bg="white", compound="left",font=("Arial", 10), fg="black", border=0, activebackground="lightgreen",command=documentreq)
        self.Docreq_button.place(x=366, y=10)

        self.Paynow_button=Button(self.Policy_frame, text="Pay Now", padx=17, bg="white", compound="left",font=("Arial", 10), fg="black", border=0, activebackground="lightgreen",command=Pay_now)
        self.Paynow_button.place(x=464,y=10)

        self.Back_button = Button(self.Policy_frame, text="Back", padx=17, bg="#d9ae14", compound="left",font=("Arial", 10), fg="white", border=0, activebackground="#7fc4f0", command=Back)
        self.Back_button.place(x=890, y=10)

        self.Home_button = Button(self.Policy_frame, text="Home", padx=17, bg="#4cafed", compound="left",font=("Arial", 10), fg="white", border=0, activebackground="#7fc4f0",command=home)
        self.Home_button.place(x=970, y=10)


        ##### ENTRY VARIABLES#####
        #### GET Policy from entry field####
        Policynumber = StringVar(value="0")
        Policyowner = StringVar()
        #### DISPLAY AND ENTRY####
        self.Policy_Label = Label(self.Policy_frame, text="Policy#: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Policy_Label.place(x=10, y=50)
        self.PN_entry = Entry(self.Policy_frame, width=16, fg='black', border=0, font=4, textvariable=Policynumber)
        self.PN_entry.place(x=80, y=50)
        self.Policy_Label = Label(self.Policy_frame, text="Policy Owner: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Policy_Label.place(x=240, y=50)
        self.Policyowner_entry = Entry(self.Policy_frame, width=30, fg='black', border=0, font=4, textvariable=Policyowner)
        self.Policyowner_entry.place(x=355, y=50)

        self.Status_Label = Label(self.Policy_frame, text="Status: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light',11, "bold"))
        self.Status_Label.place(x=10, y=80)
        self.Status_Label_output = Label(self.Policy_frame, bg='white', border=0,width=16, fg='black',font=('Microsoft YaHei UI Light',10 , "bold"))
        self.Status_Label_output.place(x=80, y=80)

        self.regdate_Label = Label(self.Policy_frame, text="RegDate: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.regdate_Label.place(x=240, y=80)
        self.regdate_Label_output = Label(self.Policy_frame, bg='white', border=0, width=11, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.regdate_Label_output.place(x=320, y=80)

        self.PTD_Label = Label(self.Policy_frame, text="PTD: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.PTD_Label.place(x=430, y=80)
        self.PTD_output = Label(self.Policy_frame, bg='white', border=0, width=11, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PTD_output.place(x=480, y=80)


        self.Modal_Label = Label(self.Policy_frame, text="ModalPremium: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Modal_Label.place(x=600, y=80)
        self.Modal_currency_output = Label(self.Policy_frame, bg='white', border=0, width=7, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.Modal_currency_output.place(x=730, y=80)
        self.Modal_amount_output = Label(self.Policy_frame, bg='white', border=0, width=11, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.Modal_amount_output.place(x=796, y=80)

        self.Company_Label = Label(self.Policy_frame, text="Company: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Company_Label.place(x=10, y=110)
        self.Company_Label_output = Label(self.Policy_frame, bg='white', border=0, width=15, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.Company_Label_output.place(x=90, y=110)

        self.Instype_Label = Label(self.Policy_frame, text="Ins type: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Instype_Label.place(x=240, y=110)
        self.Instype_Label_output = Label(self.Policy_frame, bg='white', border=0, width=30, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.Instype_Label_output.place(x=310, y=110)

        self.Mode_Label = Label(self.Policy_frame, text="Mode: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.Mode_Label.place(x=600, y=110)
        self.Mode_Label_output = Label(self.Policy_frame, bg='white', border=0, width=15, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.Mode_Label_output.place(x=655, y=110) ####### FREQUENCY + REGULAR######


        ###### MID TABS ####

        self.notebook=ttk.Notebook(self.Policy_frame)
        self.tab1=Frame(self.notebook,background="white") ### new frame for tab1
        self.tab2=Frame(self.notebook,background="white") ### new frame for tab2
        self.tab3 = Frame(self.notebook, background="white")  ### new frame for tab2

        self.notebook.add(self.tab1,text="Coverage Summary")
        self.notebook.add(self.tab2, text="Client Information")
        self.notebook.add(self.tab3, text="Beneficiaries")
        self.notebook.place(x=20,y=140)



        ########### Tab 1###############################
        self.trv = ttk.Treeview(self.tab1, columns=[1, 2, 3, 4, 5, 6, 7, 8,9], show="headings", height="12")
        self.trv.grid(row=0, column=0)

        # width of columns and alignment
        self.trv.column("1", width=50, anchor='c')
        self.trv.column("2", width=200, anchor='c')
        self.trv.column("3", width=50, anchor='c')
        self.trv.column("4", width=120, anchor='c')
        self.trv.column("5", width=120, anchor='c')
        self.trv.column("6", width=120, anchor='c')
        self.trv.column("7", width=120, anchor='c')
        self.trv.column("8", width=120, anchor='c')
        self.trv.column("9", width=120, anchor='c')

        # Headings
        # respective columns
        self.trv.heading("1", text="No.")
        self.trv.heading("2", text="Plan")
        self.trv.heading("3", text="Dur")
        self.trv.heading("4", text="Reg Date")
        self.trv.heading("5", text="Start Date")
        self.trv.heading("6", text="Status")
        self.trv.heading("7", text="CoverageAmount")
        self.trv.heading("8", text="Expiration Date")
        self.trv.heading("9", text="Premium")


        ##### LOWER OUTPUT WIDGET COVERAGE OUTPUT#####
        self.coverage_frame=LabelFrame(self.master10, width=1080, height=160, bg='#008631')
        self.coverage_frame.place(x=10, y=480)

        self.TDB_COV_LABEL=Label(self.coverage_frame, text="Total Death Benefit: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.TDB_COV_LABEL.place(x=90,y=20)
        self.TDB_COV_ENTRY = Label(self.coverage_frame, width=12, text=" ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.TDB_COV_ENTRY.place(x=310, y=20)

        self.ADB_COV_LABEL = Label(self.coverage_frame, text="Accidental Death Benefit (ADB): ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.ADB_COV_LABEL.place(x=50,y=50)
        self.ADB_COV_ENTRY = Label(self.coverage_frame, width=12, text=" ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.ADB_COV_ENTRY.place(x=310, y=50)

        self.ECI_COV_LABEL = Label(self.coverage_frame, text="Enhanced Critical Illness Coverage (ECI): ", bg='#008631',border=0, fg='white', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.ECI_COV_LABEL.place(x=20, y=80)
        self.ECI_COV_ENTRY = Label(self.coverage_frame, width=12, text=" ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 11, "bold"))
        self.ECI_COV_ENTRY.place(x=310, y=80)



        #################################### END OF Tab 1 COVERAGE ##################################################


        ########################################## START TAB 2 CLIENT INFORMATION #############################################################
        #########POLICY OWNER #################
        def show_po_ins_details():
            global getpolicy
            getpolicy=Policynumber.get()
            con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
            cur = con.cursor()
            ### QUERY FOR FETCH POLICY##
            sql3 = "select * FROM tbl_policy INNER JOIN tbl_po ON POLICY_NUM='" + str(getpolicy) + "' AND POLICY_ID=PO_ID INNER JOIN tbl_insured ON POLICY_ID=INS_ID"
            cur.execute(sql3)
            items = cur.fetchall()

            if items:
                x=items[0]### EXTRACTING TUPLE FROM LIST TO ACCESS VARIABLE PER INDEX IN THE TUPLE
                ##### assigned variables from x ###
                PO_FNAME = x[15]
                PO_MNAME = x[16]
                PO_LNAME = x[17]
                PO_AGE = x[18]
                PO_DOB = x[19]
                PO_GENDER = x[20]
                PO_PROFESSION = x[21]
                PO_CSTATUS = x[22]
                INS_FNAME = x[24]
                INS_MNAME = x[25]
                INS_LNAME = x[26]
                INS_AGE = x[27]
                INS_DOB = x[28]
                INS_PROFESSION = x[29]
                INS_CSTATUS = x[30]
                INS_GENDER = x[31]

                self.FNAME_ENTRY_PO.config(text=PO_FNAME)
                self.MNAME_ENTRY_PO.config(text=PO_MNAME)
                self.LNAME_ENTRY_PO.config(text=PO_LNAME)
                self.AGE_ENTRY_PO.config(text=PO_AGE)
                self.DOB_ENTRY_PO.config(text=PO_DOB)
                self.CSTATUS_ENTRY_PO.config(text=PO_CSTATUS)
                self.PROFESSION_ENTRY_PO.config(text=PO_PROFESSION)
                self.GENDER_ENTRY_PO.config(text=PO_GENDER)
                self.FNAME_ENTRY_INS.config(text=INS_FNAME)
                self.MNAME_ENTRY_INS.config(text=INS_MNAME)
                self.LNAME_ENTRY_INS.config(text=INS_LNAME)
                self.AGE_ENTRY_INS.config(text=INS_AGE)
                self.DOB_ENTRY_INS.config(text=INS_DOB)
                self.CSTATUS_ENTRY_INS.config(text=INS_CSTATUS)
                self.PROFESSION_ENTRY_INS.config(text=INS_PROFESSION)
                self.GENDER_ENTRY_INS.config(text=INS_GENDER)

            else:
                messagebox.showerror("", "Unable to Display Null Values")
            return getpolicy
        ################## CONTACT AND ADDRESS FOR POLICY OWNER AND INSURED ######################################################

        ############## START ADDRESS #################
        def address_fuction_po():
            self.address_window = Toplevel()
            self.address_window.title("C.A.M.S /ADDRESS Policy Owner")
            self.address_window.geometry("790x200")
            self.address_window.config(bg='#008631')
            self.address_window.resizable(False, False)

            def showaddress_po():
                getpolicy=show_po_ins_details() #### RETRIEVE POLICY NUMBER INPUT####
                if getpolicy=="" or getpolicy=="0":
                    pass
                else:
                    self.trvaddress_po.delete(*self.trvaddress_po.get_children())
                    con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                    cur = con.cursor()
                    ### Query to extract contact of policy owner to contacts ####
                    sql="SELECT POLICY_NUM,PO_ID,ADDRESS_ID,address,city,province,zipcode,country,type FROM tbl_policy INNER JOIN tbl_po ON POLICY_ID=PO_ID INNER JOIN tbladdress_po ON PO_ID=PO_ADDRESS_ID WHERE POLICY_NUM='"+getpolicy+"'"
                    cur.execute(sql)
                    address = cur.fetchall()
                    addressid=1
                    for x in address:  ## TREE VIEW INSERT VALUES###
                        self.trvaddress_po.insert("", 'end', id=x[2], text=x[0],values=(x[2],addressid,x[3],x[4],x[5],x[6],x[7],x[8]))
                        addressid=addressid+1

            def add_address_po():
                self.add_address_window = Toplevel()
                self.add_address_window.title("C.A.M.S /ADD ADDRESS Policy Owner")
                self.add_address_window.geometry("400x300")
                self.add_address_window.config(bg='#008631')
                self.add_address_window.resizable(False, False)

                def inputaddress_po():
                    getpolicy = show_po_ins_details()
                    getaddress_po = self.ADDRESS_PO_ENTRY.get(1.0,END)
                    getcity_po = CITYVAR_PO.get()
                    getprovince_po = PROVINCEVAR_PO.get()
                    getzipcode_po = ZIPCODEVAR_PO.get()
                    getcountry_po=COUNTRYVAR_PO.get()
                    getaddress_type_po=ADDRESSTYPE_PO.get()

                    try:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "Select POLICY_ID,PO_ID,address,city,province,zipcode,country,type FROM tbl_policy INNER JOIN tbl_po on POLICY_ID=PO_ID INNER JOIN tbladdress_po ON PO_ID=PO_ADDRESS_ID WHERE POLICY_NUM='" + getpolicy + "'"
                        cur.execute(sql)
                        address_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        address_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = address_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        addressindex = items[0]

                        sql = "INSERT INTO tbladdress_po(address,city,province,zipcode,country,type,PO_ADDRESS_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        val1 = (getaddress_po, getcity_po, getprovince_po, getzipcode_po,getcountry_po,getaddress_type_po,addressindex)
                        cur.execute(sql, val1)
                        messagebox.showinfo("", "Address added successfully")
                        con.commit()
                        con.close()


                        self.ADDRESS_PO_ENTRY.delete(1.0,END)
                        self.CITY_PO_ENTRY.delete(0,END)
                        self.PROVINCE_PO_ENTRY.delete(0,END)
                        self.ZIPCODE_PO_ENTRY.delete(0,END)
                        self.COUNTRY_PO_ENTRY.delete(0,END)
                        self.addresstype_combobox.set(value="")
                    except:
                        messagebox.showerror("", "Unable to Process request")
                def cancel():
                    self.add_address_window.destroy()

                #####ADD FUNCTION VARIABLES#####

                address_type=['Primary','Alternate']
                CITYVAR_PO=StringVar()
                PROVINCEVAR_PO=StringVar()
                ZIPCODEVAR_PO=StringVar()
                COUNTRYVAR_PO=StringVar()
                ADDRESSTYPE_PO=StringVar()

                self.ADDRESS_PO_LABEL = Label(self.add_address_window, text="ADDRESS: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESS_PO_LABEL.place(x=35, y=20)
                self.ADDRESS_PO_ENTRY = Text(self.add_address_window, width=30,height=2)
                self.ADDRESS_PO_ENTRY.place(x=150, y=20)

                self.CITY_PO_LABEL = Label(self.add_address_window, text="CITY: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CITY_PO_LABEL.place(x=50, y=80)
                self.CITY_PO_ENTRY = Entry(self.add_address_window, width=25, textvariable=CITYVAR_PO)
                self.CITY_PO_ENTRY.place(x=150, y=80)

                self.PROVINCE_PO_LABEL = Label(self.add_address_window, text="PROVINCE: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.PROVINCE_PO_LABEL.place(x=30, y=105)
                self.PROVINCE_PO_ENTRY = Entry(self.add_address_window, width=25, textvariable=PROVINCEVAR_PO)
                self.PROVINCE_PO_ENTRY.place(x=150 , y=105)

                self.ZIPCODE_PO_LABEL = Label(self.add_address_window, text="ZIPCODE: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ZIPCODE_PO_LABEL.place(x=30, y=130)
                self.ZIPCODE_PO_ENTRY = Entry(self.add_address_window, width=25, textvariable=ZIPCODEVAR_PO)
                self.ZIPCODE_PO_ENTRY.place(x=150, y=130)

                self.COUNTRY_PO_LABEL = Label(self.add_address_window, text="COUNTRY CODE: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.COUNTRY_PO_LABEL.place(x=15, y=155)
                self.COUNTRY_PO_ENTRY = Entry(self.add_address_window, width=25, textvariable=COUNTRYVAR_PO)
                self.COUNTRY_PO_ENTRY.place(x=150, y=155)


                self.ADDRESSTYPE_PO_LABEL = Label(self.add_address_window, text="Type: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESSTYPE_PO_LABEL.place(x=50, y=180)
                self.addresstype_combobox = ttk.Combobox(self.add_address_window, width=10, values=address_type,textvariable=ADDRESSTYPE_PO)
                self.addresstype_combobox.place(x=150, y=180)


                self.Proceed_button = Button(self.add_address_window, text="Proceed", padx=8, pady=2, bg="#149c29",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#43c92e", command=inputaddress_po)
                self.Proceed_button.place(x=110, y=220)
                self.Cancel_button = Button(self.add_address_window, text="Cancel", padx=10, pady=2, bg="#d9ae14",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=190, y=220)
                ############################### END OF ADD ADDRESS##############################


            ##### DELETE / UPDATE ADDRESS POLICY OWNER #####
            def deleteupdate_po():
                self.deleteupdateaddress_window = Toplevel()
                self.deleteupdateaddress_window.title("C.A.M.S /UPDATE/DELETE Address Policy Owner")
                self.deleteupdateaddress_window.geometry("400x300")
                self.deleteupdateaddress_window.config(bg='#008631')
                self.deleteupdateaddress_window.resizable(False, False)

                def address_po_show():
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy=="0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        global row
                        row = ROWNUMBER_VAR_PO.get()
                        ##### EXTRACT DB FOR CONTACT DETAILS TO SHOW on UPDATE DELETE WINDOW#####
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "SELECT * FROM tbladdress_po WHERE  ADDRESS_ID='" +str(row)+ "'"
                        cur.execute(sql)
                        address_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        # print(address_indexes)
                        address_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = address_indexes[0]  ### variable x is not holding the last tuple index
                        # print(x)
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        # print(items)
                        ID_PO = str(items[0])
                        address_po = items[1]
                        city_po = items[2]
                        province_po = items[3]
                        zipcode_po = items[4]
                        country_po = items[5]
                        addtype_po = items[6]


                        self.ADDRESS_PO_ENTRY.insert(1.0,address_po)
                        self.CITY_PO_ENTRY.insert(0, city_po)
                        self.PROVINCE_PO_ENTRY.insert(0, province_po)
                        self.ZIPCODE_PO_ENTRY.insert(0, zipcode_po)
                        self.COUNTRY_PO_ENTRY.insert(0, country_po)
                        self.ADDRESSTYPE_PO_ENTRY.insert(0,addtype_po)
                        self.ROW_PO_ENTRY.config(state=DISABLED)


                def delete_po():  ### DELETE FUNCTION ###
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        self.ROW_PO_ENTRY.config(state=NORMAL)
                        messagebox.showwarning("", "You are about to delete this contact?")
                        if messagebox.askokcancel("", "Proceed to Delete?"):
                            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                            cur = con.cursor()
                            sql1 = "Delete from tbladdress_po WHERE ADDRESS_ID=%s"
                            val1 = (row,)
                            cur.execute(sql1, val1)
                            con.commit()
                            messagebox.showinfo("", "Address Deleted!")
                            ### DELETE ENTRY DATA AFTER DELETE TO TABLE###

                            self.ADDRESS_PO_ENTRY.delete(1.0, END)
                            self.CITY_PO_ENTRY.delete(0, END)
                            self.PROVINCE_PO_ENTRY.delete(0, END)
                            self.ZIPCODE_PO_ENTRY.delete(0, END)
                            self.COUNTRY_PO_ENTRY.delete(0, END)
                            self.addresstype_po_combobox.set(value="")
                            showaddress_po()
                        else:
                            pass

                def updateaddress_po():
                    address_po=self.ADDRESS_PO_ENTRY.get(1.0,END)
                    city=CITYVAR_PO.get()
                    province=PROVINCEVAR_PO.get()
                    zipcode=ZIPCODEVAR_PO.get()
                    country=COUNTRYVAR_PO.get()
                    add_type=ADDRESSTYPEVAR_PO.get()

                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbladdress_po SET address =%s, city =%s,province =%s, zipcode =%s , country=%s , type=%s WHERE ADDRESS_ID= %s"
                        val2 = (address_po,city,province,zipcode,country,add_type,row)
                        cur.execute(sql2, val2)
                        con.commit()
                        messagebox.showinfo("", "Address Updated!")

                        ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                        self.ADDRESS_PO_ENTRY.delete(1.0, END)
                        self.CITY_PO_ENTRY.delete(0, END)
                        self.PROVINCE_PO_ENTRY.delete(0, END)
                        self.ZIPCODE_PO_ENTRY.delete(0, END)
                        self.COUNTRY_PO_ENTRY.delete(0, END)
                        self.addresstype_po_combobox.set(value="")
                        showaddress_po()

                def cancel_po():
                    self.deleteupdateaddress_window.destroy()


                ### UPDATE/DELETE VARIABLES###
                address_type = ['Primary', 'Alternate']
                ROWNUMBER_VAR_PO = StringVar()
                CITYVAR_PO = StringVar()
                PROVINCEVAR_PO = StringVar()
                ZIPCODEVAR_PO = StringVar()
                COUNTRYVAR_PO=StringVar()
                ADDRESSTYPEVAR_PO=StringVar()

                self.ROW_LABEL = Label(self.deleteupdateaddress_window, text="Row No: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ROW_LABEL.place(x=40, y=20)
                self.ROW_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=10, textvariable=ROWNUMBER_VAR_PO)
                self.ROW_PO_ENTRY.place(x=120, y=20)

                self.ADDRESS_LABEL = Label(self.deleteupdateaddress_window, text="Address: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESS_LABEL.place(x=40, y=45)
                self.ADDRESS_PO_ENTRY = Text(self.deleteupdateaddress_window, width=30, height=2)
                self.ADDRESS_PO_ENTRY.place(x=120, y=45)

                self.CITY_LABEL = Label(self.deleteupdateaddress_window, text="City: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CITY_LABEL.place(x=55, y=105)
                self.CITY_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=25, textvariable=CITYVAR_PO)
                self.CITY_PO_ENTRY.place(x=120, y=105)

                self.PROVINCE_LABEL = Label(self.deleteupdateaddress_window, text="Province: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.PROVINCE_LABEL.place(x=50, y=130)
                self.PROVINCE_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=25, textvariable=PROVINCEVAR_PO)
                self.PROVINCE_PO_ENTRY.place(x=120, y=130)

                self.ZIPCODE_LABEL = Label(self.deleteupdateaddress_window, text="Zipcode: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ZIPCODE_LABEL.place(x=50, y=155)
                self.ZIPCODE_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=25, textvariable=ZIPCODEVAR_PO)
                self.ZIPCODE_PO_ENTRY.place(x=120, y=155)

                self.COUNTRY_LABEL = Label(self.deleteupdateaddress_window, text="Country: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.COUNTRY_LABEL.place(x=50, y=180)
                self.COUNTRY_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=25, textvariable=COUNTRYVAR_PO)
                self.COUNTRY_PO_ENTRY.place(x=120, y=180)

                self.ADDRESSTYPE_LABEL = Label(self.deleteupdateaddress_window, text="Type: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESSTYPE_LABEL.place(x=50, y=205)
                self.ADDRESSTYPE_PO_ENTRY = Entry(self.deleteupdateaddress_window, width=13, textvariable=ADDRESSTYPEVAR_PO)
                self.ADDRESSTYPE_PO_ENTRY.place(x=120, y=205)
                self.addresstype_po_combobox = ttk.Combobox(self.deleteupdateaddress_window, width=10, values=address_type,textvariable=ADDRESSTYPEVAR_PO)
                self.addresstype_po_combobox.place(x=210, y=204)


                self.Select_button = Button(self.deleteupdateaddress_window, text="Select", padx=6, bg="#52c5f2",font=("Arial", 8, "bold"), fg="white", border=0, activebackground="#0782b3",command=address_po_show)
                self.Select_button.place(x=195, y=18)
                self.Proceed_button = Button(self.deleteupdateaddress_window, text="Update", padx=8, pady=2,bg="#28b090", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=updateaddress_po)
                self.Proceed_button.place(x=75, y=240)
                self.Proceed_button = Button(self.deleteupdateaddress_window, text="Delete", padx=8, pady=2,bg="#ed2f2f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=delete_po)
                self.Proceed_button.place(x=150, y=240)
                self.Cancel_button = Button(self.deleteupdateaddress_window, text="Cancel", padx=10, pady=2,bg="#edc42f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel_po)
                self.Cancel_button.place(x=220, y=240)



            ##### TREE VIEW GENERATOR for ADDRESS OF POLICY OWNER ####
            self.Addressframe = Frame(self.address_window, width=530, height=350)
            self.Addressframe.place(x=15, y=5)
            self.trvaddress_po = ttk.Treeview(self.Addressframe, columns=[1, 2, 3, 4, 5, 6, 7, 8], show="headings", height="5")
            self.trvaddress_po.grid(row=0, column=0, sticky='n')


            # width of columns and alignment
            self.trvaddress_po.column("1", width=70,anchor='c')
            self.trvaddress_po.column("2", width=50, anchor='c')
            self.trvaddress_po.column("3", width=200, anchor='c')
            self.trvaddress_po.column("4", width=100, anchor='c')
            self.trvaddress_po.column("5", width=100, anchor='c')
            self.trvaddress_po.column("6", width=80, anchor='c')
            self.trvaddress_po.column("7", width=80, anchor='c')
            self.trvaddress_po.column("8", width=80, anchor='c')
            # Headings
            # respective columns
            self.trvaddress_po.heading("1", text="ROW NO") ### WILL BE THE ADDRESS ID FROM TB
            self.trvaddress_po.heading("2", text="ID") ### GENERATE AND WILL BE AUTO INCREMENT BY 1 ONCE DISPLAYED IN TREEVIEW
            self.trvaddress_po.heading("3", text="ADDRESS")
            self.trvaddress_po.heading("4", text="CITY")
            self.trvaddress_po.heading("5", text="PROVINCE")
            self.trvaddress_po.heading("6", text="ZIPCODE")
            self.trvaddress_po.heading("7", text="COUNTRY")
            self.trvaddress_po.heading("8", text="TYPE")

            self.Add_button = Button(self.address_window, text="ADD", padx=50, pady=2, bg="#4cafed",font=("Arial", 10, "bold"), fg="white", border=0, activebackground="#7fc4f0",command=add_address_po)
            self.Add_button.place(x=30, y=140)
            self.Delete_button = Button(self.address_window, text="DELETE/UPDATE", padx=20, pady=2, bg="#e65d45",font=("Arial", 10, "bold"), fg="white", border=0, activebackground='#941f0a',command=deleteupdate_po)
            self.Delete_button.place(x=180, y=140)
            showaddress_po()
        ######################### END OF ADDRESS#################################################



        ############ START  CONTACTS #############################################################
        def contacts_fuction_po():
            ######OPEN CONTACTS WINDOW W/C CHILD WINDOW ON THE TOP OF MAINWINDOW (IF MAIN WINDOW(PARENT) IS CLOSE, CONTACT WINDOW (CHILD) WILL ALSO BE CLOSE ) #####
            self.contact_window=Toplevel()
            self.contact_window.title("C.A.M.S /Contacts Policy Owner")
            self.contact_window.geometry("790x170")
            self.contact_window.config(bg='#008631')
            self.contact_window.resizable(False, False)

            def showcontact_po():
                getpolicy=show_po_ins_details() #### RETRIEVE POLICY NUMBER INPUT####
                if getpolicy=="" or getpolicy=="0":
                    messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                             "Failed to display ADDRESS ")
                else:
                    self.trvcontact.delete(*self.trvcontact.get_children())
                    con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                    cur = con.cursor()
                    ### Query to extract contact of policy owner to contacts ####
                    sql="SELECT POLICY_NUM,PO_ID,CONTACT_ID_PO,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE FROM tbl_policy INNER JOIN tbl_po ON POLICY_ID=PO_ID INNER JOIN tbl_contact_po ON PO_ID=CONTACT_FK_PO WHERE POLICY_NUM='"+getpolicy+"'"
                    cur.execute(sql)
                    contacts = cur.fetchall()
                    contactid=1
                    for x in contacts:  ## TREE VIEW INSERT VALUES###
                        self.trvcontact.insert("", 'end', id=x[2], text=x[0],values=(x[2],contactid,x[3],x[4],x[5],x[6]))
                        contactid=contactid+1


            ############## ADD CONTACT ###############

            def add():  #### THIS OPENS NEW WINDOW CHILD WINDOW OF CONTACTS  (IF CONTACT WINDOW(PARENT) IS CLOSE, ADDCONTACT WINDOW (CHILD) WILL ALSO BE CLOSE )
                self.addcontact_window = Toplevel()
                self.addcontact_window.title("C.A.M.S /ADDContacts Policy Owner")
                self.addcontact_window.geometry("370x200")
                self.addcontact_window.config(bg='#008631')
                self.addcontact_window.resizable(False, False)

                def addcontact():
                    getpolicy = show_po_ins_details()
                    mobile = MOBILEVAR_PO.get()
                    landline = LANDLINEVAR_PO.get()
                    email = EMAILVAR_PO.get()
                    cont_type=CONTACTTYPE_PO.get()
                    try:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "Select POLICY_ID,PO_ID,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE FROM tbl_policy INNER JOIN tbl_po on POLICY_ID=PO_ID INNER JOIN tbl_contact_po ON PO_ID=CONTACT_FK_PO WHERE POLICY_NUM='"+getpolicy+"'"
                        cur.execute(sql)
                        contact_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        contact_indexes.reverse()  ### reversed the fetch result to get the last index
                        x=contact_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        contactindex = items[0]

                        sql = "INSERT INTO tbl_contact_po(MOBILE,LANDLINE,EMAIL,CONTACT_TYPE,CONTACT_FK_PO) VALUES (%s,%s,%s,%s,%s)"
                        val1=(mobile,landline,email,cont_type,contactindex)
                        cur.execute(sql,val1)
                        messagebox.showinfo("", "Contact added successfully")
                        con.commit()
                        con.close()
                        self.MOBILE_ENTRY.delete(0,END)
                        self.LANDLINE_ENTRY.delete(0, END)
                        self.EMAIL_ENTRY.delete(0, END)
                        self.contacttype_combobox.set(value="")
                    except:
                        messagebox.showerror("", "Unable to Process request")

                #### CANCEL ADD CONTACT
                def cancel():
                    self.addcontact_window.destroy()

                ### TEXT VARIABLES###
                MOBILEVAR_PO = StringVar()
                LANDLINEVAR_PO = StringVar()
                EMAILVAR_PO = StringVar()
                CONTACTTYPE_PO=StringVar()
                contact_type=['Primary','Alternate']

                self.MOBILE_LABEL = Label(self.addcontact_window, text="Mobile: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.MOBILE_LABEL.place(x=50, y=20)
                self.MOBILE_ENTRY = Entry(self.addcontact_window, width=25,textvariable=MOBILEVAR_PO)
                self.MOBILE_ENTRY.place(x=120, y=20)

                self.LANDLINE_LABEL = Label(self.addcontact_window, text="Landline: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.LANDLINE_LABEL.place(x=40, y=45)
                self.LANDLINE_ENTRY = Entry(self.addcontact_window, width=25, textvariable=LANDLINEVAR_PO)
                self.LANDLINE_ENTRY.place(x=120, y=45)

                self.EMAIL_LABEL = Label(self.addcontact_window, text="Email: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.EMAIL_LABEL.place(x=55, y=70)
                self.EMAIL_ENTRY = Entry(self.addcontact_window, width=25, textvariable=EMAILVAR_PO)
                self.EMAIL_ENTRY.place(x=120, y=70)

                self.CONTACTTYPE_LABEL = Label(self.addcontact_window, text="Type: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CONTACTTYPE_LABEL.place(x=55, y=100)
                self.contacttype_combobox = ttk.Combobox(self.addcontact_window, width=10, values=contact_type,textvariable=CONTACTTYPE_PO)
                self.contacttype_combobox.place(x=120, y=100)



                self.Proceed_button = Button(self.addcontact_window, text="Proceed", padx=8, pady=2, bg="#149c29",font=("Arial", 10, "bold"), fg="white", border=0, activebackground="#7fc4f0",command=addcontact)
                self.Proceed_button.place(x=120, y=140)
                self.Cancel_button = Button(self.addcontact_window, text="Cancel", padx=10, pady=2, bg="#d9ae14",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=200, y=140)
            ####################################################### END ADD WINDOW #####################################################


            ################################### DELETE / UPDATE WINDOW #################################################################
            def delete():
                self.deleteupdatecontact_window = Toplevel()
                self.deleteupdatecontact_window.title("C.A.M.S /ADDContacts Policy Owner")
                self.deleteupdatecontact_window.geometry("370x300")
                self.deleteupdatecontact_window.config(bg='#008631')
                self.deleteupdatecontact_window.resizable(False, False)

                def contact_show():
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        global row
                        row=ROWNUMBER.get()
                        ##### EXTRACT DB FOR CONTACT DETAILS TO SHOW on UPDATE DELETE WINDOW#####
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "SELECT * FROM tbl_contact_po WHERE CONTACT_ID_PO='" +str(row)+ "'"
                        cur.execute(sql)
                        contact_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        contact_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = contact_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        a=str(items[0])
                        b=items[1]
                        c=items[2]
                        d=items[3]
                        e=items[4]
                        self.MOBILE_ENTRY.insert(0,b)
                        self.LANDLINE_ENTRY.insert(0,c)
                        self.EMAIL_ENTRY.insert(0,d)
                        self.CONTACTTYPE_ENTRY.insert(0,e)
                        self.ROW_ENTRY.config(state=DISABLED)

                        ######## END######

                def delete(): ### DELETE FUNCTION ###
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n""Failed to display ADDRESS ")
                    else:
                        self.ROW_ENTRY.config(state=NORMAL)
                        messagebox.showwarning("","You are about to delete this contact?")
                        if messagebox.askokcancel("","Proceed to Delete?"):
                            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                            cur = con.cursor()
                            sql1 = "Delete from tbl_contact_po WHERE CONTACT_ID_PO=%s"
                            val1=(row,)
                            cur.execute(sql1,val1)
                            con.commit()
                            messagebox.showinfo("", "Contact Deleted!")
                            ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                            self.ROW_ENTRY.delete(0,END)
                            self.MOBILE_ENTRY.delete(0, END)
                            self.LANDLINE_ENTRY.delete(0, END)
                            self.EMAIL_ENTRY.delete(0, END)
                            self.CONTACTTYPE_ENTRY.delete(0,END)
                            self.ROW_ENTRY.config(state=DISABLED)
                            showcontact_po()
                        else:
                            pass

                def updatecontact():
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        self.ROW_ENTRY.config(state=NORMAL)
                        mobile_contact_po = MOBILEVAR_PO.get()
                        landline_contact_po = LANDLINEVAR_PO.get()
                        email_contact_po = EMAILVAR_PO.get()
                        cont_type_contact_po = CONTACTTYPE_PO.get()
                        # if mobile_contact_po=="" or landline_contact_po=="" or email_contact_po=="" or cont_type_contact_po =="":
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()

                        sql2="UPDATE tbl_contact_po SET MOBILE =%s, LANDLINE =%s,EMAIL =%s, CONTACT_TYPE =%s WHERE CONTACT_ID_PO = %s"
                        val2=(mobile_contact_po,landline_contact_po,email_contact_po,cont_type_contact_po,row)
                        cur.execute(sql2,val2)
                        con.commit()
                        messagebox.showinfo("", "Contact Updated!")


                        ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                        self.ROW_ENTRY.delete(0, END)
                        self.MOBILE_ENTRY.delete(0, END)
                        self.LANDLINE_ENTRY.delete(0, END)
                        self.EMAIL_ENTRY.delete(0, END)
                        self.CONTACTTYPE_ENTRY.delete(0, END)
                        self.ROW_ENTRY.config(state=DISABLED)

                def cancel():
                    self.deleteupdatecontact_window.destroy()

                ### TEXT VARIABLES###
                ROWNUMBER=StringVar()
                MOBILEVAR_PO = StringVar()
                LANDLINEVAR_PO = StringVar()
                EMAILVAR_PO = StringVar()
                CONTACTTYPE_PO = StringVar()

                self.ROW_LABEL = Label(self.deleteupdatecontact_window, text="Row No: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ROW_LABEL.place(x=40, y=45)
                self.ROW_ENTRY = Entry(self.deleteupdatecontact_window, width=10, textvariable=ROWNUMBER)
                self.ROW_ENTRY.place(x=120, y=45)

                self.MOBILE_LABEL = Label(self.deleteupdatecontact_window, text="Mobile: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.MOBILE_LABEL.place(x=50, y=75)
                self.MOBILE_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=MOBILEVAR_PO)
                self.MOBILE_ENTRY.place(x=120, y=75)

                self.LANDLINE_LABEL = Label(self.deleteupdatecontact_window, text="Landline: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.LANDLINE_LABEL.place(x=40, y=100)
                self.LANDLINE_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=LANDLINEVAR_PO)
                self.LANDLINE_ENTRY.place(x=120, y=100)

                self.EMAIL_LABEL = Label(self.deleteupdatecontact_window, text="Email: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.EMAIL_LABEL.place(x=50, y=125)
                self.EMAIL_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=EMAILVAR_PO)
                self.EMAIL_ENTRY.place(x=120, y=125)

                self.CONTACTTYPE_LABEL = Label(self.deleteupdatecontact_window, text="Type: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CONTACTTYPE_LABEL.place(x=50, y=150)
                self.CONTACTTYPE_ENTRY = Entry(self.deleteupdatecontact_window, width=25,textvariable=CONTACTTYPE_PO)
                self.CONTACTTYPE_ENTRY.place(x=120, y=150)

                self.Select_button = Button(self.deleteupdatecontact_window, text="Select", padx=6,bg="#52c5f2", font=("Arial", 8, "bold"), fg="white", border=0,activebackground="#0782b3", command=contact_show)
                self.Select_button.place(x=195, y=42)

                self.Proceed_button = Button(self.deleteupdatecontact_window, text="Update", padx=8, pady=2,bg="#28b090", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=updatecontact)
                self.Proceed_button.place(x=75, y=190)

                self.Proceed_button = Button(self.deleteupdatecontact_window, text="Delete", padx=8, pady=2,bg="#ed2f2f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=delete)
                self.Proceed_button.place(x=150, y=190)

                self.Cancel_button = Button(self.deleteupdatecontact_window, text="Cancel", padx=10, pady=2,bg="#edc42f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=220, y=190)



            ##### TREE VIEW GENERATOR ####
            self.contactframe=Frame(self.contact_window,width=530,height=350)
            self.contactframe.place(x=15,y=5)
            self.trvcontact = ttk.Treeview(self.contactframe, columns=[1, 2, 3, 4, 5,6], show="headings", height="5")
            self.trvcontact.grid(row=0, column=0,sticky='n')

            # width of columns and alignment
            self.trvcontact.column("1", width=80, anchor='c')
            self.trvcontact.column("2", width=50, anchor='c')
            self.trvcontact.column("3", width=120, anchor='c')
            self.trvcontact.column("4", width=120, anchor='c')
            self.trvcontact.column("5", width=150, anchor='c')
            self.trvcontact.column("6", width=80, anchor='c')

            # Headings
            # respective columns
            self.trvcontact.heading("1", text="ROW NO.")
            self.trvcontact.heading("2", text="ID")
            self.trvcontact.heading("3", text="MOBILE")
            self.trvcontact.heading("4", text="LANDLINE")
            self.trvcontact.heading("5", text="EMAIL")
            self.trvcontact.heading("6", text="TYPE")

            self.Add_button=Button(self.contact_window,text="ADD",padx=61,pady=2, bg="#4cafed",font=("Arial",10,"bold"), fg="white", border=0, activebackground="#7fc4f0",command=add)
            self.Add_button.place(x=630,y=10)
            self.Delete_button = Button(self.contact_window, text="DELETE/UPDATE", padx=23, pady=2, bg="#e65d45",font=("Arial",10,"bold"), fg="white", border=0, activebackground='#941f0a', command=delete)
            self.Delete_button.place(x=630, y=40)
            showcontact_po()
            ###########################################END OF CONTACTS POLICY OWNER###############################################################

        ################## CONTACT AND ADDRESS INSURED ######################################################

        ############## START ADDRESS #################
        def address_function_ins():
            self.address_window = Toplevel()
            self.address_window.title("C.A.M.S /ADDRESS INSURED")
            self.address_window.geometry("790x200")
            self.address_window.config(bg='#008631')
            self.address_window.resizable(False, False)

            def showaddress_ins():
                getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                if getpolicy == "" or getpolicy == "0":
                    messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                             "Failed to display ADDRESS ")
                else:
                    self.trvaddress.delete(*self.trvaddress.get_children())
                    con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                    cur = con.cursor()
                    ### Query to extract contact of policy owner to contacts ####
                    sql = "SELECT POLICY_NUM,INS_ID,ADDRESS_ID,address,city,province,zipcode,country,type FROM tbl_policy INNER JOIN tbl_insured ON POLICY_ID=INS_ID INNER JOIN tbladdress_ins ON INS_ID=INS_ADDRESS_ID WHERE POLICY_NUM='" + getpolicy + "'"
                    cur.execute(sql)
                    address = cur.fetchall()
                    addressid = 1
                    for x in address:  ## TREE VIEW INSERT VALUES###
                        self.trvaddress.insert("", 'end', id=x[2], text=x[0],values=(x[2], addressid, x[3], x[4], x[5], x[6], x[7], x[8]))
                        addressid = addressid + 1

            def add_address():
                self.add_address_window = Toplevel()
                self.add_address_window.title("C.A.M.S /ADD ADDRESS INSURED")
                self.add_address_window.geometry("400x300")
                self.add_address_window.config(bg='#008631')
                self.add_address_window.resizable(False, False)

                def inputaddress_ins():
                    getpolicy = show_po_ins_details()
                    getaddress_ins = self.ADDRESS_INS_ENTRY.get(1.0, END)
                    getcity_ins = CITYVAR_INS.get()
                    getprovince_ins = PROVINCEVAR_INS.get()
                    getzipcode_ins = ZIPCODEVAR_INS.get()
                    getcountry_ins = COUNTRYVAR_INS.get()
                    getaddress_type_ins = ADDRESSTYPE_INS.get()
                    try:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "Select POLICY_ID,INS_ID,address,city,province,zipcode,country,type FROM tbl_policy INNER JOIN tbl_insured on POLICY_ID=INS_ID INNER JOIN tbladdress_ins ON INS_ID=INS_ADDRESS_ID WHERE POLICY_NUM='" + getpolicy + "'"
                        cur.execute(sql)
                        address_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        address_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = address_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        addressindex = items[0]

                        sql = "INSERT INTO tbladdress_ins(address,city,province,zipcode,country,type,INS_ADDRESS_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        val1 = (getaddress_ins, getcity_ins, getprovince_ins, getzipcode_ins, getcountry_ins,getaddress_type_ins, addressindex)
                        cur.execute(sql, val1)
                        messagebox.showinfo("", "Insured Address added successfully")
                        con.commit()
                        con.close()

                        self.ADDRESS_INS_ENTRY.delete(1.0, END)
                        self.CITY_INS_ENTRY.delete(0, END)
                        self.PROVINCE_INS_ENTRY.delete(0, END)
                        self.ZIPCODE_INS_ENTRY.delete(0, END)
                        self.COUNTRY_INS_ENTRY.delete(0, END)
                        self.addresstype_combobox.set(value="")
                        showaddress_ins()
                    except:
                        messagebox.showerror("", "Unable to Process request")
                def cancel():
                    self.add_address_window.destroy()

                #####ADD FUNCTION VARIABLES#####

                address_type = ['Primary', 'Alternate']
                CITYVAR_INS = StringVar()
                PROVINCEVAR_INS = StringVar()
                ZIPCODEVAR_INS = StringVar()
                COUNTRYVAR_INS = StringVar()
                ADDRESSTYPE_INS = StringVar()

                self.ADDRESS_INS_LABEL = Label(self.add_address_window, text="ADDRESS: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESS_INS_LABEL.place(x=35, y=20)
                self.ADDRESS_INS_ENTRY = Text(self.add_address_window, width=30, height=2)
                self.ADDRESS_INS_ENTRY.place(x=150, y=20)

                self.CITY_INS_LABEL = Label(self.add_address_window, text="CITY: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CITY_INS_LABEL.place(x=50, y=80)
                self.CITY_INS_ENTRY = Entry(self.add_address_window, width=25, textvariable=CITYVAR_INS)
                self.CITY_INS_ENTRY.place(x=150, y=80)

                self.PROVINCE_INS_LABEL = Label(self.add_address_window, text="PROVINCE: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.PROVINCE_INS_LABEL.place(x=30, y=105)
                self.PROVINCE_INS_ENTRY = Entry(self.add_address_window, width=25, textvariable=PROVINCEVAR_INS)
                self.PROVINCE_INS_ENTRY.place(x=150, y=105)

                self.ZIPCODE_INS_LABEL = Label(self.add_address_window, text="ZIPCODE: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ZIPCODE_INS_LABEL.place(x=30, y=130)
                self.ZIPCODE_INS_ENTRY = Entry(self.add_address_window, width=25, textvariable=ZIPCODEVAR_INS)
                self.ZIPCODE_INS_ENTRY.place(x=150, y=130)

                self.COUNTRY_INS_LABEL = Label(self.add_address_window, text="COUNTRY CODE: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.COUNTRY_INS_LABEL.place(x=15, y=155)
                self.COUNTRY_INS_ENTRY = Entry(self.add_address_window, width=25, textvariable=COUNTRYVAR_INS)
                self.COUNTRY_INS_ENTRY.place(x=150, y=155)

                self.ADDRESSTYPE_INS_LABEL = Label(self.add_address_window, text="Type: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESSTYPE_INS_LABEL.place(x=50, y=180)
                self.addresstype_combobox = ttk.Combobox(self.add_address_window, width=10, values=address_type, textvariable=ADDRESSTYPE_INS)
                self.addresstype_combobox.place(x=150, y=180)

                self.Proceed_button = Button(self.add_address_window, text="Proceed", padx=8, pady=2, bg="#149c29",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#43c92e", command=inputaddress_ins)
                self.Proceed_button.place(x=110, y=220)
                self.Cancel_button = Button(self.add_address_window, text="Cancel", padx=10, pady=2, bg="#d9ae14",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=190, y=220)
                ############################### END IF ADD ADDRESS####

            ##### DELETE / UPDATE ADDRESS POLICY OWNER #####
            def deleteupdate():
                self.deleteupdateaddress_window = Toplevel()
                self.deleteupdateaddress_window.title("C.A.M.S /UPDATE/DELETE Address INSURED")
                self.deleteupdateaddress_window.geometry("400x300")
                self.deleteupdateaddress_window.config(bg='#008631')
                self.deleteupdateaddress_window.resizable(False, False)

                def address_ins_show():
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        global row_ins
                        row_ins = ROWNUMBER_VAR_INS.get()
                        ##### EXTRACT DB FOR CONTACT DETAILS TO SHOW on UPDATE DELETE WINDOW#####
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "SELECT * FROM tbladdress_ins WHERE  ADDRESS_ID='" + str(row_ins) + "'"
                        cur.execute(sql)
                        address_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        address_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = address_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        a = str(items[0])
                        b = items[1]
                        c = items[2]
                        d = items[3]
                        e = items[4]
                        f = items[5]
                        g = items[6]

                        self.ADDRESS_ENTRY_INS.insert(1.0, b)
                        self.CITY_ENTRY_INS.insert(0, c)
                        self.PROVINCE_ENTRY_INS.insert(0, d)
                        self.ZIPCODE_ENTRY_INS.insert(0, e)
                        self.COUNTRY_ENTRY_INS.insert(0, f)
                        self.ADDRESSTYPE_ENTRY_INS.insert(0, g)
                        self.ROW_ENTRY_INS.config(state=DISABLED)

                def delete():  ### DELETE FUNCTION ###
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        self.ROW_ENTRY_INS.config(state=NORMAL)
                        messagebox.showwarning("", "You are about to delete this contact?")
                        if messagebox.askokcancel("", "Proceed to Delete?"):
                            con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                            cur = con.cursor()
                            sql1 = "Delete from tbladdress_ins WHERE ADDRESS_ID=%s"
                            val1 = (row_ins,)
                            cur.execute(sql1, val1)
                            con.commit()
                            messagebox.showinfo("", "Address Deleted!")
                            ### DELETE ENTRY DATA AFTER DELETE TO TABLE###

                            self.ADDRESS_ENTRY_INS.delete(1.0, END)
                            self.CITY_ENTRY_INS.delete(0, END)
                            self.PROVINCE_ENTRY_INS.delete(0, END)
                            self.ZIPCODE_ENTRY_INS.delete(0, END)
                            self.COUNTRY_ENTRY_INS.delete(0, END)
                            self.addresstype_combobox.set(value="")
                            showaddress_ins()
                        else:
                            pass

                def updateaddress():
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        address_ins = self.ADDRESS_ENTRY_INS.get(1.0, END)
                        city = CITYVAR_INS.get()
                        province = PROVINCEVAR_INS.get()
                        zipcode = ZIPCODEVAR_INS.get()
                        country = COUNTRYVAR_INS.get()
                        add_type = ADDRESSTYPEVAR_INS.get()

                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbladdress_ins SET address =%s, city =%s,province =%s, zipcode =%s , country=%s , type=%s WHERE ADDRESS_ID= %s"
                        val2 = (address_ins, city, province, zipcode, country, add_type, row_ins)
                        cur.execute(sql2, val2)
                        con.commit()
                        messagebox.showinfo("", "Insured Address Updated!")

                        ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                        self.ADDRESS_ENTRY_INS.delete(1.0, END)
                        self.CITY_ENTRY_INS.delete(0, END)
                        self.PROVINCE_ENTRY_INS.delete(0, END)
                        self.ZIPCODE_ENTRY_INS.delete(0, END)
                        self.COUNTRY_ENTRY_INS.delete(0, END)
                        self.addresstype_combobox.set(value="")
                        showaddress_ins()

                def cancel():
                    self.deleteupdateaddress_window.destroy()

                ### UPDATE/DELETE VARIABLES###
                address_type = ['Primary', 'Alternate']
                ROWNUMBER_VAR_INS = StringVar()
                CITYVAR_INS = StringVar()
                PROVINCEVAR_INS = StringVar()
                ZIPCODEVAR_INS = StringVar()
                COUNTRYVAR_INS = StringVar()
                ADDRESSTYPEVAR_INS = StringVar()

                self.ROW_LABEL_INS = Label(self.deleteupdateaddress_window, text="Row No: ", bg='#008631', border=0,fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ROW_LABEL_INS.place(x=40, y=20)
                self.ROW_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=10, textvariable=ROWNUMBER_VAR_INS)
                self.ROW_ENTRY_INS.place(x=120, y=20)

                self.ADDRESS_LABEL_INS = Label(self.deleteupdateaddress_window, text="Address: ", bg='#008631',border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESS_LABEL_INS.place(x=40, y=45)
                self.ADDRESS_ENTRY_INS = Text(self.deleteupdateaddress_window, width=30, height=2)
                self.ADDRESS_ENTRY_INS.place(x=120, y=45)

                self.CITY_LABEL_INS = Label(self.deleteupdateaddress_window, text="City: ", bg='#008631', border=0,fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CITY_LABEL_INS.place(x=55, y=105)
                self.CITY_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=25, textvariable=CITYVAR_INS)
                self.CITY_ENTRY_INS.place(x=120, y=105)

                self.PROVINCE_LABEL_INS = Label(self.deleteupdateaddress_window, text="Province: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.PROVINCE_LABEL_INS.place(x=50, y=130)
                self.PROVINCE_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=25, textvariable=PROVINCEVAR_INS)
                self.PROVINCE_ENTRY_INS.place(x=120, y=130)

                self.ZIPCODE_LABEL_INS = Label(self.deleteupdateaddress_window, text="Zipcode: ", bg='#008631',border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ZIPCODE_LABEL_INS.place(x=50, y=155)
                self.ZIPCODE_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=25, textvariable=ZIPCODEVAR_INS)
                self.ZIPCODE_ENTRY_INS.place(x=120, y=155)

                self.COUNTRY_LABEL_INS = Label(self.deleteupdateaddress_window, text="Country: ", bg='#008631',border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.COUNTRY_LABEL_INS.place(x=50, y=180)
                self.COUNTRY_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=25, textvariable=COUNTRYVAR_INS)
                self.COUNTRY_ENTRY_INS.place(x=120, y=180)

                self.ADDRESSTYPE_LABEL_INS = Label(self.deleteupdateaddress_window, text="Type: ", bg='#008631',border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ADDRESSTYPE_LABEL_INS.place(x=50, y=205)
                self.ADDRESSTYPE_ENTRY_INS = Entry(self.deleteupdateaddress_window, width=13,textvariable=ADDRESSTYPEVAR_INS)
                self.ADDRESSTYPE_ENTRY_INS.place(x=120, y=205)
                self.addresstype_combobox = ttk.Combobox(self.deleteupdateaddress_window, width=10, values=address_type,textvariable=ADDRESSTYPEVAR_INS)
                self.addresstype_combobox.place(x=210, y=204)

                self.Select_button = Button(self.deleteupdateaddress_window, text="Select", padx=6, bg="#52c5f2",font=("Arial", 8, "bold"), fg="white", border=0, activebackground="#0782b3",command=address_ins_show)
                self.Select_button.place(x=195, y=18)
                self.Proceed_button = Button(self.deleteupdateaddress_window, text="Update", padx=8, pady=2,bg="#28b090",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0",command=updateaddress)
                self.Proceed_button.place(x=75, y=240)
                self.Proceed_button = Button(self.deleteupdateaddress_window, text="Delete", padx=8, pady=2,bg="#ed2f2f",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0",command=delete)
                self.Proceed_button.place(x=150, y=240)
                self.Cancel_button = Button(self.deleteupdateaddress_window, text="Cancel", padx=10, pady=2,bg="#edc42f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=220, y=240)

            ##### TREE VIEW GENERATOR for ADDRESS OF POLICY OWNER ####
            self.Addressframe = Frame(self.address_window, width=530, height=350)
            self.Addressframe.place(x=15, y=5)
            self.trvaddress = ttk.Treeview(self.Addressframe, columns=[1, 2, 3, 4, 5, 6, 7, 8], show="headings",height="5")
            self.trvaddress.grid(row=0, column=0, sticky='n')

            # width of columns and alignment
            self.trvaddress.column("1", width=70, anchor='c')
            self.trvaddress.column("2", width=50, anchor='c')
            self.trvaddress.column("3", width=200, anchor='c')
            self.trvaddress.column("4", width=100, anchor='c')
            self.trvaddress.column("5", width=100, anchor='c')
            self.trvaddress.column("6", width=80, anchor='c')
            self.trvaddress.column("7", width=80, anchor='c')
            self.trvaddress.column("8", width=80, anchor='c')
            # Headings
            # respective columns
            self.trvaddress.heading("1", text="ROW NO")  ### WILL BE THE ADDRESS ID FROM TB
            self.trvaddress.heading("2",text="ID")  ### GENERATE AND WILL BE AUTO INCREMENT BY 1 ONCE DISPLAYED IN TREEVIEW
            self.trvaddress.heading("3", text="ADDRESS")
            self.trvaddress.heading("4", text="CITY")
            self.trvaddress.heading("5", text="PROVINCE")
            self.trvaddress.heading("6", text="ZIPCODE")
            self.trvaddress.heading("7", text="COUNTRY")
            self.trvaddress.heading("8", text="TYPE")

            self.Add_button = Button(self.address_window, text="ADD", padx=50, pady=2, bg="#4cafed",font=("Arial", 10, "bold"), fg="white", border=0, activebackground="#7fc4f0",command=add_address)
            self.Add_button.place(x=30, y=140)
            self.Delete_button = Button(self.address_window, text="DELETE/UPDATE", padx=20, pady=2, bg="#e65d45",font=("Arial", 10, "bold"), fg="white", border=0, activebackground='#941f0a',command=deleteupdate)
            self.Delete_button.place(x=180, y=140)
            showaddress_ins()

            ######################### END OF ADDRESS#################################################

        ############ START  CONTACTS #############################################################
        def contacts_fuction_ins():
            ######OPEN CONTACTS WINDOW W/C CHILD WINDOW ON THE TOP OF MAINWINDOW (IF MAIN WINDOW(PARENT) IS CLOSE, CONTACT WINDOW (CHILD) WILL ALSO BE CLOSE ) #####
            self.contact_window = Toplevel()
            self.contact_window.title("C.A.M.S /Contacts Insured")
            self.contact_window.geometry("790x170")
            self.contact_window.config(bg='#008631')
            self.contact_window.resizable(False, False)

            def showcontact_ins():
                getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                if getpolicy == "" or getpolicy == "0":
                    messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                             "Failed to display ADDRESS ")
                else:
                    self.trvcontact.delete(*self.trvcontact.get_children())
                    con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                    cur = con.cursor()
                    ### Query to extract contact of policy owner to contacts ####
                    sql = "SELECT POLICY_NUM,INS_ID,CONTACT_ID_INS,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE FROM tbl_policy INNER JOIN tbl_insured ON POLICY_ID=INS_ID INNER JOIN tbl_contact_ins ON INS_ID=CONTACT_FK_INS WHERE POLICY_NUM='" + getpolicy + "'"
                    cur.execute(sql)
                    contacts = cur.fetchall()
                    contactid = 1
                    for x in contacts:  ## TREE VIEW INSERT VALUES###
                        self.trvcontact.insert("", 'end', id=x[2], text=x[0], values=(x[2], contactid, x[3], x[4], x[5], x[6]))
                        contactid = contactid + 1

            ############## ADD CONTACT ###############

            def add():  #### THIS OPENS NEW WINDOW CHILD WINDOW OF CONTACTS  (IF CONTACT WINDOW(PARENT) IS CLOSE, ADDCONTACT WINDOW (CHILD) WILL ALSO BE CLOSE )
                self.addcontact_window = Toplevel()
                self.addcontact_window.title("C.A.M.S /ADDContacts INSURED")
                self.addcontact_window.geometry("370x200")
                self.addcontact_window.config(bg='#008631')
                self.addcontact_window.resizable(False, False)

                def addcontact():
                    getpolicy = show_po_ins_details()
                    mobile = MOBILEVAR_INS.get()
                    landline = LANDLINEVAR_INS.get()
                    email = EMAILVAR_INS.get()
                    cont_type = CONTACTTYPE_INS.get()
                    try:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()

                        sql = "Select POLICY_ID,INS_ID,MOBILE,LANDLINE,EMAIL,CONTACT_TYPE FROM tbl_policy INNER JOIN tbl_insured on POLICY_ID=INS_ID INNER JOIN tbl_contact_ins ON INS_ID=CONTACT_FK_INS WHERE POLICY_NUM='" + getpolicy + "'"
                        cur.execute(sql)
                        contact_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        contact_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = contact_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        contactindex = items[0]

                        sql = "INSERT INTO tbl_contact_ins(MOBILE,LANDLINE,EMAIL,CONTACT_TYPE,CONTACT_FK_INS) VALUES (%s,%s,%s,%s,%s)"
                        val1 = (mobile, landline, email, cont_type, contactindex)
                        cur.execute(sql, val1)
                        messagebox.showinfo("", "Contact added successfully")
                        con.commit()
                        con.close()
                        self.MOBILE_ENTRY.delete(0, END)
                        self.LANDLINE_ENTRY.delete(0, END)
                        self.EMAIL_ENTRY.delete(0, END)
                        self.contacttype_combobox.set(value="")
                    except:
                        messagebox.showerror("", "Unable to Process request")

                #### CANCEL ADD CONTACT
                def cancel():
                    self.addcontact_window.destroy()

                ### TEXT VARIABLES###
                MOBILEVAR_INS = StringVar()
                LANDLINEVAR_INS = StringVar()
                EMAILVAR_INS = StringVar()
                CONTACTTYPE_INS = StringVar()
                contact_type = ['Primary', 'Alternate']

                self.MOBILE_LABEL = Label(self.addcontact_window, text="Mobile: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.MOBILE_LABEL.place(x=50, y=20)
                self.MOBILE_ENTRY = Entry(self.addcontact_window, width=25, textvariable=MOBILEVAR_INS)
                self.MOBILE_ENTRY.place(x=120, y=20)

                self.LANDLINE_LABEL = Label(self.addcontact_window, text="Landline: ", bg='#008631', border=0, fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.LANDLINE_LABEL.place(x=40, y=45)
                self.LANDLINE_ENTRY = Entry(self.addcontact_window, width=25, textvariable=LANDLINEVAR_INS)
                self.LANDLINE_ENTRY.place(x=120, y=45)

                self.EMAIL_LABEL = Label(self.addcontact_window, text="Email: ", bg='#008631', border=0, fg='white',font=('Microsoft YaHei UI Light', 11, "bold"))
                self.EMAIL_LABEL.place(x=55, y=70)
                self.EMAIL_ENTRY = Entry(self.addcontact_window, width=25, textvariable=EMAILVAR_INS)
                self.EMAIL_ENTRY.place(x=120, y=70)

                self.CONTACTTYPE_LABEL = Label(self.addcontact_window, text="Type: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CONTACTTYPE_LABEL.place(x=55, y=100)
                self.contacttype_combobox = ttk.Combobox(self.addcontact_window, width=10, values=contact_type,textvariable=CONTACTTYPE_INS)
                self.contacttype_combobox.place(x=120, y=100)

                self.Proceed_button = Button(self.addcontact_window, text="Proceed", padx=8, pady=2, bg="#149c29",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=addcontact)
                self.Proceed_button.place(x=120, y=140)
                self.Cancel_button = Button(self.addcontact_window, text="Cancel", padx=10, pady=2, bg="#d9ae14",font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=200, y=140)

            ####################################################### END ADD WINDOW #####################################################

            ################################### DELETE / UPDATE WINDOW #################################################################
            def delete():
                self.deleteupdatecontact_window = Toplevel()
                self.deleteupdatecontact_window.title("C.A.M.S /ADDContacts Policy Owner")
                self.deleteupdatecontact_window.geometry("370x300")
                self.deleteupdatecontact_window.config(bg='#008631')
                self.deleteupdatecontact_window.resizable(False, False)

                def contact_show():
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        global row_ins
                        row_ins = ROWNUMBER_INS.get()
                        ##### EXTRACT DB FOR CONTACT DETAILS TO SHOW on UPDATE DELETE WINDOW#####
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql = "SELECT * FROM tbl_contact_ins WHERE CONTACT_ID_INS='" + str(row_ins) + "'"
                        cur.execute(sql)
                        contact_indexes = cur.fetchall()  #### fetch the policy id result is in tuple format
                        contact_indexes.reverse()  ### reversed the fetch result to get the last index
                        x = contact_indexes[0]  ### variable x is not holding the last tuple index
                        items = list(x)  ### convert tuple to list to extract as normal integer
                        a = str(items[0])
                        b = items[1]
                        c = items[2]
                        d = items[3]
                        e = items[4]
                        self.MOBILE_ENTRY.insert(0, b)
                        self.LANDLINE_ENTRY.insert(0, c)
                        self.EMAIL_ENTRY.insert(0, d)
                        self.CONTACTTYPE_ENTRY.insert(0, e)
                        self.ROW_ENTRY.config(state=DISABLED)

                        ######## END######

                def delete():  ### DELETE FUNCTION ###
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        self.ROW_ENTRY.config(state=NORMAL)
                        messagebox.showwarning("", "You are about to delete this contact?")
                        if messagebox.askokcancel("", "Proceed to Delete?"):
                            con = mysql.connector.connect(host="localhost", user="root", password="",database='practicedb')
                            cur = con.cursor()
                            sql1 = "Delete from tbl_contact_ins WHERE CONTACT_ID_INS=%s"
                            val1 = (row,)
                            cur.execute(sql1, val1)
                            con.commit()
                            messagebox.showinfo("", "Insured Contact Deleted!")
                            ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                            self.ROW_ENTRY.delete(0, END)
                            self.MOBILE_ENTRY.delete(0, END)
                            self.LANDLINE_ENTRY.delete(0, END)
                            self.EMAIL_ENTRY.delete(0, END)
                            self.CONTACTTYPE_ENTRY.delete(0, END)
                            self.ROW_ENTRY.config(state=DISABLED)
                            showcontact_ins()
                        else:
                            pass

                def updatecontact():
                    getpolicy = show_po_ins_details()  #### RETRIEVE POLICY NUMBER INPUT####
                    if getpolicy == "" or getpolicy == "0":
                        messagebox.showerror("", "CANNOT FIND POLICY NUMBER \n"
                                                 "Failed to display ADDRESS ")
                    else:
                        self.ROW_ENTRY.config(state=NORMAL)
                        mobile_contact_ins = MOBILEVAR_INS.get()
                        landline_contact_ins = LANDLINEVAR_INS.get()
                        email_contact_ins = EMAILVAR_INS.get()
                        cont_type_contact_ins = CONTACTTYPE_INS.get()
                        # if mobile_contact_po=="" or landline_contact_po=="" or email_contact_po=="" or cont_type_contact_po =="":
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql2 = "UPDATE tbl_contact_ins SET MOBILE =%s, LANDLINE =%s,EMAIL =%s, CONTACT_TYPE =%s WHERE CONTACT_ID_INS = %s"
                        val2 = (mobile_contact_ins, landline_contact_ins, email_contact_ins, cont_type_contact_ins, row_ins)
                        cur.execute(sql2, val2)
                        con.commit()
                        messagebox.showinfo("", "Inured Contact Updated!")

                        ### DELETE ENTRY DATA AFTER DELETE TO TABLE###
                        self.ROW_ENTRY.delete(0, END)
                        self.MOBILE_ENTRY.delete(0, END)
                        self.LANDLINE_ENTRY.delete(0, END)
                        self.EMAIL_ENTRY.delete(0, END)
                        self.CONTACTTYPE_ENTRY.delete(0, END)
                        self.ROW_ENTRY.config(state=DISABLED)

                def cancel():
                    self.deleteupdatecontact_window.destroy()

                ### TEXT VARIABLES###
                ROWNUMBER_INS = StringVar()
                MOBILEVAR_INS = StringVar()
                LANDLINEVAR_INS = StringVar()
                EMAILVAR_INS = StringVar()
                CONTACTTYPE_INS = StringVar()

                self.ROW_LABEL = Label(self.deleteupdatecontact_window, text="Row No: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.ROW_LABEL.place(x=40, y=45)
                self.ROW_ENTRY = Entry(self.deleteupdatecontact_window, width=10, textvariable=ROWNUMBER_INS)
                self.ROW_ENTRY.place(x=120, y=45)

                self.MOBILE_LABEL = Label(self.deleteupdatecontact_window, text="Mobile: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.MOBILE_LABEL.place(x=50, y=75)
                self.MOBILE_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=MOBILEVAR_INS)
                self.MOBILE_ENTRY.place(x=120, y=75)

                self.LANDLINE_LABEL = Label(self.deleteupdatecontact_window, text="Landline: ", bg='#008631',border=0, fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.LANDLINE_LABEL.place(x=40, y=100)
                self.LANDLINE_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=LANDLINEVAR_INS)
                self.LANDLINE_ENTRY.place(x=120, y=100)

                self.EMAIL_LABEL = Label(self.deleteupdatecontact_window, text="Email: ", bg='#008631', border=0,fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.EMAIL_LABEL.place(x=50, y=125)
                self.EMAIL_ENTRY = Entry(self.deleteupdatecontact_window, width=25, textvariable=EMAILVAR_INS)
                self.EMAIL_ENTRY.place(x=120, y=125)

                self.CONTACTTYPE_LABEL = Label(self.deleteupdatecontact_window, text="Type: ", bg='#008631',border=0, fg='white', font=('Microsoft YaHei UI Light', 11, "bold"))
                self.CONTACTTYPE_LABEL.place(x=50, y=150)
                self.CONTACTTYPE_ENTRY = Entry(self.deleteupdatecontact_window, width=25,textvariable=CONTACTTYPE_INS)
                self.CONTACTTYPE_ENTRY.place(x=120, y=150)

                self.Select_button = Button(self.deleteupdatecontact_window, text="Select", padx=6, bg="#52c5f2",font=("Arial", 8, "bold"), fg="white", border=0,activebackground="#0782b3", command=contact_show)
                self.Select_button.place(x=195, y=42)

                self.Proceed_button = Button(self.deleteupdatecontact_window, text="Update", padx=8, pady=2,bg="#28b090", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=updatecontact)
                self.Proceed_button.place(x=75, y=190)

                self.Proceed_button = Button(self.deleteupdatecontact_window, text="Delete", padx=8, pady=2,bg="#ed2f2f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#7fc4f0", command=delete)
                self.Proceed_button.place(x=150, y=190)

                self.Cancel_button = Button(self.deleteupdatecontact_window, text="Cancel", padx=10, pady=2, bg="#edc42f", font=("Arial", 10, "bold"), fg="white", border=0,activebackground="#8c700a", command=cancel)
                self.Cancel_button.place(x=220, y=190)

            ##### TREE VIEW GENERATOR ####
            self.contactframe = Frame(self.contact_window, width=530, height=350)
            self.contactframe.place(x=15, y=5)
            self.trvcontact = ttk.Treeview(self.contactframe, columns=[1, 2, 3, 4, 5, 6], show="headings",height="5")
            self.trvcontact.grid(row=0, column=0, sticky='n')

            # width of columns and alignment
            self.trvcontact.column("1", width=80, anchor='c')
            self.trvcontact.column("2", width=50, anchor='c')
            self.trvcontact.column("3", width=120, anchor='c')
            self.trvcontact.column("4", width=120, anchor='c')
            self.trvcontact.column("5", width=150, anchor='c')
            self.trvcontact.column("6", width=80, anchor='c')

            # Headings
            # respective columns
            self.trvcontact.heading("1", text="ROW NO.")
            self.trvcontact.heading("2", text="ID")
            self.trvcontact.heading("3", text="MOBILE")
            self.trvcontact.heading("4", text="LANDLINE")
            self.trvcontact.heading("5", text="EMAIL")
            self.trvcontact.heading("6", text="TYPE")

            self.Add_button = Button(self.contact_window, text="ADD", padx=61, pady=2, bg="#4cafed",font=("Arial", 10, "bold"), fg="white", border=0, activebackground="#7fc4f0",command=add)
            self.Add_button.place(x=630, y=10)
            self.Delete_button = Button(self.contact_window, text="DELETE/UPDATE", padx=23, pady=2, bg="#e65d45",font=("Arial", 10, "bold"), fg="white", border=0,activebackground='#941f0a', command=delete)
            self.Delete_button.place(x=630, y=40)
            showcontact_ins()
        ###########################################END OF CONTACTS INSURED ###############################################################


        ##############CLIENT INFO /POLICY OWNER  ##################
        self.po_frame = LabelFrame(self.tab2, width=460, height=250, bg='white',text="Policy Owner")
        self.po_frame.place(x=10, y=10)

        self.FNAME_LABEL = Label(self.po_frame, text="First Name: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.FNAME_LABEL.place(x=13, y=10)
        self.FNAME_ENTRY_PO = Label(self.po_frame,width=13, text=" ", bg='#dbdbdb', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.FNAME_ENTRY_PO.place(x=130, y=10)

        self.MNAME_LABEL_PO = Label(self.po_frame, text="Middle Name: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MNAME_LABEL_PO.place(x=13, y=40)
        self.MNAME_ENTRY_PO = Label(self.po_frame,width=13, text=" ", bg='#dbdbdb', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MNAME_ENTRY_PO.place(x=130, y=40)

        self.LNAME_LABEL_PO = Label(self.po_frame, text="Last Name: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LNAME_LABEL_PO.place(x=13, y=70)
        self.LNAME_ENTRY_PO = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LNAME_ENTRY_PO.place(x=130, y=70)

        self.AGE_LABEL_PO = Label(self.po_frame, text="Age: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.AGE_LABEL_PO.place(x=280, y=10)
        self.AGE_ENTRY_PO = Label(self.po_frame, width=10, text=" ", bg='#dbdbdb', border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.AGE_ENTRY_PO.place(x=320, y=10)

        self.DOB_LABEL_PO = Label(self.po_frame, text="DOB: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.DOB_LABEL_PO.place(x=280, y=40)
        self.DOB_ENTRY_PO = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.DOB_ENTRY_PO.place(x=320, y=40)

        self.GENDER_LABEL_PO = Label(self.po_frame, text="Sex: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.GENDER_LABEL_PO.place(x=280, y=70)
        self.GENDER_ENTRY_PO = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.GENDER_ENTRY_PO.place(x=320, y=70)

        self.CSTATUS_LABEL_PO = Label(self.po_frame, text="Civil Status: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.CSTATUS_LABEL_PO.place(x=30, y=100)
        self.CSTATUS_ENTRY_PO = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.CSTATUS_ENTRY_PO.place(x=20, y=130)

        self.PROFESSION_LABEL_PO = Label(self.po_frame, text="Profession: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PROFESSION_LABEL_PO.place(x=170, y=100)
        self.PROFESSION_ENTRY_PO = Label(self.po_frame, width=18, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PROFESSION_ENTRY_PO.place(x=170, y=130)

        self.ADDRESS_BUTTON = Button(self.po_frame, text="Address", padx=17, bg="#d9ae14", compound="left", font=("Arial", 10), fg="white",border=0, activebackground="#8c700a", command=address_fuction_po)
        self.ADDRESS_BUTTON.place(x=50, y=160)

        self.CONTACTS_BUTTON = Button(self.po_frame, text="Contacts", padx=17, bg="#4cafed", compound="left",font=("Arial",10), fg="white", border=0, activebackground="#7fc4f0", command=contacts_fuction_po)
        self.CONTACTS_BUTTON.place(x=170, y=160)



        ##############CLIENT INFO /INSURED  ##################
        self.po_frame = LabelFrame(self.tab2, width=5, height=260, bg='white')
        self.po_frame.place(x=505, y=0)
        self.po_frame = LabelFrame(self.tab2, width=5, height=260, bg='white')
        self.po_frame.place(x=510, y=0)

        self.po_frame = LabelFrame(self.tab2, width=460, height=250, bg='white',text="Insured")
        self.po_frame.place(x=550, y=10)

        self.FNAME_LABEL_INS = Label(self.po_frame, text="First Name: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.FNAME_LABEL_INS.place(x=13, y=10)
        self.FNAME_ENTRY_INS = Label(self.po_frame,width=13, text=" ", bg='#dbdbdb', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.FNAME_ENTRY_INS.place(x=130, y=10)

        self.MNAME_LABEL_INS = Label(self.po_frame, text="Middle Name: ", bg='white', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MNAME_LABEL_INS.place(x=13, y=40)
        self.MNAME_ENTRY_INS = Label(self.po_frame,width=13, text=" ", bg='#dbdbdb', border=0,fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MNAME_ENTRY_INS.place(x=130, y=40)

        self.LNAME_LABEL_INS = Label(self.po_frame, text="Last Name: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LNAME_LABEL_INS.place(x=13, y=70)
        self.LNAME_ENTRY_INS = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LNAME_ENTRY_INS.place(x=130, y=70)

        self.AGE_LABEL_INS = Label(self.po_frame, text="Age: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.AGE_LABEL_INS.place(x=280, y=10)
        self.AGE_ENTRY_INS = Label(self.po_frame, width=10, text=" ", bg='#dbdbdb', border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.AGE_ENTRY_INS.place(x=320, y=10)

        self.DOB_LABEL_INS = Label(self.po_frame, text="DOB: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.DOB_LABEL_INS.place(x=280, y=40)
        self.DOB_ENTRY_INS = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.DOB_ENTRY_INS.place(x=320, y=40)

        self.GENDER_LABEL_INS = Label(self.po_frame, text="Sex: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.GENDER_LABEL_INS.place(x=280, y=70)
        self.GENDER_ENTRY_INS = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.GENDER_ENTRY_INS.place(x=320, y=70)


        self.CSTATUS_LABEL_INS = Label(self.po_frame, text="Civil Status: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.CSTATUS_LABEL_INS.place(x=30, y=100)
        self.CSTATUS_ENTRY_INS = Label(self.po_frame, width=13, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.CSTATUS_ENTRY_INS.place(x=20, y=130)

        self.PROFESSION_LABEL_INS = Label(self.po_frame, text="Profession: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PROFESSION_LABEL_INS.place(x=170, y=100)
        self.PROFESSION_ENTRY_INS = Label(self.po_frame, width=18, text=" ", bg='#dbdbdb', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PROFESSION_ENTRY_INS.place(x=170, y=130)

        self.ADDRESS_BUTTON = Button(self.po_frame, text="Address", padx=17, bg="#d9ae14",font=("Arial",10), fg="white", border=0, activebackground="#8c700a", command=address_function_ins)
        self.ADDRESS_BUTTON.place(x=50, y=160)
        self.CONTACTS_BUTTON = Button(self.po_frame, text="Contacts", padx=17, bg="#4cafed",font=("Arial",10), fg="white", border=0, activebackground="#7fc4f0", command=contacts_fuction_ins)
        self.CONTACTS_BUTTON.place(x=170, y=160)

        # ##################################################### END OF TAB 2 CLIENT INFORMATION ########################################################################


        #################################################### START TAB 3 BENEFICIARY INFORMATION ####################################################################

        self.treeviewbeneframe = LabelFrame(self.tab3, width=1000, height=130, bg='white')
        self.treeviewbeneframe.place(x=10, y=10)
        self.benedetailsframe=Label(self.tab3, width=900, height=160, bg='white')
        self.benedetailsframe.place(x=10, y=100)

        def show_bene():#### FUCNTION TO INSERT ITEMS IN TREEVIEW##
            con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
            cur = con.cursor()
            ### QUERY FOR FETCH POLICY##
            sql = "select POLICY_ID,POLICY_NUM,BENE_ID,firstname,middlename,lastname,age,birthday,gender,relationship,benefit_percentage from tbl_policy INNER JOIN tbl_bene on POLICY_ID=BENE_POLICY_ID where POLICY_NUM='" + str(getpolicy) + "'"
            cur.execute(sql)
            benelist = cur.fetchall()
            for x in benelist:
                self.trvbene.insert("", 'end', id=x[2], text=x[0],values=(x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10]))

        def clearbene():
            try:
                self.FNAME_ENTRY_BENE_OUTPUT.delete(0,END)
                self.MNAME_ENTRY_BENE_OUTPUT.delete(0,END)
                self.LNAME_ENTRY_BENE_OUTPUT.delete(0,END)
                self.AGE_ENTRY_BENE_OUTPUT.delete(0,END)
                self.calbenedob.delete(0,END)
                self.GENDER_ENTRY_BENE_OUTPUT.delete(0,END)
                self.RELATIONSHIP_ENTRY_BENE_OUTPUT.delete(0,END)
                self.PERCENT_LABELOUTPUT_BENE.config(text="")
                self.MOBILE_ENTRY_BENE_OUTPUT.delete(0,END)
                self.LANDLINE_ENTRY_BENE_OUTPUT.delete(0,END)
                self.EMAIL_ENTRY_BENE_OUTPUT.delete(0,END)
                self.ADDRESS_ENTRY_BENE_OUTPUT.delete(0,END)
                self.CITY_ENTRY_BENE_OUTPUT.delete(0,END)
                self.PROVINCE_ENTRY_BENE_OUTPUT.delete(0,END)
                self.ZIPCODE_ENTRY_BENE_OUTPUT.delete(0,END)
                self.COUNTRY_ENTRY_BENE_OUTPUT.delete(0,END)
            except:
                pass


        def clicktreeviewbene(event):
            try:
                #### TO DISPLAY CONTACT AND ADDRESS I WILL USE THIS BIND FUNCTION TO EXECUTE SELECT QUERY TO tbl_policy join tbladdress_bene and tbl_contact_bene
                selectrow = self.trvbene.item(self.trvbene.selection())
                #### get valus in TRV selected row display as dictionary######
                items = selectrow.get('values')
                global bene_rownum,bene_mobile,bene_landline,bene_email,bene_address,bene_city,bene_province,bene_zipcode,bene_country
                bene_rownum=str(items[0]) ### This is to extract row number of the selected beneficiary in the treeview to be use on the query to get the selected beneficiaries contact and address
                con = mysql.connector.connect(host="localhost", user="root", password="", database="practicedb")
                cur = con.cursor()
                ### QUERY FOR FETCH POLICY##
                sql = "SELECT MOBILE,LANDLINE,EMAIL,address,city,province,zipcode,country from tbl_contact_bene INNER JOIN tbladdress_bene on CONTACT_ID_BENE=ADDRESS_ID where ADDRESS_ID ='"+bene_rownum+"'"
                cur.execute(sql)
                benecontactandaddress = cur.fetchall() ##### EXTRACT CONTACTS AND ADDRESS FROM DB AND ASSIGN TO VARIABLE FOR DISPLAY

                bene_mobile=benecontactandaddress[0][0]
                bene_landline=benecontactandaddress[0][1]
                bene_email=benecontactandaddress[0][2]
                bene_address=benecontactandaddress[0][3]
                bene_city=benecontactandaddress[0][4]
                bene_province=benecontactandaddress[0][5]
                bene_zipcode=benecontactandaddress[0][6]
                bene_country=benecontactandaddress[0][7]

                sql1 = "SELECT * from tbl_bene inner join tbl_policy on POLICY_ID=BENE_POLICY_ID where BENE_ID='" + bene_rownum + "'"
                cur.execute(sql1)
                beneinfo=cur.fetchall()
                global bene_fname,bene_mname,bene_lname,bene_age,bene_bday,bene_gender,bene_relation,bene_percent
                bene_fname=beneinfo[0][1]
                bene_mname=beneinfo[0][2]
                bene_lname=beneinfo[0][3]
                bene_age=beneinfo[0][4]
                bene_bday=beneinfo[0][5]
                bene_gender=beneinfo[0][6]
                bene_relation=beneinfo[0][7]
                bene_percent=beneinfo[0][8]
                bene_enablefunction()
                insert_data_bene()
            except:
                messagebox.showerror("","No details to display")
        def insert_data_bene():
            try:
                clearbene()
                self.FNAME_ENTRY_BENE_OUTPUT.insert(0,bene_fname)
                self.MNAME_ENTRY_BENE_OUTPUT.insert(0,bene_mname)
                self.LNAME_ENTRY_BENE_OUTPUT.insert(0,bene_lname)
                self.AGE_ENTRY_BENE_OUTPUT.insert(0,bene_age)
                self.calbenedob.insert(0,bene_bday)
                self.GENDER_ENTRY_BENE_OUTPUT.insert(0,bene_gender)
                self.RELATIONSHIP_ENTRY_BENE_OUTPUT.insert(0,bene_relation)
                self.PERCENT_LABELOUTPUT_BENE.config(text=bene_percent)
                self.MOBILE_ENTRY_BENE_OUTPUT.insert(0, bene_mobile)
                self.LANDLINE_ENTRY_BENE_OUTPUT.insert(0, bene_landline)
                self.EMAIL_ENTRY_BENE_OUTPUT.insert(0, bene_email)
                self.ADDRESS_ENTRY_BENE_OUTPUT.insert(0, bene_address)
                self.CITY_ENTRY_BENE_OUTPUT.insert(0, bene_city)
                self.PROVINCE_ENTRY_BENE_OUTPUT.insert(0, bene_province)
                self.ZIPCODE_ENTRY_BENE_OUTPUT.insert(0, bene_zipcode)
                self.COUNTRY_ENTRY_BENE_OUTPUT.insert(0, bene_country)

                self.FNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.MNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.LNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.AGE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.calbenedob.config(state=DISABLED)
                self.GENDER_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.RELATIONSHIP_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.PERCENT_LABELOUTPUT_BENE.config(state=DISABLED)
                self.MOBILE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.LANDLINE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.EMAIL_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.ADDRESS_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.CITY_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.PROVINCE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.ZIPCODE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                self.COUNTRY_ENTRY_BENE_OUTPUT.config(state=DISABLED)
            except:
                messagebox.showerror("No Input/selected Policy", "Unable to display details! ")

        def bene_enablefunction():
            try:
                self.FNAME_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.MNAME_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.LNAME_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.AGE_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.calbenedob.config(state=NORMAL)
                self.GENDER_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.RELATIONSHIP_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.MOBILE_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.LANDLINE_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.EMAIL_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.ADDRESS_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.CITY_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.PROVINCE_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.ZIPCODE_ENTRY_BENE_OUTPUT.config(state=NORMAL)
                self.COUNTRY_ENTRY_BENE_OUTPUT.config(state=NORMAL)
            except:
                messagebox.showerror("No Input/selected Policy", "Unable to display details! ")

        def bene_update_contactaddress():
            try:
                if messagebox.askyesno("","Proceed on update?"):
                    get_fname=FNAME_BENEVAR.get()
                    get_mname=MNAME_BENEVAR.get()
                    get_lname=LNAME_BENEVAR.get()
                    get_age=AGE_BENEVAR.get()
                    get_dob=BDAY_BENEVAR.get()
                    get_gender=GENDER_BENEVAR.get()
                    get_relation=RELATIONSHIP_BENEVAR.get()
                    get_benemobile=MOBILE_BENEVAR.get()
                    get_benelandline=LANDLINE_BENEVAR.get()
                    get_beneemail=EMAIL_BENEVAR.get()
                    get_beneaddress=ADDRESS_BENEVAR.get()
                    get_benecity=CITY_BENEVAR.get()
                    get_province=PROVINCE_BENEVAR.get()
                    get_benezipcode=ZIPCODE_BENEVAR.get()
                    get_benecountry=COUNTRY_BENEVAR.get()
                    if get_fname == "" or get_mname == "" or get_lname == "" or get_age == "" or get_dob == "" or get_gender == "" or get_relation == "" or get_benemobile == "" or get_benelandline == "" or get_beneemail == "" or get_beneaddress == "" \
                            or get_benecity == "" or get_province == "" or get_benezipcode == "" or get_benecountry == "":
                        messagebox.showerror("", "Some fields are missing in Beneficiary information")
                    else:
                        con = mysql.connector.connect(host="localhost", user="root", password="", database='practicedb')
                        cur = con.cursor()
                        sql1 = "UPDATE tbl_contact_bene SET MOBILE =%s, LANDLINE =%s,EMAIL =%s  WHERE CONTACT_ID_BENE = %s"
                        val1 = (get_benemobile, get_benelandline, get_beneemail,bene_rownum)
                        cur.execute(sql1, val1)
                        con.commit()
                        sql2 = "UPDATE tbladdress_bene SET address =%s, city =%s,province=%s,zipcode=%s,country=%s  WHERE ADDRESS_ID = %s"
                        val2 = (get_beneaddress, get_benecity, get_province,get_benezipcode,get_benecountry,bene_rownum)
                        cur.execute(sql2, val2)
                        con.commit()

                        sql3 = "UPDATE tbl_bene SET firstname =%s, middlename =%s,lastname=%s,age=%s,birthday=%s ,gender=%s,relationship=%s WHERE BENE_ID = %s"
                        val3 = (get_fname, get_mname, get_lname, get_age, get_dob,get_gender,get_relation ,bene_rownum)
                        cur.execute(sql3, val3)
                        con.commit()
                        messagebox.showinfo("", "Beneficiary details Update Successfully!")

                        con.close()
                        self.FNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.MNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.LNAME_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.AGE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.calbenedob.config(state=DISABLED)
                        self.GENDER_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.RELATIONSHIP_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.PERCENT_LABELOUTPUT_BENE.config(state=DISABLED)
                        self.MOBILE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.LANDLINE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.EMAIL_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.ADDRESS_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.CITY_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.PROVINCE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.ZIPCODE_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                        self.COUNTRY_ENTRY_BENE_OUTPUT.config(state=DISABLED)
                else:
                    pass
            except:
                messagebox.showerror("","Unable to find Selected Beneficiary")


        ####### BENEFICIARY TREE VIEW#####
        self.trvbene = ttk.Treeview(self.treeviewbeneframe, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9], show="headings",height="3")
        self.trvbene.bind('<Double-Button-1>', clicktreeviewbene)
        self.trvbene.pack()
        # width of columns and alignment
        self.trvbene.column("1", width=80, anchor='c')
        self.trvbene.column("2", width=130, anchor='c')
        self.trvbene.column("3", width=120, anchor='c')
        self.trvbene.column("4", width=120, anchor='c')
        self.trvbene.column("5", width=50, anchor='c')
        self.trvbene.column("6", width=100, anchor='c')
        self.trvbene.column("7", width=100, anchor='c')
        self.trvbene.column("8", width=100, anchor='c')
        self.trvbene.column("9", width=100, anchor='c')
        # Headings
        # respective columns
        self.trvbene.heading("1", text="BENE NO.")
        self.trvbene.heading("2", text="Firstname")
        self.trvbene.heading("3", text="Middlename")
        self.trvbene.heading("4", text="Lastname")
        self.trvbene.heading("5", text="Age")
        self.trvbene.heading("6", text="Birthday")
        self.trvbene.heading("7", text="Gender")
        self.trvbene.heading("8", text="Relationship")
        self.trvbene.heading("9", text="Percentage")

    ###### BENE INFORMATION ###############
        FNAME_BENEVAR=StringVar()
        MNAME_BENEVAR=StringVar()
        LNAME_BENEVAR=StringVar()
        AGE_BENEVAR=StringVar()
        BDAY_BENEVAR=StringVar()
        GENDER_BENEVAR=StringVar()
        RELATIONSHIP_BENEVAR=StringVar()

        self.FNAME_LABEL_BENE = Label(self.benedetailsframe, text="First: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.FNAME_LABEL_BENE.place(x=5, y=10)
        self.FNAME_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=17, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=FNAME_BENEVAR)
        self.FNAME_ENTRY_BENE_OUTPUT.place(x=50, y=10)

        self.MNAME_LABEL_BENE = Label(self.benedetailsframe, text="Middle: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MNAME_LABEL_BENE.place(x=160, y=10)
        self.MNAME_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=17, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=MNAME_BENEVAR)
        self.MNAME_ENTRY_BENE_OUTPUT.place(x=220, y=10)

        self.LNAME_LABEL_BENE = Label(self.benedetailsframe, text="Last: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LNAME_LABEL_BENE.place(x=325, y=10)
        self.LNAME_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=20, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=LNAME_BENEVAR)
        self.LNAME_ENTRY_BENE_OUTPUT.place(x=365, y=10)

        self.AGE_LABEL_BENE = Label(self.benedetailsframe, text="Age: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.AGE_LABEL_BENE.place(x=5, y=35)
        self.AGE_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=8, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=AGE_BENEVAR)
        self.AGE_ENTRY_BENE_OUTPUT.place(x=50, y=35)

        self.BDAY_LABEL_BENE = Label(self.benedetailsframe, text="DOB:", bg='white', fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.BDAY_LABEL_BENE.place(x=5, y=60)
        self.calbenedob = DateEntry(self.benedetailsframe, date_pattern="yyyy-mm-dd", textvariable=BDAY_BENEVAR)
        self.calbenedob.place(x=50, y=60)

        self.GENDER_LABEL_BENE = Label(self.benedetailsframe, text="Gender: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.GENDER_LABEL_BENE.place(x=5, y=85)
        self.GENDER_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=12, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=GENDER_BENEVAR)
        self.GENDER_ENTRY_BENE_OUTPUT.place(x=70, y=85)

        self.RELATIONSHIP_LABEL_BENE = Label(self.benedetailsframe, text="Relationship: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.RELATIONSHIP_LABEL_BENE.place(x=180, y=65)
        self.RELATIONSHIP_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=15, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"), textvariable=RELATIONSHIP_BENEVAR)
        self.RELATIONSHIP_ENTRY_BENE_OUTPUT.place(x=290, y=65)

        self.PERCENT_LABEL_BENE = Label(self.benedetailsframe, text="Benefit(%): ", bg='white', border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PERCENT_LABEL_BENE.place(x=180, y=85)
        self.PERCENT_LABELOUTPUT_BENE = Label(self.benedetailsframe,width=10 ,bg='#c2bfba', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PERCENT_LABELOUTPUT_BENE.place(x=290, y=85)

        ####BENE CONTACT DETAILS ####
        MOBILE_BENEVAR = StringVar()
        LANDLINE_BENEVAR = StringVar()
        EMAIL_BENEVAR = StringVar()
        self.MOBILE_LABEL_BENE = Label(self.benedetailsframe, text="Mobile: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.MOBILE_LABEL_BENE.place(x=530, y=5)
        self.MOBILE_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=17, bg="#d1d0cd",fg='black',font=('ARIAL', 8, "bold"),textvariable=MOBILE_BENEVAR)
        self.MOBILE_ENTRY_BENE_OUTPUT.place(x=590, y=5)

        self.LANDLINE_LABEL_BENE = Label(self.benedetailsframe, text="Landline: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.LANDLINE_LABEL_BENE.place(x=520, y=30)
        self.LANDLINE_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=17, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=LANDLINE_BENEVAR)
        self.LANDLINE_ENTRY_BENE_OUTPUT.place(x=590, y=30)

        self.EMAIL_LABEL_BENE = Label(self.benedetailsframe, text="Email: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.EMAIL_LABEL_BENE.place(x=710, y=5)
        self.EMAIL_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=30, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=EMAIL_BENEVAR)
        self.EMAIL_ENTRY_BENE_OUTPUT.place(x=760, y=5)

        #### BENE ADDRESS DETAILS ####
        ADDRESS_BENEVAR=StringVar()
        CITY_BENEVAR=StringVar()
        PROVINCE_BENEVAR=StringVar()
        ZIPCODE_BENEVAR=StringVar()
        COUNTRY_BENEVAR=StringVar()
        self.ADDRESS_LABEL_BENE = Label(self.benedetailsframe, text="Address: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.ADDRESS_LABEL_BENE.place(x=520, y=55)
        self.ADDRESS_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=63, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=ADDRESS_BENEVAR)
        self.ADDRESS_ENTRY_BENE_OUTPUT.place(x=590, y=55)

        self.CITY_LABEL_BENE = Label(self.benedetailsframe, text="City: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.CITY_LABEL_BENE.place(x=540, y=80)
        self.CITY_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=30, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=CITY_BENEVAR)
        self.CITY_ENTRY_BENE_OUTPUT.place(x=590, y=80)

        self.PROVINCE_LABEL_BENE = Label(self.benedetailsframe, text="Province: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.PROVINCE_LABEL_BENE.place(x=790, y=80)
        self.PROVINCE_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=20, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=PROVINCE_BENEVAR)
        self.PROVINCE_ENTRY_BENE_OUTPUT.place(x=860, y=80)


        self.ZIPCODE_LABEL_BENE = Label(self.benedetailsframe, text="Zipcode: ", bg='white', border=0, fg='black',font=('Microsoft YaHei UI Light', 10, "bold"))
        self.ZIPCODE_LABEL_BENE.place(x=590, y=105)
        self.ZIPCODE_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=10, bg="#d1d0cd", fg='black', font=('ARIAL', 8, "bold"), textvariable=ZIPCODE_BENEVAR )
        self.ZIPCODE_ENTRY_BENE_OUTPUT.place(x=660,y=105)

        self.COUNTRY_LABEL_BENE = Label(self.benedetailsframe, text="Country: ", bg='white', border=0, fg='black', font=('Microsoft YaHei UI Light', 10, "bold"))
        self.COUNTRY_LABEL_BENE.place(x=730, y=105)
        self.COUNTRY_ENTRY_BENE_OUTPUT = Entry(self.benedetailsframe, width=8, bg="#d1d0cd", fg='black',font=('ARIAL', 8, "bold"),textvariable=COUNTRY_BENEVAR )
        self.COUNTRY_ENTRY_BENE_OUTPUT.place(x=800, y=105)


        self.BENE_EDIT_BUTTON=Button(self.benedetailsframe,text="EDIT",padx=11,bg="#f5b32f",fg="white",activebackground="#c79f1a",border=0,command=bene_enablefunction)
        self.BENE_EDIT_BUTTON.place(x=30,y=140)
        self.BENE_SAVEUPDATE_BUTTON = Button(self.benedetailsframe, text="SAVE", padx=10, bg="#3ab55f", fg="white",activebackground="#05872c", border=0, command=bene_update_contactaddress)
        self.BENE_SAVEUPDATE_BUTTON.place(x=80, y=140)
        self.BENE_CANCELEDIT_BUTTON = Button(self.benedetailsframe, text="CANCEL", padx=5, bg="#e66763", fg="white",activebackground="#ed2c26", border=0, command=insert_data_bene)
        self.BENE_CANCELEDIT_BUTTON.place(x=130, y=140)

        ##################################### END OF TAB3 BENEFICIARY DETAILS##########################################################















if __name__=='__main__':
    main()



