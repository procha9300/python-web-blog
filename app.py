from flask import Flask, redirect, url_for, request, render_template
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.myblog


    @app.route('/', methods=["GET", "POST"])
    def home():

        if request.method == 'POST':

            entry_content = request.form.get("content")
            _date = datetime.datetime.today().strftime("%Y-%m-%d")
            formatted_date = datetime.datetime.strptime(_date, "%Y-%m-%d").strftime("%b %d")

            app.db.entries.insert_one(
                {
                    "content" : entry_content,
                    "date" : _date,
                    "formatted_date" : formatted_date
                }
            )

        entries = [e for e in app.db.entries.find({})]

        return render_template("home.html", entries=entries)

    @app.route('/recent/')
    def recent():
        return 'recent'

    @app.route('/calendar/')
    def calendar():
        return 'calendar'
    
    return app
