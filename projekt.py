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
def index(error = ""):
    #Visar förstasidan som består av ett formulär så man kan logga in
    if request.query:
        error = getattr(request.query, "error")
    return template("index", error=error)

def check_log_in(epost, lösenord):
    cursor.execute('SELECT email, password FROM Account WHERE email = ? AND password = ?', (epost, lösenord))

@route('/log_in', method='POST')
def log_in():
    epost = getattr(request.forms, 'email')
    lösenord = getattr(request.forms, 'password')

    if check_log_in(epost, lösenord):
        return template('flode')
    else:
        return redirect('/?error=Felaktigt lösenord eller e-postadress')

@route('/settings')
def settings():
    return template('settings')

@route("/flode")
def flode():
    return template("flode")

@route("/skapakonto")
def skapakontos(error = ""):
    if request.query:
        error = getattr(request.query, "error") # Tar query från skapakonto.html och visar felmeddelande på samma sida
    return template("skapakonto", error=error)

def checkemail(epost):
    '''Funktion som berättar hur epostadress anges'''

    if(len(epost)<8):
        return False
    elif not re.search('[a-z]', epost):
        return False
    elif not re.search('[@]', epost):
        return False
    elif not re.search('[.]', epost):
        return False
    elif re.search('\s', epost):
        return False
    else:
        return True


def checkpass(lösenord):
    '''Funktion som berättar hur lösenord får anges.'''
 
    if (len(lösenord)<6):
        return False
    elif not re.search("[a-z]", lösenord):
        return False
    elif not re.search("[A-Z]", lösenord):
        return False
    elif not re.search("[0-9]", lösenord):
        return False
    elif re.search("\s", lösenord):
        return False
    else:
        return True

@route("/new_member", method="POST")
def new_member():
    förnamn = getattr(request.forms, "fname")
    efternamn = getattr(request.forms, "lname")
    epost = getattr(request.forms,"email")
    födelsedag = getattr(request.forms,"bday")
    lösenord = getattr(request.forms,"password")
    
    
    if checkpass(lösenord) and checkemail(epost):
        cursor.execute("insert into Account(email, f_name, l_name, b_day, password) values (?, ?, ?, ?, ?)", epost, förnamn, efternamn, födelsedag, lösenord)
        connection.commit()
        return template("flode")

    # Skapar felmeddelande om lösenord är inkorrekt
    else:
        return redirect("/skapakonto?error=Felaktigt lösenord eller e-postadress")

@route("/about")
def about():
    return template("about")

@route("/profil")
def profil():
    #Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna
    cursor.execute("select picture from Recipe")
    res = cursor.fetchall()
    images=[]
    for r in res:
        images.append(r[0])
    print(images)

    cursor.execute("select title from Recipe")
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

@route("/recipe") 
def show_recipe():
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser och instruktioner om respektive recept från databasen
    """
    cursor.execute("SELECT title from Recipe")
    ti = cursor.fetchall() # TODO
    title = []
    for i in ti:
        title.append(i[0])

    cursor.execute("SELECT ingredients from Recipe")
    ing = cursor.fetchall() # TODO
    ingredients = []
    for r in ing:
        ingredients.append(r[0])

    cursor.execute("SELECT instructions from Recipe")
    ins = cursor.fetchall() # TODO
    instructions = []
    for t in ins:
        instructions.append(t[0])
    return template("recipe", title = title, ingredients = ingredients, instructions = instructions)

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



