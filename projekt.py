from bottle import route, run, template, request, static_file
import pyodbc as db

server = '127.0.0.1'
username = 'Iloveglass'
password = '.'
database = 'foodnest'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor() #type: db.Cursor



@route("/")
def index():
    """Visar förstasidan som består av ett formulär så man kan logga in"""
    return template("index")

@route("/flode")
def flode():
    return template("flode")

@route("/skapakonto")
def skapakontos():
    return template("skapakonto")

@route("/about")
def about():
    return template("about")

@route("/profil")
def profil():
    #Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna
    #Måste fixa så att bilderna visas(ska fråga på onsdag)
    cursor.execute("select title from Recept")
    res = cursor.fetchone()
    while res:
        print(res)
        res = cursor.fetchone()
    return template("profil")

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

    cursor.execute("insert into Recept(title, portion, ingresienses, rec_desc ) values (?, ?, ?, ?)", titel, ange_antal_portioner, ingredienser, instruktioner )
    connection.commit()

    return template ("flode")

@route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="static")

run(host='127.0.0.1', port=8030)

