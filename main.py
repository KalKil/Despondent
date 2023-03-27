from flask import Flask, render_template, request, redirect
import pymsql
import pymysql.cursors


app = Flask(__name__)

@app.route("/")
def index():
    print("despondentdemon")
    return render_template("home.html.jinja")

if __name__ == '__main__':
    app.run(debug=True)


Connection = pymsql.connect(
    host ='10.100.33.60',
    user='Kwilliams3',
    password='223686940',
    database='kwilliams3_social_phones',
    cursorclass=pymsql.cursors.DictCursor,
    autocommit=True
)

app.route('/feed')
def post_feed:

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `post` ORDER BY `timestamp`")

    results = cursor.fetchall()
        "feed.html.jinja",
