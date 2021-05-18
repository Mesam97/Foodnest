import os
from bottle import route, run, template, request, static_file, redirect, error, app
import bottle_session
import re
import mysql.connector
import configparser

app = app()
plugin = bottle_session.SessionPlugin(cookie_lifetime=600)
app.install(plugin)

config = configparser.ConfigParser()
config.read('config.ini')

db_user = config['DATABASE']['User']
db_name = config['DATABASE']['Database']
db_passwrd = config['DATABASE']['Password']
db_server = config['DATABASE']['Server']

foodnestdb = mysql.connector.connect(host=db_server,user=db_user,password=db_passwrd,database=db_name)

cursor = foodnestdb.cursor()

@route('/')
def index(error = ''):
    """ Visar förstasidan som består av ett logga in-formulär """

    if request.query:
        error = getattr(request.query, 'error')
    return template('index', error = error)


@route('/log_in', method = 'POST')
def log_in(session):
    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')

    cursor.execute('SELECT * FROM Account WHERE Email = %s AND password = %s', (email, password))
    result = cursor.fetchall()
    if result:
        session['username'] = email  
    else:
        return redirect('/?error=Felaktigt lösenord eller e-postadress')
    
    return redirect('posts')
    

def check_log_in(email, password):
    cursor.execute('SELECT * FROM Account WHERE Email = %s AND password = %s', (email, password))
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
    
    # Skapar felmeddelande om lösenordet eller epost är inte följer kraven
    if check_pass(password) and check_email(email):
        sql = 'INSERT INTO Account(email, first_name, last_name, birthday, password) VALUES (%s, %s, %s, %s, %s)'
        val = (email, first_name, last_name, birthday, password)
        cursor.execute(sql, val)
        foodnestdb.commit()
        return template('posts', recipes = recipe_list)
    else:
        return redirect('/create_account?error=Felaktigt lösenord eller e-postadress')


@route('/about')
def about():
    """ Visar en sida om oss """
    return template('about')


@route('/profile')
def profile(session):
    """ Visar en profilsida med alla inlägg och möjlighet att navigera mellan sidor """ 

    print(session)
    cursor.execute(f"SELECT Picture, Recipeid, Title FROM Recipes WHERE Email = '{session['username']}'")
    recipes = cursor.fetchall()
    recipe_list = []

    #Lexikon
    for r in recipes:
        recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
        recipe_list.append(recipe_dict)

    return template('profile', recipes = recipe_list)

@route('/password_error')
def password_error(error = ''):
    # Tar query från create_account.html och visar felmeddelande på samma sida
    if request.query:
        error = getattr(request.query, 'error')
    return template('index', error = error)


@route('/change_password', method = 'POST')
def change_password(session):
    old_password = getattr(request.forms, 'old-password')
    password = getattr(request.forms, 'new-password')
 
    if check_pass(password):
        sql = (f"UPDATE Account SET Password = %s WHERE Email = '{session['username']}'")
        val = (password, old_password)
        cursor.execute(sql, val)
        foodnestdb.commit()
        return redirect('profile') 
    else:
        return redirect('/password_error?error=Felaktigt lösenord')


@route('/remove/<id>')
def remove(session, id):
    cursor.execute('DELETE FROM Recipes WHERE Recipeid = ' + id)
    foodnestdb.commit()

    return redirect('/profile')


@route('/posts')
def posts():
    """ Visar flöde-sidan som består av bilder på recepten """
    cursor.execute('SELECT Picture, Recipeid, Title FROM Recipes')
    recipes = cursor.fetchall()

    recipe_list = []

    #Lexikon
    for r in recipes:
        recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
        recipe_list.append(recipe_dict)

    return template('posts', recipes = recipe_list)

@route('/posts', method='POST')
def posts_category():
    category = getattr(request.forms, 'category')
    if category == "Alla kategorier" or category == "Äldst":
        cursor.execute('SELECT Picture, Recipeid, Title FROM Recipes')
        recipes = cursor.fetchall()

        recipe_list = []

        #Lexikon
        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)
    elif category == "Nyast":
        cursor.execute("SELECT Picture, Recipeid, Title FROM Recipes ORDER BY Recipeid DESC")
        recipes = cursor.fetchall()

        recipe_list = []

        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)
    
    else: 
        sql = "SELECT Picture, Recipeid, Title FROM Recipes WHERE Categories = %s"
        val = (category, )
        cursor.execute(sql,val)
        recipes = cursor.fetchall()

        recipe_list = []

        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)

    return template('posts', recipes = recipe_list)

@route('/create_recipe')
def create_recipe(session):
    """ Visar en sida där användare kan skapa ett recept """
    return template('create_recipe')


@route('/recipe/<id>') 
def show_recipe(id):
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser och instruktioner om respektive recept från databasen
    """
    cursor.execute('SELECT Picture, Title, Ingredients, Instructions, Portion FROM Recipes WHERE Recipeid = ' + id)
    recipes = cursor.fetchall()

    #Lexikon
    for r in recipes:
        recipe_dict = {'picture': r[0], 'title': r[1], 'ingredients': r[2], 'instructions': r[3], 'portion': r[4], 'id': id}
 
    return template('recipe', recipes = recipe_dict)

@route('/save_recipe', method = 'POST')
def save_to_database(session):
    """ På denna länken kan användarna skapa recept """

    title = getattr(request.forms, 'title')
    ingredients = getattr(request.forms, 'ingredients')
    instructions = getattr(request.forms, 'instructions')
    portions = getattr(request.forms, 'portions')
    picture = getattr(request.files,'picture')
    category = getattr(request.forms, 'checkbox')
    
    name, ext = os.path.splitext(picture.filename)
    if ext not in ('.png', '.jpg', '.jpeg','.jfif'):
        return 'File extension not allowed.'

    save_path = f'static'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    picture.save(save_path)

    sql = 'INSERT INTO Recipes(Title, Portion, Ingredients, Instructions, Picture, Email, Categories) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = (title, portions, ingredients, instructions, '/static/' + picture.filename, session['username'], category)
    cursor.execute(sql, val)
    foodnestdb.commit()

    return redirect('posts')

@route('/log_out')
def logout(session):
    session['username'] = ''

    return redirect('/')

'''
Man skall kunna gilla ett recept
Man skall kunna ogilla ett gillat recept
Användare skall kunna se sina gillade recept
På inläggen skall användaren kunna se antalet gillningar
'''
@route('/like_recipe/<recipeid>', method = 'POST') #TODO
def like_recipe(session, recipeid):
    """
    Tabell som har koll på användare och recept, alltså en n-m-tabell. 
    När användaren gillar ett recept läggs en post i tabellen.
    En ändpunkt som tar en parameter: recept. Användaren via session
    """
    like_button = getattr(request.forms, 'like_button')

    sql = 'INSERT INTO Post_likes(recipeid, email, liked) VALUES (%s, %s, %s)'
    val = (recipeid, session['username'], true)
    cursor.execute(sql, val)
    foodnestdb.commit()

    return redirect('recipe')

def count_likes(): #TODO
    # likes = (select count(*) from post_likes where recipeid = ' + recipeid)
    pass

@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root = 'static')

@route('/recipe/static/<filename>')
def static_recipe(filename):
    """ För att varje recept ska visas på egen sida dvs. ta med HTML, CSS """
    return static_file(filename, root = 'static')

@route('/profile/static/<filename>')
def static_profile(filename):
    """ För att varje recept ska visas på egen sida dvs. ta med HTML, CSS """
    return static_file(filename, root = 'static')


run(host='127.0.0.1', port=8070)
