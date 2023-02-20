#!C:\Users\JoshuaPC\AppData\Local\Programs\Python\Python310\python.exe
print ("Content-Type:text/html")
print()

import cgi
from tkcalendar import *
from datetime import datetime
import datetime
import cgitb; cgitb.enable()
import mysql.connector
import pandas as pd


form=cgi.FieldStorage()
ID=0   ### extract amount to policy payment
PN=form.getvalue("policynumber")
fullname=form.getvalue("fullname")
email=form.getvalue("email")
address=form.getvalue("address")
provinecity=form.getvalue("provinecity")
zipcode=form.getvalue("zipcode")
cardname=form.getvalue("Nameoncard")
cardnumber=form.getvalue("cardnumber")
expmonth=form.getvalue("expirationmonth")
expyear=form.getvalue("expirationyear")
cvv=form.getvalue("cvv")
paid_counter=None


def get_data():
    global strt_date,duration,frequency,Initialpaymentamount,Policy_ID,Policynum,payment_remaining
    con=mysql.connector.connect(host='localhost',username='root',password='',db='practicedb')
    cur=con.cursor()
    sql = "SELECT POLICY_ID,tbl_policy.POLICY_NUM,PAYMENT_TOTAL,START_DATE,PAYMENT_DURATION,FREQUENCY FROM tbl_policy where tbl_policy.POLICY_NUM='"+str(PN)+"'"
    cur.execute(sql)
    records = cur.fetchall()
    try:
        Policy_ID=records[0][0]
        Policynum =records[0][1]
        Initialpaymentamount= records[0][2]
        strt_date=records[0][3]
        duration=records[0][4]
        frequency=records[0][5]
        
        ##### To avoid multiple transaction from the link sent to client I extract Months paid
        # from the payment table and under the condition we can verify if the link was used. process complete if monthspaid=0 return error if monthspaid > 0
        sql1= "SELECT MONTHS_PAID FROM tbl_payment join tbl_policy on POLICY_ID=PAYMENT_ID_FK where tbl_policy.POLICY_NUM='"+str(PN)+"'"
        cur.execute(sql1)
        pay_item=cur.fetchone()
        try:  #### I use try Except to by pass error if client doesn`t pay yet so the page will accept the client`s `st payment.
            paid_counter=pay_item[0]
        except(TypeError,IndexError): ### except error in Index and type error.
            paid_counter=0

        if paid_counter==0:
            def get_duedate():
                global duedate,paid_month,paid_date,payment_remaining
                duedate=""
                paid_month=0
                paid_date=datetime.date.today()
                var=pd.to_datetime(strt_date)
                if duration=="10-YEARS":
                    dur=10
                    payment_per_year=12
                    payment_remaining=dur*payment_per_year
                    if frequency=="Monthly":            
                        date_range = datetime.timedelta(days=31)
                        ### calculate next duedate
                        duedate = date_range + var
                        ### calculate payment left
                        paid_month=paid_month+1
                        payment_remaining=payment_remaining-paid_month
                    elif frequency=="Quarterly":
                        date_range = datetime.timedelta(days=90)
                        ### calculate next duedate
                        duedate = date_range + var
                        ### calculate payment left
                        paid_month=paid_month+3
                        payment_remaining=payment_remaining-paid_month
                    elif frequency=="SemiAnnual":
                        date_range = datetime.timedelta(days=181)
                        ### calculate next duedate
                        duedate = date_range + var
                        ### calculate payment left
                        paid_month=paid_month+6
                        payment_remaining=payment_remaining-paid_month
                    elif frequency=="Annual":
                        date_range = datetime.timedelta(days=365)
                        ### calculate next duedate
                        duedate = date_range + var
                        ### calculate payment left
                        paid_month=paid_month+12
                        payment_remaining=payment_remaining-paid_month
                    return paid_month,payment_remaining
                
            def process_payment():
                con=mysql.connector.connect(host='localhost',username='root',password='',db='practicedb')
                cur=con.cursor()
                sql2="INSERT INTO tbl_payment(PAYMENT_ID,POLICY_NUM,PAY_STARTDATE,DUE_DATE,FULLNAME,EMAIL,ADDRESS,PROVINCECITY,ZIPCODE,CARDNAME,CARDNUM,EXPMONTH, EXPYEAR,CVV,amount,MONTHS_PAID,PAYMENT_REMAINING,PAYMENT_ID_FK) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val2=(ID,PN,paid_date,duedate,fullname,email,address,provinecity,zipcode,cardname,cardnumber,expmonth,expyear,cvv,Initialpaymentamount,paid_month,payment_remaining,Policy_ID)
                cur.execute(sql2, val2)
                con.commit()
                print("<div align=center> <h2> Payment Accepted </h2> <h3> Policy Number:</h3>"+ str(Policynum)+"  <h3> Amount Payed</h3>" + "PHP"+ " "+  str(Initialpaymentamount)+" </div>")
                
                sql3="UPDATE tbl_policy SET POLICY_STATUS =%s WHERE tbl_policy.POLICY_NUM =%s"
                val3=("ACTIVE",Policynum)
                cur.execute(sql3,val3)
                con.commit()
                
                sql4="UPDATE tbl_rider INNER join tbl_policy SET RIDER_STATUS=%s WHERE tbl_policy.POLICY_NUM =%s"
                val4=("ACTIVE",Policynum)
                cur.execute(sql4,val4)
                con.commit()
                cur.close()
                con.close()
            get_duedate()
            process_payment()
        else:
            print("<div align=center> <h2> Session Expired </h2>")
    except(ValueError,IndexError):
        print("<div align=center> <h2> Policy Number Invalid </h2>")
get_data()
    
     



    
