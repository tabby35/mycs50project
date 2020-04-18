from flask import render_template, request,redirect,session
from flask import Flask,flash
#from flask_session import Session
import sqlite3
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash,generate_password_hash

#con=sqlite3.connect("cong.db")
#cur=con.cursor()
#cur.execute("""CREATE TABLE data("Id INT PRIMARY KEY AUTO INCREMENT NOT NULL,publisher TEXT NOT NULL")""")
#cur.close()

app = Flask(__name__)

#@app.route("/")
#def index():
    #return render_template("homepage.html")

@app.route("/b4register")
def b4register():
    return render_template("register.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    #user reach route via post in register
    msg="this b4 signing up"
    if request.method=="POST" :
        if request.form["Name"] and request.form["password"]==request.form["confirmpassword"]:
                    #hash the password
                        try:
                            hash=generate_password_hash(request.form["password"])
                            Name=request.form["Name"]
                            #add if user doesnt exist
                            with sqlite3.connect("cong.db") as con:
                                cur=con.cursor()
                                cur.execute("INSERT INTO data (Name,hash) VALUES(?,?)",(Name,hash))
                                #automatically log in the user
                                #rows=cur.execute("SELECT* FROM adm WHERE Name=:Name",Name=Name)
                                #session["Name"]=rows[0]["Id"]
                                con.commit()
                                msg="succefully signed up"
                                return render_template("success.html",msg=msg)
                        except:
                            con.rollback()
                            return render_template("register.html",msg=msg)
                        #finally:  
                        #   con.close() 
                        #  msg="sucessfully registered" 
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", msg="your have succefully logged out")

@app.route("/")
def b4login():
    return render_template("login.html")

@app.route("/login",methods=["POST","GET"])
def login():
    #forget user id
    #session.clear()
    if request.method=="POST":
            #ENSURE DETAILS WERE SUBMITTED
            if not request.form["Name"] and not request.form["Password"]:
                return render_template("success.html",msg="password/name is required")
                #return render_template("success.html",msg="username is required")
            else:
                try:
                    with sqlite3.connect("cong.db") as con:
                        cur=con.cursor()
                        #check existance of password and name
                        rows=cur.execute("SELECT* data WHERE Name=:Name")
                        if len(rows)==1 and check_password_hash(rows["id"]["hash"],request.form["Password"]):
                            session["Name"]=rows["id"]["Name"]
                    return render_template("success.html",msg="log in successfull")
                except:xxxxxxxxxxxxx
                Returns = request.form["Returns"] 
                Publications = request.form["Publications"]
                Videos = request.form["Videos"] 
                with sqlite3.connect("cong.db") as con:  
                    cur = con.cursor()
                    cur.execute("INSERT into data (Name,Hours,Returns,Publications,Videos) values (?,?,?,?,?)",(Name,Hours,Returns,Publications,Videos))  
                    con.commit()  
                    msg = "successfully Added"  
            except:  
                con.rollback()  
                msg = "We can not add the to the list"  
            finally:  
                return render_template("success.html",msg = msg)  
                con.close()

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods=["POST"])
def deleterecord():
    msg="The msg if didnt load"
    name= request.form["name"]
    #Name= request.form["Name"]
    with sqlite3.connect("cong.db")as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM data WHERE name=?", name)
            #cur.commit()
            msg="DELETED SUCCEFULLY"
        except:
            #cur.rollback()
            msg="CAN NOT DELETE THE DATA"
        finally:
            return render_template("deleted.html",msg=msg)
            cur.close()

@app.route("/view")
def view():
    con=sqlite3.connect("cong.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data")
    rows=cur.fetchall()
    return render_template("view.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)