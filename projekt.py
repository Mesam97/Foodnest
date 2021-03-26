from bottle import route, run, template, request

def read_from_file():
    try: 
        my_file= open("storage/", "r")
        my_file.close()

        return products
    except:
        my_file= open("storage/", "w")
        my_file.write()
        my_file.close()

        return []

@route("/")
def index():
    """Visar förstasidan som består av ett formulär så man kan logga in"""
    return template ("index")

@route("/flode")
def flode():
    return template("flode")

@route("/profil")
def profil():
    """Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna"""
    return template ("profil")

@route("/flode", method = "POST")
def flodet():
    return template ("flode")

@route("/skapa_recept")
def skaparecept():
    ''' På denna länken kan användarna skapa recept'''
    return template("skapa_recept")

run(host='127.0.0.1', port=8080)

