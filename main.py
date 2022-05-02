import os

# from numpy import broadcast
import pyrebase
from flask import Flask, session, render_template, request, redirect
# from flask_socketio import SocketIO, send

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyC71CWprW8zUaL0Td4w-YIoO7V_NxGgX-Y",
    "authDomain": "snakechat-316c0.firebaseapp.com",
    "databaseURL": "https://snakechat-316c0-default-rtdb.firebaseio.com",
    "projectId": "snakechat-316c0",
    "storageBucket": "snakechat-316c0.appspot.com",
    "messagingSenderId": "563952925760",
    "appId": "1:563952925760:web:7695afd6d2fa34b236f3a5",
    "measurementId": "G-K4QLTWEVN3"
}

#sessions

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app.secret_key = 'ilikepie'
# socketio = SocketIO(app)
# user = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

scores = {
    "Sal": 32,
    "Escher": 31,
        }

sorted_scores = dict( sorted(scores.items(),
                            key=lambda item: item[1],
                            reverse=True))

messages = db.child('messages').get()
mesg = messages.val()

sender = db.child('sender').get()
snd = sender.val()

pkg = zip(snd.values(), mesg.values())

# @app.route("/chat")
# @socketio.on('message')
# def handleMssage(msg):
#     print('Message: ' + msg)
#     send(msg, broadcast=True)
    # return render_template("chat.html")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/snakechat", methods=['GET', 'POST'])
def snakechat():

    try:

        if session["is_logged_in"] == True:

            global scores
            global sorted_scores

            if request.method == 'POST':
                name = request.form['name']

                db.child('messages').push(name)
                db.child('sender').push(session["email"])

                messages = db.child('messages').get()
                sender = db.child('sender').get()

                mesg = messages.val()
                snd = sender.val()

                pkg = zip(snd.values(), mesg.values())
                return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"], message = pkg)

            else:
                return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"], message = pkg)
    except Exception as e:
        # else:
        print("WHYYY")
        print(e)
        return render_template("index.html")



@app.route("/signup", methods=['GET', 'POST'])
def signup():

    global scores
    global sorted_scores

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # name = request.form['name']
        try:
            auth.create_user_with_email_and_password(email, password)
            user_session = auth.sign_in_with_email_and_password(email, password)
            # session['user'] = email
            global user
            session["is_logged_in"] = True
            session["email"] = user_session["email"]
            session["uid"] = user_session["localId"]
            # session["name"] = name
            # data = {"name": name, "email": email}
            # db.child("users").child(user["uid"]).set(data)
            return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"], message = pkg)
        except:
            print("Error Creating Account")
            return render_template("signup.html")
    else:
        try:
            if session["is_logged_in"] == True:
                return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"], message = pkg)
        except:
            # else:
            return render_template("signup.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():

    global scores
    global sorted_scores


    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("waat")
        try:
            user_session = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email

            global user
            session["is_logged_in"] = True
            session["email"] = user_session["email"]
            session["uid"] = user_session["localId"]
            # data = db.child("users").get()
            # user["name"] = data.val()[user["uid"]]["name"]
            return snakechat()
            # return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"])
        except:
            print("Check credentials")
            return render_template("signin.html")

    else:
        try:
            if session["is_logged_in"] == True:
                messages = db.child('messages').get()
                mesg = messages.val()

                sender = db.child('sender').get()
                snd = sender.val()

                pkg = zip(snd.values(), mesg.values())
                return render_template("snakechat.html", sorted_scores=sorted_scores, email = session["email"], message = pkg)
        except:
            # else:
            return render_template("signin.html")


@app.route("/signout")
def signout():
    global user
    # if user["is_logged_in"] == True:

    #     user = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
    #     # user["name"] == ""
    #     # user["email"] == ""
    #     # user["uid"] == ""
    #     return render_template("index.html")
    # else:
    session.pop('is_logged_in')
    session.pop('email')
    session.pop('uid')

    # user = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
    return render_template("index.html")

@app.route("/snakegame")
def snakegame():

    return render_template("snakegame.html")

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template("pagenotfound.html")



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    # socketio.run(app)
    app.run(host='127.0.0.1', port=8080, debug=True)