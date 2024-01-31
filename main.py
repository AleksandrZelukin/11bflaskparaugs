from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

db = sqlite3.connect('datubaze.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS skolnieki(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "vards" TEXT, 
    "uzvards" TEXT, 
    "perskods" TEXT
)""")

db.commit()
@app.route('/')
def index():
  return render_template("index.html", title="Galvena Lapa") 
  #return render_template("login.html", title="Ieeja vietnē")

@app.route('/jauns', methods=['POST', 'GET'])
def skolnieki():
    if request.method == "POST":
        vards = request.form["vards"]
        uzvards = request.form["uzvards"]
        pk = request.form["personas kods"]
        a = [vards,uzvards,pk]
        db = sqlite3.connect('datubaze.db')
        sql = db.cursor()
        sql.execute("INSERT INTO skolnieki(vards,uzvards,perskods) VALUES(?,?,?)",a)
        db.commit()
    return render_template('jauns.html')
db.close()

@app.route('/dati', methods=['POST', 'GET'])
def dati():
  db = sqlite3.connect('datubaze.db')
  sql = db.cursor()
  sql.execute("SELECT * FROM skolnieki")
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
            cur.execute("delete from skolnieki where id = ?",id)  
            msg = "record successfully deleted" 
        except:  
            msg = "can't be deleted" 
        finally:  
            return render_template("delete_record.html",msg = msg)


@app.route('/par')
def par():
  return render_template("par.html")


app.run(host='0.0.0.0', port=81)
