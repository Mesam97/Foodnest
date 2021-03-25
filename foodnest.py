from bottle import route, run, template, redirect, request

@route("/flode")
def flode():
    picture_name = 'pesto_med_pasta.jpg'
    return template("flode", picture=picture_name)

@route("/storage/bilder/<picture>")
def serve_pictures(picture):
    return static_file(picture, root="storage/bilder")

run(host="127.0.0.1", port=8090, debug=True, reloader=True)
