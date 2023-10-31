from flask import Flask,render_template,request,session
import random
import string
import mysql.connector
import smtplib
jdb=Flask(__name__)

db=mysql.connector.connect(database="hotelmanagment",user="root",password="Password@123",port=3306)
c=db.cursor()

@jdb.route("/")
def home():
    return render_template("home.html")
@jdb.route("/Home") 
def myroot():
    return render_template("home.html")

@jdb.route("/customerLogin")
def customerLogin():
    return render_template("customerLogin.html")


@jdb.route("/customerReg")
def customerReg():
    return render_template("customerReg.html")

@jdb.route("/adminLogin")    
def adminLogin():
    return render_template("adminLogin.html")
@jdb.route("/SearchRooms")    
def searchRoom():
    return render_template("searchRoom.html")
@jdb.route("/customerHomePage")
def customerhomepage():
    return render_template("customerHomePage.html")
@jdb.route("/adminHomePage")
def adminhomepage():
    return render_template("adminHomePage.html")
@jdb.route("/rooms")    
def Rooms():
    return render_template("rooms.html")

@jdb.route("/addRooms")    
def addRooms():
    return render_template("addRooms.html")
@jdb.route("/AboutUs")
def AboutUs():
    return render_template("Aboutus.html")

@jdb.route("/ContactUs")
def ContactUs():
    return render_template("ContactUs.html")
    
@jdb.route("/logout")  
def logout():
    return render_template("home.html")
@jdb.route("/finalLogout")
def finalLogout():
     return render_template("finalLogout.html")

@jdb.route("/adminLoginDB",methods=['POST'])    
def adminLoginDB():
        un=request.form['uname']
        pwd=request.form['pwd']

        if un=='admin' and pwd=='admin':
                return render_template("adminHomePage.html")
        else:
                return render_template("adminLogin.html")

@jdb.route("/addRoomsDB",methods=['POST'])    
def addRoomsDB():
        rid=request.form['t1']
        rtype=request.form['t2']
        rprice=request.form['t3']
        

        sql="insert into rooms values("+str(rid)+",'"+rtype+"','"+rprice+"','yes')"
        c.execute(sql)
        db.commit()
        return render_template("rooms.html")

@jdb.route("/viewRooms")    
def viewRooms():
        c.execute("select roomnum,roomtype,roomprice from rooms")
        data=c.fetchall()
        
        #data is tuples in a list
        return render_template("viewRooms.html",d=data)
@jdb.route("/updateRoom",methods=['POST'])    
def updateRooms():
        roomno=request.form['roomno']
        c.execute("select * from rooms where roomnum="+roomno)
        data=c.fetchall()
        #data is tuples in a list
        return render_template("updateRoom.html",d=data)

@jdb.route("/updateRoomsDB",methods=['POST'])    
def updateRoomsDB():
        roomno=request.form['t1']
        rtype=request.form['t2']
        rprice=request.form['t3']
        

        sql="update rooms set roomnum='"+str(roomno)+"',roomtype='"+rtype+"',roomprice='"+rprice+"' where roomnum="+roomno

        c.execute(sql)
        db.commit()
        
        c.execute("select roomnum,roomtype,roomprice from rooms")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewRooms.html",d=data)
    
@jdb.route("/deleteRoom",methods=['POST'])    
def delete():
        roomno=request.form['roomno']
        
        sql="delete from rooms where roomnum="+roomno
        print(sql)
        c.execute(sql)
        db.commit()
        
        c.execute("select * from rooms")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewRooms.html",d=data)



@jdb.route("/customer")
def viewCustomerDetails():
        c.execute("select * from customers")
        data=c.fetchall()
        #data is tuples in a list
        return render_template("viewCustomers.html",d=data)


@jdb.route("/blockCustomer",methods=['POST'])    
def blockCustomer():
        cid=request.form['cid']
        c.execute("select roomnum from bookingdetails where custid={}".format(cid) )
        rnum=c.fetchall()[0][0]
        db.commit()
        
        
        sql1="update rooms set booked=\'no\'  where roomnum={} ".format(rnum)
        c.execute(sql1)
        db.commit()
       
        sql="delete from customers where id={}".format(cid)
        
        c.execute(sql)
        db.commit()
        
        c.execute("select * from customers ")
        data=c.fetchall()
        
        return render_template("viewCustomers.html",d=data)

    
@jdb.route("/booking")    
def bookingdetails():
        c.execute("select * from bookingdetails")
        data=c.fetchall()
       
        return render_template("bookingdetails.html",d=data)

@jdb.route("/payment")    
def paymentdetails():
        c.execute("select * from paymentdetails")
        data=c.fetchall()
        
        return render_template("paymentdetails.html",d=data)




@jdb.route("/customerLoginDB", methods=['POST'])
def customerLoginDB():
    uname = request.form['username']
    pwd = request.form['password']
    sql = "SELECT * FROM `customers` WHERE username='" + uname + "' and password='" + pwd + "'"
    c.execute(sql)
    d = c.fetchall()
    if len(d) > 0:
        session['cid'] = d[0][0]
        session['cname']=d[0][1]
        return render_template("customerHomePage.html")
    else:
        return render_template("customerLogin.html")

@jdb.route("/customerRegDB", methods=['POST'])
def customerRegDB():
    name = request.form['name']
    cont = request.form['contact']
    mail = request.form['mail']
    address = request.form['add']
    username = request.form['uname']
    #password = request.form['pwd']
    p=string.ascii_letters+string.digits
    password=''.join(random.choice(p) for i in range(8))
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("athmakurihemalatha2000@gmail.com","ktrcqmzwownpjgbf")
    s.sendmail("athmakurihemalatha2000@gmail.com",mail,"You Succesfully regstered forthe Luxury Hotel.Your Password is"+password)
    s.quit()
    sql = "insert into customers(name,contact,email,address,username,password) values('" + name + "','" + cont + "','" + mail + "','" + address + "','" + username + "','" + password + "')"
    c.execute(sql)
    db.commit()
    return render_template("customerLogin.html")
@jdb.route("/UserViewRooms")    
def UserviewRooms():
        c.execute("select roomnum,roomtype,roomprice from rooms where booked='no' ")
        data=c.fetchall()
        
        return render_template("UserViewRooms.html",d=data)
@jdb.route("/UserProfile")
def profile():
    cid = session['cid']
    c.execute("select * from customers WHERE id='" + str(cid) + "'")
    data = c.fetchall()
  
    return render_template("profile.html", d=data)


@jdb.route("/updateprofile", methods=['POST'])
def updateprofile():
    cid = session['cid']
    c.execute("select * from customers WHERE id='" + str(cid) + "'")
    data = c.fetchall()
   
    return render_template("updateProfile.html", d=data)


@jdb.route("/updateprofileDB", methods=['POST'])
def updateprofileDB():
    cid = session['cid']
    name = request.form['t1']
    contact = request.form['t2']
    mail = request.form['t3']
    address = request.form['t4']
    username = request.form['t5']
    password = request.form['t6']

    sql = "update customers set name=%s,contact=%s,email=%s,address=%s,username=%s,password=%s where id = %s"
    data = (name, contact, mail, address, username, password, cid)
    c.execute(sql, data)
    db.commit()

    c.execute("select * from customers WHERE id='" + str(cid) + "'")
    data = c.fetchall()
    return render_template("profile.html", d=data)     
    
@jdb.route("/BookRoom",methods=['POST'])    
def BookRoom():
    try:
        custid=session['cid']
        custname=session['cname']
        roomno=request.form['roomno']
        rtype=request.form['roomtype']
        rprice=request.form['roomprice']
        fprice=int(rprice)*2
        #rdura=request.form['days']
        #print(rdura)
      
        sql="insert into bookingdetails(custid,custname,roomnum,roomtype,price) values('"+str(custid)+"','"+custname+"','"+str(roomno)+"','"+rtype+"','"+str(fprice)+"')"
        c.execute(sql)
        db.commit()
        
        sql2="update rooms set booked=\'yes\'  where roomnum={} ".format(roomno)
        c.execute(sql2)
        db.commit()
        
        payid=random.randint(1000,9999)
        sql1="insert into paymentdetails(payid,custname,cost) values('"+str(payid)+"','"+custname+"','"+str(fprice)+"')"
        c.execute(sql1)
        db.commit()
        return render_template("customerHomePage.html")
    except:
         return render_template("ResponsePage.html")
    
@jdb.route("/MyBookings")    
def myBookings():
        cid=session['cid']
        c.execute("select * from bookingdetails where custid='"+str(cid)+"' ")
        data=c.fetchall()
        return render_template("userbookingdetails.html",d=data)
@jdb.route("/searchRoomsDB",methods=['POST'])  
def searchRoomsDB():
        rtype=request.form['rtype']
        print(rtype)
        
        c.execute("select * from rooms where roomtype='{}' and booked=\'no\'  ".format(rtype)  )
        
        data=c.fetchall()
        if len(data) > 0:
            return render_template("UserViewRooms.html",d=data)
        else:
            return render_template("ResponsePage.html")

if __name__=='__main__':
         jdb.secret_key='1234'
         jdb.run(port=8005)
