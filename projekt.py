from bottle import route, run, template, request, static_file, redirect
import pyodbc as db
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')

connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + config['DATABASE']['Server'] + ';DATABASE=' +
                        config['DATABASE']['Database'] + ';UID=' + config['DATABASE']['Username'] + ';PWD=' + config['DATABASE']['Password'])
cursor = connection.cursor() #type: db.Cursor

def save_pictures_to_file():
    bild_namn = getattr(request.forms,"picture")
    my_file = open("static","w")
    my_file.write("/static/" + bild_namn)
    my_file.close()

@route("/")
def index():
    #Visar förstasidan som består av ett formulär så man kan logga in
    return template("index")

@route("/flode")
def flode():
    return template("flode")

@route("/skapakonto")
def skapakontos():
    return template("skapakonto")

def checkpass(lösenord):
    lösenord = getattr(request.forms, "password")
    flag = 0
    while True:  
        if (len(lösenord)<6):
            flag = -1
            break
        elif not re.search("[a-z]", lösenord):
            flag = -1
            break
        elif not re.search("[A-Z]", lösenord):
            flag = -1
            break
        elif not re.search("[0-9]", lösenord):
            flag = -1
            break
        elif re.search("\s", lösenord):
            flag = -1
            break
        else:
            flag = 0
            return True
            break
    
    if flag ==-1:
        return False

@route("/new_member", method="POST")
def new_member():
    förnamn = getattr(request.forms, "fname")
    efternamn = getattr(request.forms, "lname")
    epost = getattr(request.forms,"email")
    födelsedag = getattr(request.forms,"bday")
    lösenord = getattr(request.forms,"password")
    
    while True:
        if checkpass(lösenord):
            break
            
        else:
            skapakontos()           
            break

    cursor.execute("insert into Account(email, f_name, l_name, b_day, password) values (?, ?, ?, ?, ?)", epost, förnamn, efternamn, födelsedag, lösenord)
    connection.commit()
    return template("flode")

@route("/about")
def about():
    return template("about")

@route("/profil")
def profil():
    #Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna
    cursor.execute("select picture_name from Recept")
    res = cursor.fetchall()
    images=[]
    for r in res:
        images.append(r[0])
    print(images)

    cursor.execute("select title from Recept")
    tes=cursor.fetchall()
    styles=[]
    for t in tes:
        styles.append(t[0])
    print(styles)
    
    return template("profil", images=images, styles=styles)

@route("/change_password", method="POST")
def change_password():
    old=getattr(request.forms, "old")
    new= getattr(request.forms, "new")
    cursor.execute("select * from Account where password=?",old)
    result=cursor.fetchall()
    if len(result)> 0:
        sql=("update Account set password=? where password=?")
        val=(new,old)
        cursor.execute(sql,val)
        cursor.commit()
    redirect("/profil")

@route("/flode",method = "POST")
def flodet():
    return template("flode")

@route("/skapa_recept")
def skaparecept():
    #Visar en sida där användarna kan skapa ett recept
    return template("skapa_recept")

@route("/saves_recepe", method="POST")
def save_to_db():
    #På denna länken kan användarna skapa recept
    titel= getattr(request.forms, "titel")
    ingredienser= getattr(request.forms, "ingredienser")
    instruktioner= getattr(request.forms,"instruktioner")
    ange_antal_portioner= getattr(request.forms,"portioner")
    bild_namn= getattr(request.forms,"picture")
    
    cursor.execute("insert into Recept(title, portion, ingresienses, rec_desc, picture_name ) values (?, ?, ?, ?, ?)", titel, ange_antal_portioner, ingredienser, instruktioner,"/static/" + bild_namn )
    connection.commit()

    return template("flode", files=save_pictures_to_file())

@route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="static")

run(host='127.0.0.1', port=8080, debug=True, reloader=True)



