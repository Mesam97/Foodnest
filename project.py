import os
from bottle import route, run, template, request, static_file, redirect, app
import bottle_session
import re
import mysql.connector
import configparser

app = app()
plugin = bottle_session.SessionPlugin(cookie_lifetime=None)
app.install(plugin)

config = configparser.ConfigParser()
config.read('config.ini')

db_user = config['DATABASE']['User']
db_name = config['DATABASE']['Database']
db_passwrd = config['DATABASE']['Password']
db_server = config['DATABASE']['Server']

foodnestdb = mysql.connector.connect(host = db_server,
                                    user = db_user,
                                    password = db_passwrd,
                                    database = db_name)

cursor = foodnestdb.cursor(buffered = True)

@route('/')
def index(error = ''):
    # Visar förstasidan som består av ett logga in-formulär 

    if request.query:
        error = getattr(request.query, 'error')
    return template('index', error = error)


@route('/log_in', method = 'POST')
def log_in(session):
    # Hämtar email och lösenord från databasen. 

    email = getattr(request.forms, 'email')
    password = getattr(request.forms, 'password')

    cursor.execute('SELECT * FROM Account WHERE Email = %s AND password = %s', (email, password))
    result = cursor.fetchall()
    if result:
        session['username'] = email 

    else:
        return redirect('/?error=Felaktigt lösenord eller e-postadress')
    
    return redirect('posts')
    

@route('/create_account')
def create_account(error = ''):
    # Tar query från skapakonto.html och visar felmeddelande på samma sida
    if request.query:
        error = getattr(request.query, 'error')

    return template('create_account', error = error)


def check_email(email):
    # Funktion som berättar hur epostadress anges 

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
    # Funktion som berättar hur lösenord får anges 
 
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
def new_member(session):
    # Hämtar svar från ett forumlär i create_account.html och lägger in dem i databasen
    first_name = getattr(request.forms, 'first-name')
    last_name = getattr(request.forms, 'last-name')
    email = getattr(request.forms, 'email')
    birthday = getattr(request.forms, 'birthday')
    password = getattr(request.forms, 'password')

    if check_pass(password) and check_email(email):
        sql = 'INSERT INTO Account(Email, First_name, Last_name, Birthday, Password) VALUES (%s, %s, %s, %s, %s)'
        values = (email, first_name, last_name, birthday, password)
        cursor.execute(sql, values)
        foodnestdb.commit()
        session['username'] = email 
        print('Hej?')

        return redirect('/posts')
    else:
        # Skapar felmeddelande om lösenord eller epost inte följer kraven
        return redirect('/create_account?error=Felaktigt lösenord eller e-postadress')


@route('/about')
def about():
    # Visar en sida om oss 

    return template('about')

@route('/about_index')
def about_index():
    # Visar en annan sida om oss, när användaren ej är inloggad 

    return template('about_index')


@route('/profile')
def profile(session, error = ''):
    # Visar en profilsida med alla inlägg och möjlighet att navigera mellan sidor 

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
    # Hämtar svaren ifrån formulär på profile.html och ändrar lösenordet ifall det följer kraven
    old_password = getattr(request.forms, 'old-password')
    password = getattr(request.forms, 'new-password')
 
    if check_pass(password):
        cursor.execute(f"UPDATE Account SET Password = '{password}' WHERE Email = '{session['username']}'")
        foodnestdb.commit()
        return redirect('profile') 

    else:
        return redirect('/profile?error=Felaktigt lösenord')


@route('/remove/<id>')
def remove(id):
    # Tar bort allt som har med ett viss ID att göra
     
    cursor.execute('SELECT Picture FROM Recipes WHERE Recipeid = ' + id)
    picture = cursor.fetchall()
    # [4:-4] tar bort de fyra första och 4 sista tecknen i strängen (filnamnet)
    removed_picture = str(picture)[4:-4]

    # Tar bort filnamnet från mappen Static
    os.remove(removed_picture)
    
    # Deletar receptet från varje tabell, en i taget med parent-tabellen sist
    cursor.execute('DELETE FROM Tags WHERE Recipeid = ' + id)
    cursor.execute('DELETE FROM Likes WHERE Recipeid = ' + id)
    cursor.execute('DELETE FROM Comments WHERE Recipeid = ' + id)
    cursor.execute('DELETE FROM Recipes WHERE Recipeid = ' + id)
    foodnestdb.commit()

    return redirect('/profile')


@route('/posts')
def posts():
    # Visar flöde-sidan som består av bilder på recepten 

    cursor.execute('SELECT Picture, Recipeid, Title FROM Recipes')
    recipes = cursor.fetchall()

    recipe_list = []

    # Lexikon
    for r in recipes:
        recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
        recipe_list.append(recipe_dict)

    return template('posts', recipes = recipe_list)


@route('/posts', method='POST')
def category():
    # Hämtar svaren ifrån formulär och kategoriserar innehållet efter svaret
    category = getattr(request.forms, 'category')

    if category == 'Alla kategorier' or category == 'Äldsta':
        cursor.execute('SELECT Picture, Recipeid, Title FROM Recipes')
        recipes = cursor.fetchall()

        recipe_list = []

        # Lexikon
        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)

    elif category == 'Senaste':
        cursor.execute('SELECT Picture, Recipeid, Title FROM Recipes ORDER BY Recipeid DESC')
        recipes = cursor.fetchall()

        recipe_list = []

        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)

    elif category:
        cursor.execute('SELECT Recipes.Picture, Recipes.Recipeid, Recipes.Title '
                       'FROM Recipes INNER JOIN Tags ON Recipes.Recipeid = Tags.Recipeid '
                       'WHERE Tags.Categories = ' + '"' + category + '"')

        recipes = cursor.fetchall()

        recipe_list = []

        for r in recipes:
            recipe_dict = {'id': r[1], 'img': r[0], 'title': r[2]}
            recipe_list.append(recipe_dict)

    return template('posts', recipes = recipe_list)


@route('/create_recipe')
def create_recipe(session):
    # Visar en sida där användare kan skapa ett recept 

    return template('create_recipe')


@route('/recipe/<id>')
def show_recipe(id, session):
    """ 
    Webbsida för recept:
    Hämtar in titel, ingredienser, instruktioner, bild, portioner
    och kommentarer om respektive recept från databasen
    """

    # För att hämta info från databasen om ett viss recept
    cursor.execute('SELECT Account.First_name, Recipes.Picture, Recipes.Title, Recipes.Ingredients, Recipes.Instructions, Recipes.Portion '
                   'FROM Account INNER JOIN Recipes '
                   'ON Account.Email = Recipes.Email WHERE Recipeid = ' + id)
    recipes = cursor.fetchall()

    for r in recipes:
        recipe_dict = {'first_name': r[0], 'picture': r[1], 'title': r[2], 'ingredients': r[3], 'instructions': r[4], 'portion': r[5], 'id': id}

    # För att man ska kunna gilla/ogilla ett recept. Kopplat till JS
    liked = 0
    if request.query:
        liked = request.query['liked']

        try:
            if liked == '1':
                cursor.execute(f"INSERT INTO Likes(recipeid, email) VALUES ({id}, '{session['username']}')")
                foodnestdb.commit()

            else:
                cursor.execute(f"DELETE FROM Likes WHERE Recipeid = {id} and Email =  '{session['username']}'")              
                foodnestdb.commit()

        except:
            pass

    cursor.execute(f"SELECT * FROM Likes WHERE Recipeid = {id} AND Email = '{session['username']}'")
    likes = cursor.fetchall()

    if likes == []:
        liked = 0
    else:
        liked = 1
    
    # Funktionen så att man ska kunna se antal gillningar körs
    total_dict = count_likes(id)
    # Funktionen så att man ska kunna se kommentarer för ett viss recept körs
    comments_list = comment(id)
    
    return template('recipe', recipes = recipe_dict, comments = comments_list, liked = liked, total_likes = total_dict)


def count_likes(id):
    # Funtion så att man kan se antalet gillningar på ett specifikt recept 
    cursor.execute('SELECT COUNT(*) FROM Likes WHERE recipeid = ' + id)
    total_likes = cursor.fetchall()

    for t in total_likes:
        total_dict = {'likes': t[0]}

    return total_dict


@route('/likes')
def liked_recipes(session, error = ''):
    """
    Selectar och JOINAR data från tabellerna Recipes och Likes. 
    Väljer ut data som matchar den inloggade användarens email och det han/hon gillat.
    """
    cursor.execute(f"SELECT L.Recipeid, R.Picture, R.Title FROM Recipes AS R INNER JOIN Likes AS L ON R.Recipeid = L.Recipeid WHERE L.Email = '{session['username']}'")
    liked_recipes = cursor.fetchall()

    liked_list = []

    for l in liked_recipes:
        liked_dict = {'id': l[0], 'image': l[1], 'title': l[2]}
        liked_list.append(liked_dict)

    if request.query:
        error = getattr(request.query, 'error')

    return template('likes', liked = liked_list, error = error)


def comment(id):
    # Funktion som hämtar kommentarer från databasen om ett viss recept 
    cursor.execute('SELECT Account.First_name, Comments.Sentence '
                   'FROM Account INNER JOIN Comments '
                   'ON Account.Email = Comments.Email WHERE Recipeid = ' + id)
    comments = cursor.fetchall()

    comments_list = []

    for c in comments:
        comments_dict = {'first_name': c[0], 'sentence': c[1], 'id': id}
        comments_list.append(comments_dict)

    return comments_list


@route('/save_comment/<id>', method = 'POST')
def save_comment(session, id):
    """ 
    Tar kommentar från formulär och insertar det i tabellen Comments,
    som sen redirectar användaren till recipe + id 
    """
    comment = getattr(request.forms, 'comment')

    sql = 'INSERT INTO Comments(Recipeid, Sentence, Email) VALUES (%s, %s, %s)'
    values = (id, comment, session['username'])
    cursor.execute(sql, values)
    foodnestdb.commit()

    return redirect('/recipe/' + id)


@route('/save_recipe', method = 'POST')
def save_to_database(session):
    # Funktion som hämtar svaren ifrån formuläret i create_recipe.html och sparar det till databas

    title = getattr(request.forms, 'title')
    ingredients = getattr(request.forms, 'ingredients')
    instructions = getattr(request.forms, 'instructions')
    portions = getattr(request.forms, 'portions')
    picture = getattr(request.files,'picture')
    category = request.forms.getall('category[]')
    
    name, ext = os.path.splitext(picture.filename)
    if ext not in ('.png', '.jpg', '.jpeg','.jfif'):
        return 'File extension not allowed.'

    save_path = f'static'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    picture.save(save_path)

    sql = 'INSERT INTO Recipes(Title, Portion, Ingredients, Instructions, Picture, Email) VALUES (%s, %s, %s, %s, %s, %s)'
    values = (title, portions, ingredients, instructions, '/static/' + picture.filename, session['username'])
    cursor.execute(sql, values)
    id = cursor.lastrowid
    print(category)
    print(id)   

    for c in category:
    
        # Gör en foorloop, som går igenom lista med kategorier
        cursor.execute('INSERT INTO Tags(Categories, Recipeid) VALUES (%s,%s)', (str(c), str(id)))
        foodnestdb.commit()

    return redirect('posts')
 

@route('/log_out')
def logout(session):
    # Tömmer den inloggade användaren m.h.a. session 
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

run(host='127.0.0.1', port=8030, debug=True, reloader=True)
