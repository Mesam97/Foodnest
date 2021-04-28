import os
from bottle import route, run, template, request, static_file, redirect, error
import pyodbc as db
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')

connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + config['DATABASE']['Server'] + ';DATABASE=' +
                        config['DATABASE']['Database'] + ';UID=' + config['DATABASE']['Username'] + ';PWD=' + config['DATABASE']['Password'])
cursor = connection.cursor() #type: db.Cursor

@route('/')
def index(error = ''):
    """ Visar förstasidan som består av ett logga in-formulär """
    if request.query:
        error = getattr(request.query, 'error')
    return template('index', error = error)


@route('/log_in', method = 'POST')
def log_in():
    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')
    user_account = (email) + (password)

    cursor.execute("SELECT * FROM account WHERE email = ? AND password = ?", (email, password))
    result = cursor.fetchall()
    if len(result) > 0:
        pass  
    else:
        return redirect('/?error=Felaktigt lösenord eller e-postadress')
    
    return redirect('posts')
    

def check_log_in(email, password):
    cursor.execute('SELECT * FROM account WHERE email =? AND password = ?', (email, password))
    account = cursor.fetchall()

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

@route('/posts', method = 'POST')
def new_member():
    first_name = getattr(request.forms, 'first-name')
    last_name = getattr(request.forms, 'last-name')
    email = getattr(request.forms, 'email')
    birthday = getattr(request.forms, 'birthday')
    password = getattr(request.forms, 'password')

    recipe_list = []
    
    # Skapar felmeddelande om lösenordet eller
    # epost är inte följer kraven
    if check_pass(password) and check_email(email):
        cursor.execute('INSERT INTO account(email, first_name, last_name, birthday, password) VALUES (?, ?, ?, ?, ?)', email, first_name, last_name, birthday, password)
        connection.commit()
        return template('posts', recipes = recipe_list)
    else:
        return redirect('/create_account?error=Felaktigt lösenord eller e-postadress')

@route('/about')
def about():
    """ Visar en sida om oss """
    return template('about')

@route('/profile')
def profile():
    """ Visar en profilsida med alla inlägg och möjlighet att navigera mellan sidor """
    cursor.execute('SELECT picture FROM recipes')
    image = cursor.fetchall()
    image_list = []
    for i in image:
        image_list.append(i[0])

    cursor.execute('SELECT title FROM recipes')
    title = cursor.fetchall()
    title_list = []
    for t in title:
        title_list.append(t[0])
    
    return template('profile', image = image_list, title = title_list)

@route('/change_password', method = 'POST')
def change_password():
    old_password = getattr(request.forms, 'old-password')
    new_password = getattr(request.forms, 'new-password')
    cursor.execute('SELECT * FROM account WHERE password = ?', old_password)
    
    result = cursor.fetchall()
    if len(result) > 0:
        sql = ('UPDATE account SET password = ?  WHERE password = ?')
        val = (new_password, old_password)
        cursor.execute(sql, val)
        cursor.commit()

    return redirect('/profile')

@route('/remove', method = 'POST')
def remove():
    if request.method == 'POST':
        if request.form['remove'] == 'remove':
            cursor.execute('DELETE * FROM recipes WHERE recipeid = 1')
        """checkbox = getattr(request.forms, 'remove')
        cursor.execute('SELECT * FROM recipes WHERE recipeid = 1')
        if checkbox == selected:
            
        cursor.commit()"""
    
        return template('profile', form=form)

@route('/posts')
def posts():
    """ Visar flöde-sidan som består av bilder på recepten """
    cursor.execute('SELECT picture, recipeid, title FROM recipes')
    recipes = cursor.fetchall()
    recipe_list = []
    for r in recipes:
        recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
        recipe_list.append(recipe_dict)

    return template('posts', recipes = recipe_list)

@route('/create_recipe')
def create_recipe():
    """ Visar en sida där användare kan skapa ett recept """
    return template('create_recipe')

@route('/recipe/<id>') 
def show_recipe(id):
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser och instruktioner om respektive recept från databasen
    """
    cursor.execute('SELECT picture, title, ingredients, instructions FROM recipes WHERE recipeid = ' + id)
    recipes = cursor.fetchall()
    for r in recipes:
        recipe_dict = {'picture': r[0], 'title': r[1], 'ingredients': r[2], 'instructions': r[3],'id': id}
 
    return template('recipe', recipes = recipe_dict)
    
@route('/save_recipe', method = 'POST')
def save_to_database():
    """ På denna länken kan användarna skapa recept """
    title = getattr(request.forms, 'title')
    ingredients = getattr(request.forms, 'ingredients')
    instructions = getattr(request.forms, 'instructions')
    portions = getattr(request.forms, 'portions')
    upload = getattr(request.files,"picture")
    
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return 'File extension not allowed.'

    save_path = f"static"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    upload.save(save_path)
    
    cursor.execute('INSERT INTO recipes(title, portion, ingredients, instructions, picture) VALUES (?, ?, ?, ?, ?)', title, portions, ingredients, instructions, '/static/' + upload.filename)
    connection.commit()

    return redirect('posts')

@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root = 'static')

@route('/recipe/static/<filename>')
def static_recipe(filename):
    """ För att varje recept ska visas på egen sida dvs. ta med HTML, CSS """
    return static_file(filename, root = 'static')

run(host='127.0.0.1', port=8030, debug=True, reloader=True)
