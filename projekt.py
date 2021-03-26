from bottle import route, run, template, request, static_file
import os, sys

def read_from_file():
    try: 
        my_file= open("storage/","r")
        my_file.close()

        return products
    except:
        my_file= open("storage/","w")
        my_file.write()
        my_file.close()

        return []

'''Visar forstasidan som bestar av ett formular sa man kan logga in'''
@route("/")
<<<<<<< Updated upstream
def profil():
    """Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna"""
    return template ("index")

run(host='127.0.0.1', port=8080)
=======
def index():
    return template("index")

'''Visar en profilsida med alla inlagg och mojlighet till att navigera sig till dem andra sidorna'''
@route("/profil")
def profil():
    return template("profil")

@route("/flode", method = "POST")
def flodet():
    return template("flode")

''' Pa denna lanken kan anvandarna skapa recept'''
@route("/skapa_recept")
def skaparecept():
    return template("skapa_recept")

@route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="static")

run(host='127.0.0.1', port=8070)
>>>>>>> Stashed changes
