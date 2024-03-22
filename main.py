from flask import Flask,render_template,request
import sqlite3
import csv

app = Flask(__name__)

conn = sqlite3.connect("POKEDEX4.db")

c = conn.cursor()

statement = '''CREATE TABLE IF NOT EXISTS Pokemon(
            no TEXT PRIMARY KEY,
            name TEXT,
            type_1 TEXT,
            type_2 TEXT,
            total INTEGER,
            hp INTEGER,
            attack INTEGER,
            defense INTEGER,
            sp_atk INTEGER,
            sp_def INTEGER,
            speed INTEGER,
            generation INTEGER,
            legendary TEXT,
            unique(no,name)
            );'''

c.execute(statement)
file = open('Pokemon.csv')
data = csv.reader(file)

next(data) #remove header

statement = "INSERT INTO Pokemon(no,name,type_1,type_2,total,hp,attack,defense,sp_atk,sp_def,speed,generation,legendary) values(?,?,?,?,?,?,?,?,?,?,?,?,?)"
#c.executemany(statement,data)

conn.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/display', methods=['GET','POST'])
def display():
    
    if request.method == "GET":
        
        return render_template("display.html")
    else:
        num = int(request.form['num'])
        
        conn = sqlite3.connect("POKEDEX4.db")
        
        cursor = conn.cursor()
        
        
        display = cursor.execute("SELECT * from Pokemon").fetchmany(num)
        
        conn.close()
        return render_template("display.html", display = display)

@app.route('/type', methods=['GET','POST'])
def type():
  if request.method == "GET":
    return render_template("type.html")
    
  else:
    type1 = request.form['type1']

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    select = "select * from Pokemon where type_1 = ?"
    
    display = cursor.execute(select,(type1,)).fetchone()
    
    conn.close()
                             
    return render_template("type.html", display = display)

@app.route('/totalbase', methods=['GET','POST'])
def totalbase():
  if request.method == "GET":
    return render_template("totalbase.html")
    
  else:
    user_base = request.form['user_base']

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    select2 = "SELECT * FROM Pokemon WHERE total = ?"
    
    display = cursor.execute(select2,(user_base,)).fetchall()
    
    conn.close()
                             
    return render_template("totalbase.html", display = display)


@app.route('/minstat', methods=['GET','POST'])
def minstat():
  if request.method == "GET":
    return render_template("minstat.html")
    
  else:
    mindef = int(request.form['mindef'])
    minatk = int(request.form['minatk'])
    minspeed = int(request.form['minspeed'])

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    select2 = "SELECT * FROM Pokemon WHERE sp_atk >= ? and sp_def >= ? and speed >= ?"
    
    display = cursor.execute(select2,(minatk,mindef,minspeed,)).fetchall()
    
    conn.close()
                             
    return render_template("minstat.html", display = display)

@app.route('/legendary', methods=['GET','POST'])
def legendary():
  if request.method == "GET":
    return render_template("legendary.html")
    
  else:
    user_type1 = request.form['user_type1']
    user_type2 = request.form['user_type2']

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    select2 = "SELECT * FROM Pokemon WHERE legendary = 'TRUE' and type_1 = ?  and type_2 = ?"
    
    display = cursor.execute(select2,(user_type1,user_type2,)).fetchall()
    
    conn.close()
                             
    return render_template("legendary.html", display = display)

@app.route('/insert', methods=['GET','POST'])
def insert():
  if request.method == "GET":
    return render_template("insert.html")
    
  else:
    uno = request.form['uno']
    uname = request.form['uname']
    utype1 = request.form['utype1']
    utype2 = request.form['utype2']
    utotal = request.form['utotal']
    uhp = request.form['uhp']
    uattack = request.form['uattack']
    udefense = request.form['udefense']
    usp_atk = request.form['usp_atk']
    usp_def = request.form['usp_def']
    uspeed = request.form['uspeed']
    ugeneration = request.form['ugeneration']
    ulegendary = request.form['ulegendary']

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    sql = "INSERT INTO Pokemon(no,name,type_1,type_2,total,hp,attack,defense,sp_atk,sp_def,speed,generation,legendary) values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(sql,(uno,uname,utype1,utype2,utotal,uhp,uattack,udefense,usp_atk,usp_def,uspeed,ugeneration,ulegendary))

    display = cursor.execute("SELECT * FROM Pokemon").fetchall()
    
    conn.close()
                             
    return render_template("insert.html", display = display)

@app.route('/HP', methods=['GET','POST'])
def HP():
  if request.method == "GET":
    return render_template("HP.html")
    
  else:
    minhp = request.form['minhp']

    conn = sqlite3.connect("POKEDEX4.db")
    
    cursor = conn.cursor()
    
    select_all = "SELECT type_1,count(type_1) FROM Pokemon WHERE hp > ? GROUP BY type_1 ORDER BY hp DESC"
    
    display = cursor.execute(select_all,(minhp,)).fetchall()
    
    conn.close()
                             
    return render_template("HP.html", display = display)


if __name__ == '__main__':
    app.run()
