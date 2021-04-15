from bottle import route, run, template, request, static_file, redirect
import pyodbc as db
import configparser
import re
import os
import shutil

config = configparser.ConfigParser()
config.read('config.ini')

connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + config['DATABASE']['Server'] + ';DATABASE=' +
                        config['DATABASE']['Database'] + ';UID=' + config['DATABASE']['Username'] + ';PWD=' + config['DATABASE']['Password'])
cursor = connection.cursor() #type: db.Cursor

def save_picture():
    picture = getattr(request.files, 'picture')
    """ 
    source = picture
    destination =
    dest = shutil.move(source, destination) 
    """
    # Ska print finnas?
    print(picture)

@route('/')
def index(error = ''):
    """
    Visar förstasidan som består av ett formulär så man kan logga in 
    """
    if request.query:
        error = getattr(request.query, 'error')
    
    return template('index', error = error)

def check_log_in(email, password):
    cursor.execute('SELECT email, password FROM account WHERE email = ? AND password = ?', (email, password))

@route('/log_in', method='POST')
def log_in():
    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')

    if check_log_in(email, password):
        return template('posts')
    else:
        return redirect('/?error = Felaktigt lösenord eller e-postadress')

@route('/create_account')
def create_account(error = ''):
    # Tar query från skapakonto.html och visar felmeddelande på samma sida
    if request.query:
        error = getattr(request.query, 'error')

    return template('create_account', error = error)

def check_email(email):
    """ Funktion som berättar hur epostadress anges """

    if(len(email)<8):
        return False
    elif not re.search('[a-z]', email):
        return False
    elif not re.search('[@]', email):
        return False
    elif not re.search('[.]', email):
        return False
    elif re.search('\s', email):
        return False
    else:
        return True

def check_pass(password):
    """ Funktion som berättar hur lösenord får anges """
 
    if (len(password)<6):
        return False
    elif not re.search('[a-z]', password):
        return False
    elif not re.search('[A-Z]', password):
        return False
    elif not re.search('[0-9]', password):
        return False
    elif re.search('\s', password):
        return False
    else:
        return True

@route('/new_member', method = 'POST')
def new_member():
    first_name = getattr(request.forms, 'first-name')
    last_name = getattr(request.forms, 'last-name')
    email = getattr(request.forms, 'email')
    birthday = getattr(request.forms, 'birthday')
    password = getattr(request.forms, 'password')
    
    if check_pass(password) and check_email(email):
        cursor.execute('INSERT INTO account(email, first_name, last_name, birthday, password) VALUES (?, ?, ?, ?, ?)', email, first_name, last_name, birthday, password)
        connection.commit()
        return template('posts')

    # Skapar felmeddelande om lösenord är inkorrekt
    else:
        return redirect('/create_account?error = Felaktigt lösenord eller e-postadress')

@route('/about')
def about():
    return template('about')

@route('/profile')
def profile():
    """
    Visar en profilsida med alla inlägg och möjlighet till att navigera sig till dem andra sidorna
    """
    cursor.execute('SELECT picture FROM recipes')
    res = cursor.fetchall()
    images = []
    for r in res:
        images.append(r[0])

    cursor.execute('SELECT title FROM recipes')
    tes = cursor.fetchall()
    styles = []
    for t in tes:
        styles.append(t[0])
    
    return template('profile', images = images, styles = styles)

@route('/change_password', method = 'POST')
def change_password():
    old_password = getattr(request.forms, 'old-password')
    new_password = getattr(request.forms, 'new-password')
    cursor.execute('SELECT * FROM account WHERE password = ?', old)
    
    result = cursor.fetchall()
    if len(result) > 0:
        sql = ('UPDATE account SET password = ?  WHERE password = ?')
        val = (new-password, old-password)
        cursor.execute(sql, val)
        cursor.commit()

    return redirect('/profile')

@route('/posts')
def posts():
    return template('posts')

@route('/create_recipe')
def create_recipe():
    # Visar en sida där användarna kan skapa ett recept
    return template('create_recipe')

@route('/recipe') 
def show_recipe():
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser och instruktioner om respektive recept från databasen
    """
    cursor.execute('SELECT title FROM recipes')
    # TODO
    ti = cursor.fetchall()
    title = []
    for i in ti:
        title.append(i[0])

    cursor.execute('SELECT ingredients FROM recipes')
    # TODO
    ing = cursor.fetchall()
    ingredients = []
    for r in ing:
        ingredients.append(r[0])

    cursor.execute('SELECT instructions FROM recipes')
    # TODO
    ins = cursor.fetchall() 
    instructions = []
    for t in ins:
        instructions.append(t[0])
    return template('recipe', title = title, ingredients = ingredients, instructions = instructions)

@route('/save_recipe', method = 'POST')
def save_to_database():
    """ På denna länken kan användarna skapa recept """

    title = getattr(request.forms, 'title')
    ingredients = getattr(request.forms, 'ingredients')
    instructions = getattr(request.forms, 'instructions')
    portions = getattr(request.forms, 'portions')
    picture = getattr(request.forms, 'picture')
    
    cursor.execute('INSERT INTO recipes(title, portions, ingredients, instructions, picture) VALUES (?, ?, ?, ?, ?)', title, portions, ingredients, instructions, '/static/' + picture)
    connection.commit()
    return template('posts', files = save_picture())

@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root = 'static')

run(host='127.0.0.1', port=8070, debug=True, reloader=True)



