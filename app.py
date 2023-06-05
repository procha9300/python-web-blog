from flask import Flask, redirect, url_for, request, render_template, session
from flask_session import Session
import datetime
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
from bcrypt import hashpw, gensalt, checkpw
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():

    # App Config
    app = Flask(__name__)
    app.config['SESSION_PERMANENT'] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.myblog

    # Defining functions
    def sendEmail(receiver_email, subject, message):

        #Email config
        sender_email = os.getenv("EMAIL_APP")

        # SMTP server configuration (for Outlook.com)
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
        smtp_username = sender_email
        smtp_password = os.getenv("PASSWORD_APP")

        # Create the email message
        email = MIMEMultipart()
        email['From'] = sender_email
        email['To'] = receiver_email
        email['Subject'] = subject
        email.attach(MIMEText(message, 'html'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(email)
            print('Email sent successfully!')
        except Exception as e:
            print('Error sending email:', str(e))
        finally:
            server.quit()

    @app.route('/', methods=["GET", "POST"])
    def start():

        if request.method == 'GET':
            if session.get('name'):
                return redirect(url_for('home'))
            else:
                return render_template("login.html")

        elif request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            users = [e for e in app.db.users.find({})]
            flg = False

            for user in users:
                if user["username"] == username:
                    flg = True
                    break

            if flg and checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                print("success")
                session["name"] = username
                return redirect(url_for("home"))
            
            elif flg and not checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                print("Wrong Password!")
                return redirect(url_for("start"))
            else:
                print("Username %s does not exist." %username)
                return redirect(url_for("start"))


    @app.route('/signup/', methods=["GET", "POST"])
    def signup():

        if request.method == 'GET':
            return render_template("signup.html")

        elif request.method == 'POST':

            # Get form parameters
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            day = request.form.get("day")
            month = request.form.get("month")
            year = request.form.get("year")
            gender = request.form.get("gender")

            # Hash password
            hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

            # token for username
            user_token = secrets.token_urlsafe(32)
            user_hashed_token = hashpw(user_token.encode('utf-8'), gensalt()).decode('utf-8')

            # Build dict to insert in DB
            new_user = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "password": hashed_password,
                "birth_date": day+'-'+month+'-'+year,
                "gender" : gender,
                "validation" : False,
                "user_hashed_token" : user_hashed_token,
                "token_expire_dttm" : "",
                "token_recover_pass" : ""
            }        

            # insert entry in DB
            app.db.users.insert_one(new_user)

            # Send email to confirm registration
            link = url_for('verify', _external=True)
            subject = "myBlog: Confirm your registration."

            message = f"""Hi {first_name}!<br><br>
            You've just signup for myBlog with as '{username}'.<br><br>
            To confirm your registration by clicking 
            <a href="{link}?token={user_token}">here</a>.<br><br>"""

            sendEmail(email, subject, message)

            return redirect(url_for('start'))
        
    @app.route('/signup/verification')
    def verify():
        user_token = request.args.get("token")
        users = [e for e in app.db.users.find({})]

        for user in users:

            try:
                if user["user_hashed_token"] == '' : continue
            except: continue

            if checkpw(user_token.encode('utf-8'), user["user_hashed_token"].encode('utf-8')):
                username = user["username"]
                app.db.users.update_one(
                                    {"username" : username}, 
                                    {"$set": 
                                        {
                                            "validation" : True,
                                            "user_hashed_token" : ""
                                        }
                                    }
                                )

                return render_template("verify.html")

        return render_template("invalid_link.html", error=401, msg="Unexpected Token")

    @app.route('/datavalidation', methods=['GET', 'POST'])
    def validate():

        if request.method == 'GET':
            # Check if user already exists
            data = request.args.to_dict()
            field = list(data.keys())
            elem = list(data.values())

            users = [e for e in app.db.users.find({})]

            for user in users:
                for i in range(len(field)):
                    if user.get(field[i]) == elem[i]:
                        print("already exists!")
                        return {'status' : 'Already exists'}

            return {'status' : 'OK'}
        
        elif request.method == 'POST':
            
            users = [e for e in app.db.users.find({})]

            for user in users:
                if user["username"] == session.get("name"):
                    flg = user["validation"]
                    break

            if flg: return {'status' : 'OK'}
            else: return {'status' : 'NOk'}


    @app.route('/reset/', methods=["GET", "POST"])
    def reset():
        if request.method == 'GET':
            return render_template("reset.html")
        
        elif request.method == 'POST':
            username = request.form.get("username")

            users = [e for e in app.db.users.find({})]

            for user in users:
                if user["username"] == username:
                    receiver_email = user["email"]
                    first_name = user["first_name"]
                    break

            # Generate a token
            token = secrets.token_urlsafe(32)
            hashed_token = hashpw(token.encode('utf-8'), gensalt()).decode('utf-8')
            token_expire_dttm = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

            app.db.users.update_one(
                            {"username" : username}, 
                            {"$set": {"token_recover_pass" : hashed_token,
                                    "token_expire_dttm" : token_expire_dttm}}
                        )
            
            link = url_for('reset', _external=True)
            subject = 'myBlog: Recover you password.'
            message = f"""Hi {first_name}!<br><br>
            To recover your password click
            <a href="{link}/{token}">here</a>.<br><br>"""

            sendEmail(receiver_email, subject, message)

            return redirect(url_for('start'))
        
    @app.route('/reset/<string:token>/', methods=["GET", "POST"])
    def recover(token):
        if request.method == 'GET':
            users = [e for e in app.db.users.find({})]
            now = datetime.datetime.now()
            username = ''

            for user in users:
                try:
                    expire_dttm = datetime.datetime.strptime(user['token_expire_dttm'], "%Y-%m-%d %H:%M:%S")
                except:
                    continue

                if checkpw(token.encode('utf-8'), user['token_recover_pass'].encode('utf-8')) and expire_dttm > now:
                    username = user['username']
                    return render_template("reset2.html", username=username)
                elif checkpw(token.encode('utf-8'), user['token_recover_pass'].encode('utf-8')) and expire_dttm <= now:
                    return render_template("invalid_link.html", error=498, msg="Token Expired")
            
            return render_template("invalid_link.html", error=401, msg="Unexpected Token")
        else:
            username = request.form.get("username")
            new_password = request.form.get("password")
            hashed_password = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
            invalid_dttm = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
            app.db.users.update_one(
                            {"username" : username}, 
                            {"$set": {"password" : hashed_password,
                                    "token_expire_dttm" : invalid_dttm}}
                        )
            return redirect(url_for('start'))


    @app.route('/home/', methods=["GET", "POST"])
    def home():

        if request.method == 'POST':

            entry_content = request.form.get("content")
            _date = datetime.datetime.today().strftime("%Y-%m-%d")
            formatted_date = datetime.datetime.strptime(_date, "%Y-%m-%d").strftime("%b %d")

            app.db.entries.insert_one(
                {
                    "username" : session.get('name'),
                    "content" : entry_content,
                    "date" : _date,
                    "formatted_date" : formatted_date
                }
            )

            return redirect(url_for('home'))

        elif request.method == 'GET':

            if session.get('name'):
                entries = [e for e in app.db.entries.find({})]
                entries_ = []
                for entry in entries:
                    try: entry["username"]
                    except: continue

                    if entry["username"] == session.get('name'):
                        entries_.append(entry)

                return render_template("home.html", entries=entries_, username=session.get('name'))
            else:
                return redirect(url_for('start'))

    @app.route("/logout/")
    def logout():
        session["name"] = None
        return redirect(url_for("start"))

    @app.route('/recent/')
    def recent():
        return 'recent'

    @app.route('/calendar/')
    def calendar():
        return 'calendar'

    # Handle 404 - Endpoint not found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('invalid_link.html', error=404, msg="Page not found")

    
    return app