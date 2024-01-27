from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('datubaze.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS nomnieks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "vards" TEXT, 
    "uzvards" TEXT, 
    "talrunis" TEXT
)""")

db.commit()
@app.route('/')
def index():
  return render_template("index.html", title="Galvena Lapa") 

@app.route('/jauns', methods=['POST', 'GET'])
def nomnieki():
    if request.method == "POST":
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        talrunis = request.form["talrunis"]
        a = [vards,uzvards,talrunis]
        db = sqlite3.connect('datubaze.db')
        sql = db.cursor()
        sql.execute("INSERT INTO nomnieks(vards,uzvards,talrunis) VALUES(?,?,?)",a)
        db.commit()
    return render_template('jauns.html')
db.close()

@app.route('/dati', methods=['POST', 'GET'])
def dati():
  db = sqlite3.connect('datubaze.db')
  sql = db.cursor()
  sql.execute("SELECT * FROM nomnieks")
  records = sql.fetchall()
  #print(records)
  return render_template("dati.html", rows = records)

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("datubaze.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from nomnieks where id = ?",id)  
            msg = "record successfully deleted" 
        except:  
            msg = "can't be deleted" 
        finally:  
            return render_template("delete_record.html",msg = msg)


@app.route('/par')
def par():
  return render_template("par.html")


app.run(host='0.0.0.0', port=81)
