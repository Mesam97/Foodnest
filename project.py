import os
from bottle import route, run, template, request, static_file, redirect, app
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

foodnestdb = mysql.connector.connect(host=db_server,
                                    user=db_user,
                                    password=db_passwrd,
                                    database=db_name)

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
def profile(session, error= ""):
    """ Visar en profilsida med alla inlägg och möjlighet att navigera mellan sidor """ 

    print(session)
    cursor.execute(f"SELECT Picture, Recipeid, Title FROM Recipes WHERE Email = '{session['username']}'")
    recipes = cursor.fetchall()
    recipe_list = []

    #Lexikon
    for r in recipes:
        recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
        recipe_list.append(recipe_dict)
    
    # Tar query från create_account.html och visar felmeddelande på samma sida
    if request.query:
        error = getattr(request.query, 'error')

    return template('profile', recipes = recipe_list, error = error)



@route('/change_password', method = 'POST')
def change_password(session):
    old_password = getattr(request.forms, 'old-password')
    password = getattr(request.forms, 'new-password')
 
    if check_pass(password):
        cursor.execute(f"UPDATE Account SET Password = '{password}' WHERE Email = '{session['username']}'")
        foodnestdb.commit()
        return redirect('profile') 
    else:
        return redirect('/profile?error=Felaktigt lösenord')


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
def show_recipe(id, session):
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser, instruktioner, bild, portioner och kommentarer om respektive recept från databasen
    """
    cursor.execute('SELECT Picture, Title, Ingredients, Instructions, Portion FROM Recipes WHERE Recipeid = ' + id)
    recipes = cursor.fetchall()

    cursor.execute('SELECT Email, Sentence FROM Comments WHERE Recipeid = ' + id)
    comments = cursor.fetchall()

    comments_list = []
    
    #Lexikon
    for r in recipes:
        recipe_dict = {'picture': r[0], 'title': r[1], 'ingredients': r[2], 'instructions': r[3], 'portion': r[4], 'id': id}
    
    for c in comments:
        comments_dict = {'email': c[0], 'sentence': c[1], 'id': id}
        comments_list.append(comments_dict)

    # För att man ska kunna gilla/ogilla ett recept. Kopplat till JS
    liked = 0
    if request.query:
        liked = request.query['liked']
        try:
            if liked == '1':
                cursor.execute(f'INSERT INTO Post_likes(recipeid, email) VALUES ({id}, "{session["username"]}")')
                foodnestdb.commit()
            else:
                cursor.execute(f'DELETE FROM Post_likes WHERE Recipeid = {id} and Email =  "{session["username"]}"')              
                foodnestdb.commit()
        except:
            pass
        
    return template('recipe', recipes = recipe_dict, comments = comments_list, liked = liked)


@route('/save_comment/<id>', method = 'POST')
def save_comment(session, id):
    comment = getattr(request.forms, 'comment')

    sql = 'INSERT INTO Comments(Recipeid, Sentence, Email) VALUES (%s, %s, %s)'
    val = (id, comment, session['username'])
    cursor.execute(sql, val)
    foodnestdb.commit()

    return redirect('/recipe/' + id)


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

    sql = 'INSERT INTO Recipes(Title, Portion, Ingredients, Instructions, Picture, Email) VALUES (%s, %s, %s, %s, %s, %s)'
    val = (title, portions, ingredients, instructions, '/static/' + picture.filename, session['username'])
    cursor.execute(sql, val)
    #cursor.execute(f"select Recipeid from Recipes where Title= '{title}'")
    #id= cursor.fetchall()
    #cursor.execute('INSERT INTO Tags(Categories, Recipeid) VALUES (%s,%s)' % category, id)
    foodnestdb.commit()

    return redirect('posts')


@route('/log_out')
def logout(session):
    session['username'] = ''

    return redirect('/')


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


run(host='127.0.0.1', port=8070, debug=True, reloader=True)
#KD3