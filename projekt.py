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

@route("/new_member", method="POST")
def new_member():
    förnamn= getattr(request.forms, "fname")
    efternamn= getattr(request.forms, "lname")
    epost= getattr(request.forms,"email")
    födelsedag= getattr(request.forms,"bday")
    lösenord= getattr(request.forms,"password")

    cursor.execute("insert into Recept(email, f_name, l_name, b_day, password ) values (?, ?, ?, ?)", epost, förnamn, efternamn, födelsedag,  lösenord)
    connection.commit()

    return template ("flode")

@route("/about")
def about():
    return template("about")

@route("/profil")
def profil():
    #Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna
    #Måste fixa så att bilderna visas(funkar nästan helt)
    cursor.execute("select picture_name from pictures")
    res = cursor.fetchone()
    while res:
        print(res)
        res = cursor.fetchone()

    cursor.execute("select title from Recept")
    tes=cursor.fetchone()
    while tes:
        print(tes)
        tes = cursor.fetchone()
        
    return template("profil", res=res, tes=tes)

@route("/liked_recepes")
def liked():
    #Visar en sida med alla inlägg som man har gillat och möjlighet till att navigera sig till dem andra sidorna
    #Måste fixa så att bilderna visas(funkar nästan helt)
    cursor.execute("select picture_name from pictures")
    res = cursor.fetchone()
    while res:
        print(res)
        res = cursor.fetchone()

    cursor.execute("select title from Recept")
    tes=cursor.fetchone()
    while tes:
        print(tes)
        tes = cursor.fetchone()
        
    return template("liked_recepes", res=res, tes=tes)

@route("/remove")
def remove_post():
    #visar en sida där användaren skriver in titeln på det inlägg som ska tas bort
    return template("profil")
    
@route("/delete")
def delete():
    #Funktionen som tar bort inlägget ifrån databasen
    titel= getattr(request.forms, "remove")
    cursor.execute("select * from Recept where title = ?", titel)
    result = cursor.fetchall()
    if len(result) > 0:
        cursor.execute("delete from Recept where title = ?", titel)
        print("Inlägget är borttaget.")    
    else: 
        print("Det inlägget finns inte")
        
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
    bild_namn= getattr(request.forms,"picture")
    
    cursor.execute("insert into pictures(picture_name) values(?)",bild_namn)
    cursor.execute("insert into Recept(title, portion, ingresienses, rec_desc ) values (?, ?, ?, ?)", titel, ange_antal_portioner, ingredienser, instruktioner )
    connection.commit()

    return template ("flode")

@route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="static")

run(host='127.0.0.1', port=8030)

