from bottle import route, run, template, redirect, request

@route("/flode")
def flode():
    return template("flode")

run(host="127.0.0.1", port=8090, debug=True, reloader=True)
